export function formatearMiles(numero) {
  try {
    return new Intl.NumberFormat("es-AR").format(numero);
  } catch (err) {
    return numero;
  }
}


export const actividadMesas = {};
