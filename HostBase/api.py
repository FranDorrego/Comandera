from fastapi import FastAPI, Request, Query
from typing import Optional
import win32com.client
import pythoncom

app = FastAPI()

# Configuración
archivo_mdb = r"./sifare.mdb"
password = "mery46"


def ejecutar_sql(query: str):
    pythoncom.CoInitialize()
    try:
        conn = win32com.client.Dispatch("ADODB.Connection")
        conn.Open(
            f"Provider=Microsoft.Jet.OLEDB.4.0;Data Source={archivo_mdb};Jet OLEDB:Database Password={password};"
        )

        if query.strip().lower().startswith("select"):
            rs = conn.Execute(query)[0]
            columnas = [rs.Fields(i).Name for i in range(rs.Fields.Count)]
            resultados = []
            while not rs.EOF:
                fila = {col: rs.Fields.Item(col).Value for col in columnas}
                resultados.append(fila)
                rs.MoveNext()
            rs.Close()
            conn.Close()
            return {"status": "ok", "query": query, "res": resultados}
        else:
            conn.Execute(query)
            conn.Close()
            return {"status": "ok", "query": query, "res": "Consulta ejecutada correctamente"}
    except Exception as e:
        return {"status": "error", "query": query, "res": str(e)}


def obtener_info_tablas():
    pythoncom.CoInitialize()
    try:
        conn = win32com.client.Dispatch("ADODB.Connection")
        conn.Open(
            f"Provider=Microsoft.Jet.OLEDB.4.0;Data Source={archivo_mdb};Jet OLEDB:Database Password={password};"
        )
        catalog = win32com.client.Dispatch("ADOX.Catalog")
        catalog.ActiveConnection = conn

        tablas_info = []
        for table in catalog.Tables:
            if table.Type != "TABLE":
                continue
            nombre_tabla = table.Name
            columnas = [col.Name for col in table.Columns]

            # Obtener ejemplo de filas
            ejemplo = ejecutar_sql(f"SELECT TOP 3 * FROM [{nombre_tabla}]")
            tablas_info.append({
                "nombre": nombre_tabla,
                "columnas": columnas,
                "ejemplo": ejemplo.get("res", [])
            })

        conn.Close()
        return {"status": "ok", "query": "estructura base", "res": tablas_info}
    except Exception as e:
        return {"status": "error", "query": "estructura base", "res": str(e)}


def select_limitado(tabla, limit):
    query = f"SELECT TOP {limit} * FROM [{tabla}] ORDER BY id DESC"
    return ejecutar_sql(query)


@app.post("/api/{tabla}")
async def api_post_tabla(tabla: str, request: Request):
    data = await request.json()
    query = data.get("query", "")
    return ejecutar_sql(query)


@app.get("/api/base")
def api_get_base():
    return obtener_info_tablas()


@app.get("/api/select/{tabla}")
def api_get_select(tabla: str, limit: int = Query(100, gt=0)):
    return select_limitado(tabla, limit)
