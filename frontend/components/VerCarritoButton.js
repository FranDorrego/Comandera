import styles from "@/styles/pedido.module.css";

export default function VerCarritoButton({ visible }) {
  if (visible) return null;
  return (
    <button className={styles.verCarrito}
      onClick={() => document.querySelector('#carrito')?.scrollIntoView({ behavior: 'smooth' })}
    >🛒 Ver carrito</button>
  );
}