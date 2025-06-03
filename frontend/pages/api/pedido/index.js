
// Este endpoint recibe un pedido y lo guarda en la base de datos

export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Método no permitido" });
  }

  const url = process.env.link_base || "http://localhost:3001";
  const { mesa, mesero, items } = req.body;

  if (!mesa || !mesero || !Array.isArray(items)) {
    return res.status(400).json({ error: "Faltan datos necesarios" });
  }

  let meseroId = mesero;
  if (typeof mesero === "object" && mesero?.me_cod) {
    meseroId = mesero.me_cod;
  }

  try {
    // 🔍 Paso 1: Obtener configuración de la tabla `control`
    // Se obtiene la fecha (`con_fec`) y los flags de impresión (`imp_cpb`)
    const controlRes = await fetch(`${url}/api/control`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        query: "SELECT TOP 1 con_fec, imp_cpb FROM control ORDER BY con_fec DESC"
      }),
    });

    const controlData = await controlRes.json();

    // 🛑 Si no se obtiene un resultado válido, usar valores por defecto
    if (!controlData?.res?.[0]) {
      console.error("⚠ No se pudo obtener configuración de control:", controlData);
      controlData.res = [{
        con_fec: new Date().toISOString().slice(0, 10),
        imp_cpb: "000"
      }];
    }

    // 📅 Extraer fecha y hora del sistema o desde la tabla
    const { con_fec, imp_cpb } = controlData.res[0];
    const fecha = con_fec;
    const hora = new Date().toTimeString().slice(0, 5);

    // ⚙️ Paso 2: Determinar qué sectores deben imprimir (cocina, parrilla, bar)
    // Se interpreta el string binario imp_cpb (por ejemplo, "010")
    const imp_cpb_str = imp_cpb.toString().padStart(3, "0").toLowerCase();
    const impcocina = imp_cpb_str[0] === "0" ? 1 : 0;
    const impparrilla = imp_cpb_str[1] === "0" ? 1 : 0;
    const impbar = imp_cpb_str[2] === "0" ? 1 : 0;

    // 🧾 Paso 3: Insertar cada producto pedido en la tabla `cocina`
    for (const item of items) {
      // 🗒️ Formatear la observación del producto (escapando comillas si es necesario)
      const observacion = `W ${item.obs ? item.obs : ""}`;

      // 🧱 Construir query de inserción SQL
      const coc_con = Math.floor(Math.random() * 900000) + 100000; // ejemplo simple

      const query = `
        INSERT INTO cocina (
          coc_con, coc_mes, coc_pro, coc_can, coc_val, coc_obs,
          coc_est, coc_est1, coc_ela, coc_fac, coc_fac1,
          coc_mese, coc_fec, coc_hor, coc_per, coc_cos,
          coc_car, coc_div, coc_prep, impcocina, impbar, impparrilla,
          cli_id, men_cod, descuento
        )
        VALUES (
          '${coc_con}', '${mesa}', '${item.id}', ${item.cantidad}, ${item.total}, '${observacion}',
          '0', '0', '0', '0', '0',
          '${meseroId}', '${fecha}', '${hora}', '1', 0,
          '${meseroId}', '0', '0', ${impcocina}, ${impbar}, ${impparrilla},
          0, null, null
        )
      `;

      // 🚀 Ejecutar inserción en la base de datos
      const response = await fetch(`${url}/api/cocina`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });

      // 🧯 Verificar si hubo error al insertar
      if (!response.ok) {
        const error = await response.json();
        console.error("❌ Error al insertar pedido:", error);
        return res.status(500).json({ error: "Error al guardar pedido." });
      }
    }

    // ✅ Todo insertado correctamente
    return res.status(200).json({ status: "ok", cantidad: items.length });

  } catch (err) {
    // 🛑 Error inesperado
    console.error("❌ Error inesperado:", err);
    return res.status(500).json({ error: "Error inesperado al guardar pedido" });
  }
}
