import { actividadMesas } from "@/components/utils";

// Esta API maneja la actividad de las mesas en un sistema de pedidos online
// Permite registrar la actividad de una mesa y desocuparla si es necesario
// Esta función está desactivada

export default async function handler(req, res) {

  return res.status(200).json({ status: "ok", mensaje: "Funcion desactivada" });

  const { mesa, user, } = req.query;

  if (req.method !== "GET") {
    return res.status(405).json({ error: "Método no permitido" });
  }

  if (!mesa || !user) {
    return res.status(400).json({ error: "Faltan parámetros: mesa y user" });
  }

  if (req.query?.delete){
    delete actividadMesas[mesa];
    return res.status(200).json({ status: "ok", mensaje: "Mesa desocupada" });
  }

  actividadMesas[mesa] = {
    time: new Date().toISOString(),
    mesero: user,
  };

  return res.status(200).json({ status: "ok", actualizado: actividadMesas[mesa] });
}
