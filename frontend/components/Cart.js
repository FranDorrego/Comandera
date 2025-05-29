import styles from "@/styles/pedido_cart.module.css";
import { formatearMiles } from "./utils";

export default function Cart({ carrito, onRemove, onSubmit }) {
  const items = Object.entries(carrito);
  const total = items.reduce((sum, [_, i]) => sum + i.cantidad * i.producto.precio, 0);
  return (
    <div id="carrito" className={styles.carrito}>
      <h3>Carrito</h3>
      {items.map(([key, item]) => (
        <div
          key={key}
          className={styles.item}
          data-precio={`$${formatearMiles(item.cantidad * item.producto.precio)}`}
        >
          <div>
            <span>{item.producto.nombre} ({item.cantidad})</span>
            {item.obs && <div className={styles.obs}><b>Obs:</b> {item.obs}</div>}
          </div>
          <button onClick={() => onRemove(key)} title="Quitar">
            🗑️
          </button>
        </div>
      ))}
      <p className={styles.total}>Total: ${formatearMiles(total)}</p>
      <button onClick={onSubmit} className={styles.enviar}>Enviar pedido</button>
    </div>
  );
}