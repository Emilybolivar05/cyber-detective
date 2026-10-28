def fuerza_bruta(tabla):
    # IPs con 5 o más intentos fallidos
    solo_fallidos = tabla[tabla["status"] == "failed"]
    conteo = solo_fallidos["ip"].value_counts()
    return conteo[conteo >= 5]

def multiples_fallos(tabla):
    # Usuarios con 4 o más intentos fallidos
    solo_fallidos = tabla[tabla["status"] == "failed"]
    conteo = solo_fallidos["user"].value_counts()
    return conteo[conteo >= 4]

def horario_inusual(tabla):
    # Logins antes de las 6 de la mañana
    return tabla[tabla["hour"] < 6]

def ip_sospechosa(tabla):
    # IPs con 3 o más usuarios distintos
    usuarios_por_ip = tabla.groupby("ip")["user"].nunique()
    return usuarios_por_ip[usuarios_por_ip >= 3]

def impossible_travel(tabla):
    # Usuarios con actividad en 2 o más países
    paises = tabla.groupby("user")["country"].nunique()
    return paises[paises >= 2]