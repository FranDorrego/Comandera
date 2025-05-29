import { useEffect, useState } from "react";
import styles from "@/styles/mesas.module.css";
import { useRouter } from "next/router";
import Image from "next/image";
import Cookies from "js-cookie";

export default function Mesas() {
  const MIN_POR_SECCION = 10;
  const MAX_SECCIONES = 5;

  const [mesas, setMesas] = useState([]);
  const [errorBuscar, setErrorBuscar] = useState("");
  const [buscarMesa, setBuscarMesa] = useState("");
  const [rango, setRango] = useState([1, 100]);
  const [mesero_actual, setMesero_actual] = useState(Cookies.get("mesero_actual"));
  const router = useRouter();

  useEffect(() => {
    const cargarMesas = async () => {
      try {
        const res = await fetch("/api/mesas");
        const data = await res.json();
        if (data.status === "ok") {
          const mesasFiltradas = data.mesas.filter((m) => m.tipo === "M");
          setMesas(mesasFiltradas);
        }
      } catch (error) {
        console.error("Error al cargar mesas:", error);
      }
    };

    if (!mesero_actual) {
      router.push("/");
      return;
    }
    try {
      setMesero_actual(JSON.parse(mesero_actual));
    } catch (error) {
      console.error("Error al obtener mesero actual:", error);
      router.push("/");
    }

    cargarMesas();
  }, []);

  const TOTAL_MESAS = mesas.length || 100;

  const generarRangos = () => {
    let secciones = Math.min(MAX_SECCIONES, Math.floor(TOTAL_MESAS / MIN_POR_SECCION));
    if (secciones === 0) secciones = 1;

    const base = Math.floor(TOTAL_MESAS / secciones);
    const extra = TOTAL_MESAS % secciones;

    const rangos = [];
    let actual = 1;

    for (let i = 0; i < secciones; i++) {
      const inicio = actual;
      const fin = actual + base - 1 + (i < extra ? 1 : 0);
      rangos.push([inicio, fin]);
      actual = fin + 1;
    }

    return rangos;
  };

  const rangos = generarRangos();

  const buscarYEntrar = async () => {
    setErrorBuscar("");
    const numero = parseInt(buscarMesa);
    if (!numero) return setErrorBuscar("Número inválido");

    try {
      const res = await fetch(`/api/mesas/${numero}`);
      if (!res.ok) return setErrorBuscar("Mesa no encontrada");

      const data = await res.json();
      if (data.status === "ok") {
        irAPedido(numero);
      } else {
        setErrorBuscar("Mesa inválida");
      }
    } catch (error) {
      setErrorBuscar("Error de conexión");
      console.error("Error al buscar mesa:", error);
    }
  };

  const irAPedido = (mesa) => router.push(`/pedido/${mesa}`);

  const mesasOrdenadas = [...mesas].sort((a, b) => a.numero - b.numero);
  const mesasFiltradas = mesasOrdenadas.filter(
    (m) => m.numero >= rango[0] && m.numero <= rango[1]
  );

  return (
    <div className={styles.container}>

      <div className={styles.name}>{mesero_actual?.me_des}</div>

      <button className={styles.logout} onClick={() => {
        Cookies.remove("mesero_actual");
        router.push("/");
      }}>
        Cerrar sesión
      </button>

      <div className={styles.mesash1}>Mesas disponibles</div>

      <div className={styles.buscarBox}>
        <input
          type="number"
          placeholder="N° de mesa"
          value={buscarMesa}
          onChange={(e) => setBuscarMesa(e.target.value)}
          className={styles.inputBuscar}
        />
        <button onClick={buscarYEntrar} className={styles.buscarBtn}>Ir</button>
      </div>
      {errorBuscar && <div className={styles.errorBuscar}>{errorBuscar}</div>}

      <div className={styles.filtros}>
        {rangos.map(([inicio, fin], idx) => (
          <button key={idx} onClick={() => setRango([inicio, fin])}>
            {inicio} - {fin}
          </button>
        ))}
        <button onClick={() => setRango([1, TOTAL_MESAS])}>Todas</button>
      </div>

      <div className={styles.grid}>
        {mesasFiltradas.map(({ numero, estado }) => (
          <div
            key={numero}
            className={`${styles.mesa} ${estado === "ocupada" || estado === "en_uso"
              ? styles.ocupada
              : styles.libre
              }`}
            onClick={() => (estado === "libre" ? irAPedido(numero) : undefined)}
          >
            <Image
              src={
                estado === "ocupada" || estado === "en_uso"
                  ? "/logo_apagado.png"
                  : "/logo_color.png"
              }
              alt={`Mesa ${numero}`}
              width={40}
              height={40}
            />
            <span>Mesa {numero}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
