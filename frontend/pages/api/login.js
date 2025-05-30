

export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Método no permitido" });
  }

  const { idMesero, clave } = req.body;

  if (!idMesero || !clave) {
    return res.status(400).json({ error: "Faltan datos" });
  }

  const url = process.env.link_base || "http://localhost:3001";

  const query = `SELECT * FROM meseros WHERE me_cod = '${idMesero}' AND me_ide = '${clave}'`;

  try {
    console.log(`${url}/api/meseros`, query)
    const response = await fetch(`${url}/api/meseros`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query }),
    });

    const data = await response.json();

    if (data.status !== "ok" || !data.res || data.res.length === 0) {
      return res.status(401).json({ error: "Credenciales inválidas" });
    }

    return res.status(200).json({ success: true, mesero: data.res[0] });
  } catch (error) {
    console.error("Error al conectar con el servidor Access:", error);
    return res.status(500).json({ error: "Error interno del servidor" });
  }
}
