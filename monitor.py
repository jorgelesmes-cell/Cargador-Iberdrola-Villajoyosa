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
