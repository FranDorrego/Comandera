import { actividadMesas } from "@/pages/mesas";

export default async function handler(req, res) {
  const { mesa, user } = req.query;

  if (req.method !== "GET") {
    return res.status(405).json({ error: "Método no permitido" });
  }

  if (!mesa || !user) {
    return res.status(400).json({ error: "Faltan parámetros: mesa y user" });
  }

  actividadMesas[mesa] = {
    time: new Date().toISOString(),
    mesero: user,
  };

  return res.status(200).json({ status: "ok", actualizado: actividadMesas[mesa] });
}
