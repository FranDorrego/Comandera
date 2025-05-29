export default async function handler(req, res) {
  const url = process.env.link_base || "http://localhost:3001";

  if (req.method !== "GET") {
    return res.status(405).json({ error: "Método no permitido" });
  }

  try {
    const query = "SELECT cod_cat, nom_cat FROM categorias";

    const response = await fetch(`${url}/api/categorias`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });

    const data = await response.json();

    if (data.status !== "ok" || !Array.isArray(data.res)) {
      return res.status(500).json({ error: "Error al obtener categorías" });
    }

    const categorias = data.res.map((c) => ({
      cod_cat: c.cod_cat,
      nom_cat: c.nom_cat,
    }));

    return res.status(200).json({ status: "ok", categorias });
  } catch (err) {
    console.error("Error en /api/pedido/categoria:", err);
    return res.status(500).json({ error: "Error interno del servidor" });
  }
}
