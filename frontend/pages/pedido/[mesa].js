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
  const [mesero_actual, setMesero_actual] = useState(Cookies.get("mesero_actual"));

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
    setMesero_actual(JSON.parse(mesero_actual));
  }, []);


  const handleAdd = (producto, obs) => {
    const key = `${producto.id}-${producto.nombre}-${producto.precio}-${obs || ''}`;
    setCarrito((prev) => {
      const nuevo = { ...prev };
      if (!nuevo[key]) {
        nuevo[key] = { producto: producto, cantidad: 1, obs };
      } else {
        nuevo[key].cantidad += 1;
      }
      return nuevo;
    });

    // notificar online...
    //fetch(`/api/pedido/online?mesa=${mesa}&user=${mesero_actual?.me_des}`)
  };



  const handleRemove = key => {
    setCarrito(prev => {
      const next = { ...prev };
      if (next[key].cantidad > 1) next[key].cantidad -= 1;
      else delete next[key];
      return next;
    });

    // notificar online...
    //fetch(`/api/pedido/online?mesa=${mesa}&user=${mesero_actual?.me_des}`)
  };

  const handleSubmit = async () => {
    const items = Object.values(carrito).map(i => ({
      id: i.producto.id,
      nombre: i.producto.nombre,
      cantidad: i.cantidad,
      obs: i.obs,
      total: i.cantidad * i.producto.precio,
    }));
    const pedido = { mesa, mesero: { ...mesero_actual }, items, total: items.reduce((s, i) => s + i.total, 0) };
    const res = await fetch('/api/pedido', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(pedido) });
    if (!res.ok) {
      const error = await res.json();
      alert(`Error al enviar el pedido: ${error.error} Reintnta enviar.`);
      return;
    }
    else {
      router.push('/mesas');
    }

    // notificar online...
    //fetch(`/api/pedido/online?mesa=${mesa}&user=${mesero_actual?.me_des}&delete=true`)
  };

  return (
    <>
      <div className={styles.container}>
        <div>
          <div className={styles.name}>{mesero_actual?.me_des}</div>
          <button onClick={() => {
            //fetch(`/api/pedido/online?mesa=${mesa}&user=${mesero_actual?.me_des}&delete=true`);
            router.push("/mesas")
          }} className={styles.volver}>
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
