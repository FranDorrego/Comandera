export default async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).json({ error: "Método no permitido" });

  const url = process.env.link_base || "http://localhost:3001";
  const { mesa, mesero, items } = req.body;

  if (!mesa || !mesero || !Array.isArray(items)) {
    return res.status(400).json({ error: "Faltan datos necesarios" });
  }

  const now = new Date();
  const fecha = now.toISOString().slice(0, 10).replace(/-/g, "/");
  const hora = now.toTimeString().slice(0, 5);

  try {
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
          '${mesa}', '${item.id}', ${item.cantidad}, ${item.total / item.cantidad || 0}, '',
          '0', '0', '0', '0', '0',
          '${mesero}', '${fecha}', '${hora}', '1', 0,
          '${mesero}', '0', '0', '1', '1', '1',
          0, null, null
        )
      `;

      await fetch(`${url}/api/cocina`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });
    }

    res.status(200).json({ status: "ok", cantidad: items.length });
  } catch (err) {
    console.error("Error insertando pedido:", err);
    res.status(500).json({ error: "Error al guardar en cocina" });
  }
}
