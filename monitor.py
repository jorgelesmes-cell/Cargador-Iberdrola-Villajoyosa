import json
import urllib.request
import os

URL = (
    "https://www.iberdrola.es/o/webclipb/iberdrola/"
    "puntosrecargacontroller/getDatosPuntoRecarga"
)

payload = {
    "dto": {
        "cuprId": [5519]
    },
    "language": "es"
}

data = json.dumps(payload).encode("utf-8")

request = urllib.request.Request(
    URL,
    data=data,
    method="POST",
    headers={
        "Content-Type": "application/json; charset=UTF-8",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Origin": "https://www.iberdrola.es",
        "Referer": "https://www.iberdrola.es/movilidad-electrica/productos/puntos-de-recarga",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/140.0.0.0 Safari/537.36"
        ),
    },
)

print("Consultando directamente el punto Iberdrola...")

with urllib.request.urlopen(request, timeout=30) as response:
    texto = response.read().decode("utf-8")
    print("HTTP:", response.status)

    datos = json.loads(texto)

    with open("iberdrola.json", "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=2)

    print("Respuesta recibida correctamente.")
    print("Datos guardados en iberdrola.json")
punto = datos["entidad"][0]

conectores = punto["logicalSocket"]

libres = 0

for conector in conectores:
    estado = conector["status"]["statusCode"]
    numero = conector["physicalSocket"][0]["physicalSocketCode"]

    print(f"Toma {numero}: {estado}")

    if estado != "OCCUPIED":
        libres += 1

print(f"Conectores libres: {libres}/{len(conectores)}")
estado_actual = "LIBRE" if libres > 0 else "OCUPADO"

try:
    with open("estado_anterior.txt", "r") as archivo:
        estado_anterior = archivo.read().strip()
except FileNotFoundError:
    estado_anterior = ""

with open("estado_anterior.txt", "w") as archivo:
    archivo.write(estado_actual)

if estado_actual == "LIBRE" and estado_anterior != "LIBRE":
    print("HAY UN CARGADOR DISPONIBLE")
else:
    print("TODOS LOS CARGADORES ESTAN OCUPADOS")
import os
import requests

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

CHAT_IDS = [
    os.environ.get("TELEGRAM_CHAT_ID"),
    os.environ.get("TELEGRAM_CHAT_ID_ESPOSA"),
]

if estado_actual == "LIBRE" and estado_anterior != "LIBRE":
    mensaje = (
        "⚡ ¡HAY CARGADOR LIBRE EN IBERDROLA VILLAJOYOSA! "
        f"Libres: {libres}/{len(conectores)}"
    )

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    for chat_id in CHAT_IDS:
        if not chat_id:
            continue

        respuesta = requests.post(
            url,
            data={"chat_id": chat_id, "text": mensaje},
            timeout=15,
        )
        respuesta.raise_for_status()

    print("Avisos enviados a Telegram correctamente.")
