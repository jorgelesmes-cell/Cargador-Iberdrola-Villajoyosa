import json
import urllib.request

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

if libres > 0:
    print("HAY UN CARGADOR DISPONIBLE")
else:
    print("TODOS LOS CARGADORES ESTAN OCUPADOS")
import os
import requests

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

if libres > 0:
    mensaje = f"⚡ ¡HAY CARGADOR LIBRE EN IBERDROLA VILLAJOYOSA! Libres: {libres}/{len(conectores)}"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    respuesta = requests.post(
        url,
        data={"chat_id": CHAT_ID, "text": mensaje},
        timeout=15
    )
    respuesta.raise_for_status()
    print("Aviso enviado a Telegram correctamente.")
print("PRUEBA TELEGRAM")
requests.post(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    data={"chat_id": CHAT_ID, "text": "✅ Prueba correcta: el bot de Iberdrola puede enviarte mensajes."},
    timeout=15
).raise_for_status()
