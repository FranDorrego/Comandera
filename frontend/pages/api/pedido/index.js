import crypto from "crypto";

// Este endpoint recibe un pedido y lo guarda en la base de datos
// Si hay un error, hace rollback de los cambios

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

  const now = new Date();
  const fecha = now.toISOString().slice(0, 10).replace(/-/g, "/");
  const hora = now.toTimeString().slice(0, 5);
  const batchId = crypto.randomUUID().slice(0, 3); // pequeño identificador para rollback

  const queries = [];

  for (const item of items) {
    const query = `
      INSERT INTO cocina (
        coc_mes, coc_pro, coc_can, coc_val, coc_obs,
        coc_est, coc_est1, coc_ela, coc_fac, coc_fac1,
        coc_mese, coc_fec, coc_hor, coc_per, coc_cos,
        coc_car, coc_div, coc_prep, impcocina, impbar, impparrilla,
        cli_id, men_cod, descuento
      )
      VALUES (
        '${mesa}', '${item.id}', ${item.cantidad}, ${item.total / item.cantidad || 0},
        ${item.observacion ? `'${item.observacion}'` : 'null'},
        '0', '0', '0', '0', '0',
        '${meseroId}', '${fecha}', '${hora}', '1', 0,
        '${batchId}', '0', '0', '1', '1', '1',
        0, null, null
      )
    `;
    queries.push(query);
  }

  try {
    for (const query of queries) {
      const response = await fetch(`${url}/api/cocina`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });

      if (!response.ok) {
        const error = await response.json();
        console.error("❌ Error al insertar pedido:", error);

        // 🔁 Rollback
        const rollbackQuery = `DELETE FROM cocina WHERE coc_car = '${batchId}' AND coc_fec = '${fecha}' AND coc_hor = '${hora}'`;
        await fetch(`${url}/api/cocina`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ query: rollbackQuery }),
        });

        return res.status(500).json({ error: "Error al guardar en cocina. Se deshicieron los cambios." });
      }
    }

    return res.status(200).json({ status: "ok", cantidad: items.length });

  } catch (err) {
    console.error("❌ Error inesperado:", err);
    return res.status(500).json({ error: "Error inesperado al guardar en cocina" });
  }
}
