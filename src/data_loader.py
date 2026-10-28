import pandas as pd

def cargar_datos(ruta):
    tabla = pd.read_csv(ruta)
    tabla["timestamp"] = pd.to_datetime(tabla["timestamp"])
    tabla["hour"] = tabla["timestamp"].dt.hour
    return tabla