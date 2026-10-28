def nivel_de_riesgo(score):
    if score >= 80:
        return "Critical"
    elif score >= 60:
        return "High"
    elif score >= 30:
        return "Medium"
    else:
        return "Low"

def score_usuario(nombre, usuarios_sospechosos, usuarios_viajeros, madrugada):
    score = 0
    if nombre in usuarios_sospechosos.index:
        score = score + 10
    if nombre in usuarios_viajeros.index:
        score = score + 25
    if nombre in madrugada["user"].unique():
        score = score + 10
    return score

def score_ip(direccion, sospechosas, ips_sospechosas):
    score = 0
    if direccion in sospechosas.index:
        score = score + 40
    if direccion in ips_sospechosas.index:
        score = score + 30
    return score