import plotly.express as px
import pandas as pd
import streamlit as st
from src.data_loader import cargar_datos
from src.threat_detector import fuerza_bruta, multiples_fallos, horario_inusual, ip_sospechosa, impossible_travel
from src.risk_score import nivel_de_riesgo, score_usuario, score_ip

st.set_page_config(page_title="Cyber Detective", layout="wide")

# Estilo oscuro para todos los gráficos de Plotly
px.defaults.template = "plotly_dark"
px.defaults.color_discrete_sequence = ["#00d4aa"]

# Título de la página
st.title("Cyber Detective - Security Log Analyzer")

# Cargar los datos
tabla = cargar_datos("data/security_logs.csv")
solo_fallidos = tabla[tabla["status"] == "failed"]

# ---------- Las 5 reglas de detección ----------
conteo_ips = solo_fallidos["ip"].value_counts()
conteo_usuarios = solo_fallidos["user"].value_counts()

sospechosas = fuerza_bruta(tabla)
usuarios_sospechosos = multiples_fallos(tabla)
madrugada = horario_inusual(tabla)
ips_sospechosas = ip_sospechosa(tabla)
usuarios_viajeros = impossible_travel(tabla)

# Cuántos marcó cada regla
cantidades = [len(sospechosas), len(usuarios_sospechosos), len(madrugada["user"].unique()), len(ips_sospechosas), len(usuarios_viajeros)]

# ---------- Tarjetas de métricas ----------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total events", len(tabla))
col2.metric("Failed logins", len(solo_fallidos))
col3.metric("Suspicious IPs", len(sospechosas))
col4.metric("Threats detected", sum(cantidades))

# ---------- Alertas ----------
for ip in sospechosas.index:
    st.error(f"ALERT: possible brute force attack from IP {ip}")

# ---------- Gráficos ----------
graf1, graf2 = st.columns(2)

conteo = tabla["status"].value_counts()
fig = px.bar(x=conteo.index, y=conteo.values, title="Failed vs Successful Logins")
graf1.plotly_chart(fig)

nombres = ["Brute Force", "Multiple Failed Logins", "Unusual Login Time", "Suspicious IP", "Impossible Travel"]
fig2 = px.bar(x=cantidades, y=nombres, orientation="h", title="Threat Distribution")
graf2.plotly_chart(fig2)

fig3 = px.bar(x=conteo_ips.values, y=conteo_ips.index, orientation="h", title="Top Suspicious IPs")
st.plotly_chart(fig3)

graf3, graf4 = st.columns(2)

por_pais = tabla["country"].value_counts()
fig4 = px.bar(x=por_pais.values, y=por_pais.index, orientation="h", title="Activity by Country")
graf3.plotly_chart(fig4)

tabla["hora_exacta"] = tabla["timestamp"].dt.floor("h")
por_tiempo = tabla["hora_exacta"].value_counts().sort_index()
fig5 = px.line(x=por_tiempo.index, y=por_tiempo.values, markers=True, title="Activity Over Time")
graf4.plotly_chart(fig5)

# ---------- Event Logs ----------
st.header("Event Logs")

opcion = st.selectbox("Filter by status", ["all", "failed", "success"])

if opcion == "all":
    st.dataframe(tabla)
else:
    st.dataframe(tabla[tabla["status"] == opcion])

# ---------- Threat Detection ----------
st.header("Threat Detection")

amenazas = []

for ip in sospechosas.index:
    amenazas.append(["Brute Force", "High", ip, "5 o más intentos fallidos desde la misma IP"])

for ip in ips_sospechosas.index:
    amenazas.append(["Suspicious IP", "High", ip, "3 o más usuarios distintos desde la misma IP"])

for usuario in usuarios_sospechosos.index:
    amenazas.append(["Multiple Failed Logins", "Medium", usuario, "4 o más intentos fallidos de un mismo usuario"])

for usuario in usuarios_viajeros.index:
    amenazas.append(["Impossible Travel", "Medium", usuario, "Actividad desde 2 o más países"])

for usuario in madrugada["user"].unique():
    amenazas.append(["Unusual Login Time", "Low", usuario, "Login antes de las 6 de la mañana"])

tabla_amenazas = pd.DataFrame(amenazas, columns=["threat", "severity", "ip_or_user", "explanation"])
st.dataframe(tabla_amenazas)

# ---------- Risk Score ----------
st.header("Risk Score")

# Score de cada usuario
filas_usuarios = []
for usuario in tabla["user"].unique():
    score = score_usuario(usuario, usuarios_sospechosos, usuarios_viajeros, madrugada)
    filas_usuarios.append([usuario, score, nivel_de_riesgo(score)])

tabla_usuarios = pd.DataFrame(filas_usuarios, columns=["user", "score", "level"])
st.subheader("By user")
st.dataframe(tabla_usuarios)

# Score de cada IP
filas_ips = []
for ip in tabla["ip"].unique():
    score = score_ip(ip, sospechosas, ips_sospechosas)
    filas_ips.append([ip, score, nivel_de_riesgo(score)])

tabla_ips = pd.DataFrame(filas_ips, columns=["ip", "score", "level"])
st.subheader("By IP")
st.dataframe(tabla_ips)