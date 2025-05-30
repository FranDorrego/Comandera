import { actividadMesas } from "@/components/utils";


export default async function handler(req, res) {
  const url = process.env.link_base || "http://localhost:3001";

  try {
    // 1. Obtener mesas con tipo 'M'
    const mesasRes = await fetch(`${url}/api/mesas`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        query: "SELECT TOP 100 * FROM mesas WHERE mes_tip='M' ORDER BY VAL(mes_cod)",
      }),
    });
    const mesasData = await mesasRes.json();

    if (!mesasData.res || mesasData.res.length === 0) {
      return res.status(500).json({ error: "No se encontraron mesas" });
    }

    const todasMesas = mesasData.res
      .map((m) => parseInt(m.mes_cod))
      .filter(Boolean);

    // 2. Verificar uso en tiempo real (solo variable local)
    const ahora = new Date();
    const resultado = todasMesas.map((num) => {
      const actividad = actividadMesas[num];
      const estado =
        actividad && (ahora - new Date(actividad.time)) / 1000 < 60
          ? "en_uso"
          : "libre";

      return { numero: num, estado, tipo: "M" };
    });

    return res.status(200).json({ status: "ok", mesas: resultado });
  } catch (err) {
    console.error("Error en /api/mesas", err);
    return res.status(500).json({ error: "Error interno del servidor" });
  }
}
