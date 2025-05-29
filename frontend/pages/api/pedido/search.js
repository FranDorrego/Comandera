export default async function handler(req, res) {
  const { name } = req.query;
  const url = process.env.link_base || "http://localhost:3001";

  if (req.method !== "GET") {
    return res.status(405).json({ error: "Método no permitido" });
  }

  if (!name || name.length < 1) {
    return res.status(400).json({ error: "Parámetro 'name' requerido" });
  }

  const searchTerm = name.replace(/'/g, "''"); // escapamos comillas simples
  const query = `SELECT TOP 8 pro_cod, pro_des, pro_val, pro_cat FROM productos WHERE pro_des LIKE '%${searchTerm}%' AND pro_val > 0`;

  try {
    const response = await fetch(`${url}/api/productos`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });

    const data = await response.json();

    if (data.status !== "ok") {
      return res.status(500).json({ error: "Error al consultar productos" });
    }

    const productos = (data.res || []).map((p) => ({
      id: parseInt(p.pro_cod),
      nombre: p.pro_des,
      precio: parseFloat(p.pro_val),
      categoria: p.pro_cat,
    }));

    return res.status(200).json({ status: "ok", productos });
  } catch (err) {
    console.error("Error en /api/pedido/search:", err);
    return res.status(500).json({ error: "Error interno del servidor" });
  }
}
