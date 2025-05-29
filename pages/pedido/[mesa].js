import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import Cookies from "js-cookie";
import SearchAndList from "@/components/SearchAndList";
import Cart from "@/components/Cart";
import VerCarritoButton from "@/components/VerCarritoButton";
import styles from "@/styles/pedido.module.css";

export default function Pedido() {
  const router = useRouter();
  const { mesa } = router.query;
  const [carrito, setCarrito] = useState({});
  const [carritoVisible, setCarritoVisible] = useState(false);
  var mesero_actual = Cookies.get("mesero_actual");

  // Observa visibilidad del carrito
  useEffect(() => {
    const obs = new IntersectionObserver(([e]) => setCarritoVisible(e.isIntersecting));
    const el = document.querySelector('#carrito');
    if (el) obs.observe(el);
    return () => obs.disconnect();
  }, []);

  // Verifica si hay mesero actual
  useEffect(() => {
    if (!mesero_actual) {
      router.push("/");
    }
  }, []);

  const handleAdd = (producto, obs) => {
    const key = `${producto.id}-${producto.nombre}-${producto.precio}-${obs || ''}`;
    setCarrito((prev) => {
      const nuevo = { ...prev };
      if (!nuevo[key]) {
        nuevo[key] = { producto: producto, cantidad: 1, obs };
      } else {
        nuevo[key].cantidad += 0.5;
      }
      return nuevo;
    });
  };

  const handleRemove = key => {
    setCarrito(prev => {
      const next = { ...prev };
      if (next[key].cantidad > 1) next[key].cantidad -= 0.5;
      else delete next[key];
      return next;
    });
    // notificar online...
  };

  const handleSubmit = async () => {
    const items = Object.values(carrito).map(i => ({
      id: i.producto.id,
      nombre: i.producto.nombre,
      cantidad: i.cantidad,
      observacion: i.observacion,
      total: i.cantidad * i.producto.precio,
    }));
    const pedido = { mesa, mesero_actual, items, total: items.reduce((s, i) => s + i.total, 0) };
    await fetch('/api/pedido', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(pedido) });
    router.push('/mesas');
  };

  return (
    <>
      <div className={styles.container}>
        <div>
          <button onClick={() => router.push("/mesas")} className={styles.volver}>
            ⬅ Volver
          </button>
          <h2 className={styles.titulo}>Mesa {mesa}</h2>
        </div>

        <SearchAndList mesero={mesero_actual} mesa={mesa} onAdd={handleAdd} />
        <Cart carrito={carrito} onRemove={handleRemove} onSubmit={handleSubmit} />
        <VerCarritoButton visible={carritoVisible} />
      </div>
    </>
  );
}
