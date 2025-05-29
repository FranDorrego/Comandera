import { useEffect, useState } from "react";
import styles from "@/styles/pedido_shear.module.css";
import { formatearMiles } from "./utils";

export default function SearchAndList({ onAdd, mesero, mesa }) {
  const [productos, setProductos] = useState([]);
  const [filtro, setFiltro] = useState("");

  // Función reutilizable para cargar productos
  const cargarProductos = async (query = "") => {
    const endpoint = query
      ? `/api/pedido/search?name=${encodeURIComponent(query)}`
      : "/api/pedido/productos";

    const res = await fetch(endpoint);
    const data = await res.json();

    if (data.status === "ok") {
      const lista = data.productos.map(p => ({ ...p, obs: "" }));
      setProductos(lista);
    } else {
      setProductos([]);
    }

    // notificar online...
    fetch(`/api/pedido/online?mesa=${mesa}&user=${mesero?.me_id}`)
  };

  // Cargar inicial
  useEffect(() => {
    cargarProductos();
  }, []);

  // Búsqueda reactiva
  useEffect(() => {
    cargarProductos(filtro);
  }, [filtro]);

  return (
    <>
      <input
        className={styles.inputBuscar}
        type="text"
        placeholder="Buscar producto..."
        value={filtro}
        onChange={e => setFiltro(e.target.value)}
      />

      <div className={styles.productos}>
        {productos.length === 0 && (
          <div className={styles.empty}>
            <div className={styles.emptyIcon}>🛒</div>
            <p>No se encontraron productos</p>
          </div>
        )}


        {productos.length > 0 && productos.map(prod => (
          <div key={`${prod.id}-${prod.nombre}-${prod.precio}`} className={styles.card}>
            <div className={styles.cardHeader}>
              <h4>{prod.nombre}</h4>
              <span className={styles.precio}>${formatearMiles(prod.precio)}</span>
            </div>
            <input
              type="text"
              placeholder="Observación"
              value={prod.obs}
              onChange={e => {
                const obs = e.target.value;
                setProductos(ps => ps.map(p => p.id === prod.id ? { ...p, obs } : p));
              }}
              className={styles.observacion}
            />
            <button onClick={() => onAdd(prod, prod.obs || "")}>Agregar</button>
          </div>
        ))}
      </div>

    </>
  );
}
