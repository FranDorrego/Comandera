export default async function handler(req, res) {
  const { id } = req.query;
  const url = process.env.link_base || "http://localhost:3001";

  if (req.method !== "GET") {
    return res.status(405).json({ error: "Método no permitido" });
  }

  if (!id || isNaN(id)) {
    return res.status(400).json({ error: "ID inválido" });
  }

  const query = `SELECT * FROM mesas WHERE mes_cod='${id}' AND mes_tip='M'`;

  try {
    const response = await fetch(`${url}/api/mesas`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });

    const data = await response.json();

    if (data.status === "ok" && data.res.length > 0) {
      return res.status(200).json({ status: "ok", mesa: data.res[0] });
    } else {
      return res.status(404).json({ error: "Mesa no encontrada" });
    }
  } catch (err) {
    console.error("Error en /api/mesas/[id]:", err);
    return res.status(500).json({ error: "Error interno del servidor" });
  }
}
