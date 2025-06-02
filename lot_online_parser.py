import requests
from bs4 import BeautifulSoup

REGIONS = ["Омская", "Новосибирская"]
TARGET_PURPOSES = ["СНТ", "ИЖС"]
MAX_PRICE = 3_000_000

def fetch_lot_online():
    base_url = "https://lot-online.ru"
    results = []
    headers = {"User-Agent": "Mozilla/5.0"}

    for region in REGIONS:
        page = 1
        while True:
            try:
                url = f"{base_url}/search?text=земельный+участок+{region}&category=1&page={page}"
                resp = requests.get(url, headers=headers, timeout=10)
                if resp.status_code != 200:
                    print(f"[lot-online] Ошибка HTTP {resp.status_code} на {url}")
                    break
                soup = BeautifulSoup(resp.text, "html.parser")
                lots = soup.select("div.lot-card")
                if not lots:
                    break

                for lot in lots:
                    try:
                        title = lot.select_one(".lot-card__title").text.strip()
                        link_tag = lot.select_one(".lot-card__title a")
                        url = base_url + link_tag.get("href", "")
                        price_text = lot.select_one(".lot-card__price").text.strip().split()[0]
                        price = int(price_text.replace(" ", "").replace("₽", ""))
                        purpose = "СНТ" if "снт" in title.lower() else ("ИЖС" if "ижс" in title.lower() else "")
                        if not purpose or price > MAX_PRICE:
                            continue

                        results.append({
                            "title": title,
                            "price": price,
                            "url": url,
                            "region": region + " область",
                            "purpose": purpose
                        })
                    except Exception as e:
                        print(f"[lot-online] Ошибка парсинга лота: {e}")
                        continue

                page += 1
            except Exception as e:
                print(f"[lot-online] Ошибка запроса: {e}")
                break

    return results

