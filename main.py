import json
from playwright.sync_api import sync_playwright


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        page = browser.new_page()

        def handle_response(response):
            url = response.url
            if "ajax/route/car_places" in url:
                print("\n[INFO] Поймали car_places:", url)
                try:
                    data = response.json()
                    text = json.dumps(data, ensure_ascii=False, indent=2)
                    print("[INFO] JSON:\n", text[:1000], "...\n")
                except Exception as e:
                    print("[WARN] Не удалось распарсить JSON:", e)

        page.on("response", handle_response)

        page.goto("https://pass.rw.by/ru/", wait_until="networkidle")
        print(
            "Вручную:\n"
            "  1) выбрать станцию 'Откуда', 'Куда', дату, нажать 'НАЙТИ';\n"
            "  2) на странице с поездами нажать 'ВЫБРАТЬ МЕСТА' на нужном поезде;\n"
            "  3) на странице с вагонами кликнуть по любому вагону.\n\n"
            "Как только сайт отправит запрос ajax/route/car_places, JSON появится в терминале."
        )

        page.wait_for_timeout(10 * 60 * 1000)

        browser.close()


if __name__ == "__main__":
    main()
