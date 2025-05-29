export default async function handler(req, res) {
  const url = process.env.link_base || "http://localhost:3001";
  const { categoria } = req.query;

  if (req.method !== "GET") {
    return res.status(405).json({ error: "Método no permitido" });
  }

  try {
    // 1. Armar query SQL
    let query = "SELECT TOP 5 pro_cod, pro_des, pro_val, pro_cat FROM productos where pro_val > 0";

    if (categoria) {
      query += ` WHERE pro_cat='${categoria}'`;
    } else {
      query += " ORDER BY RND(pro_cod)";
    }

    const productosRes = await fetch(`${url}/api/productos`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });

    const productosData = await productosRes.json();
    if (!productosData.res || productosData.res.length === 0) {
      return res.status(200).json({ status: "ok", productos: [] });
    }

    // 2. Mapear respuesta
    const productos = productosData.res.map((p) => ({
      id: parseInt(p.pro_cod),
      nombre: p.pro_des,
      precio: parseFloat(p.pro_val),
      categoria: p.pro_cat,
    }));

    return res.status(200).json({ status: "ok", productos });
  } catch (err) {
    console.error("Error en /api/pedido/productos:", err);
    return res.status(500).json({ error: "Error interno del servidor" });
  }
}
