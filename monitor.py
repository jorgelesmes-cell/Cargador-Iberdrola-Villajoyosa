from playwright.sync_api import sync_playwright

URL = "https://www.iberdrola.es/movilidad-electrica/productos/puntos-de-recarga"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    page = browser.new_page(
        viewport={"width": 1920, "height": 1080}
    )

    print("Abriendo mapa de Iberdrola...")

    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(10000)

    print("Titulo:", page.title())
    print("URL final:", page.url)

    page.screenshot(
        path="iberdrola.png",
        full_page=True
    )

    print("Captura guardada correctamente.")

    browser.close()
