import { useEffect, useState } from "react";
import styles from "@/styles/index.module.css";
import Cookies from "js-cookie";
import { useRouter } from "next/router";
import Image from "next/image";

export default function Home() {
  const [meseros, setMeseros] = useState([]);
  const [idMesero, setIdMesero] = useState("");
  const [clave, setClave] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

  useEffect(() => {
    const perfilesGuardados = Cookies.get("meseros");
    if (perfilesGuardados) {
      setMeseros(JSON.parse(perfilesGuardados));
    }
  }, []);

  const handleLogin = async () => {
    setError("");
    const res = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ idMesero, clave }),
    });

    if (res.ok) {
      const result = await res.json();
      const nuevosMeseros = [...meseros.filter(m => m.id !== idMesero), { ...result?.mesero  }];
      Cookies.set("meseros", JSON.stringify(nuevosMeseros), { expires: 1 / 2, });
      Cookies.set("mesero_actual", JSON.stringify({ ...result?.mesero }), { expires: 1 / 2, });
      router.push("/mesas");
    } else {
      setError("Credenciales incorrectas. Verifica tu ID y clave.");
    }
  };

  const ingresarDirecto = async (perfil) => {
    setError("");
    const res = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ idMesero: perfil.me_des, clave: perfil.me_cod }),
    });

    if (res.ok) {
      const result = await res.json();
      Cookies.set("mesero_actual", JSON.stringify({ ...result?.mesero }), { expires: 1 / 2, });
      router.push("/mesas");
    } else {
      setError(`Error al iniciar sesión como ${perfil.id}`);
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.card}>
        <div className={styles.logo}>
          <Image src="/logo.png" alt="Logo" width={80} height={80} />
        </div>

        <h1 className={styles.loginH1}>Sistema de Mesas</h1>
        <p className={styles.loginp}>Inicia sesión</p>

        {error && <div className={styles.errorMessage}>{error}</div>}

        {meseros.length > 0 && (
          <div className={styles.guards}>
            {meseros.map((perfil, index) => (
              <button key={index} onClick={() => ingresarDirecto(perfil)}>
                Entrar como {perfil.me_des}
              </button>
            ))}
          </div>
        )}

        <input
          className={styles.inputLogin}
          type="text"
          placeholder="ID del mesero"
          value={idMesero}
          onChange={(e) => setIdMesero(e.target.value)}
        />
        <input
          className={styles.inputLogin}
          type="password"
          placeholder="Clave"
          value={clave}
          onChange={(e) => setClave(e.target.value)}
        />
        <button onClick={handleLogin} className={styles.loginBtn}>
          Ingresar
        </button>
      </div>
    </div>
  );
}
