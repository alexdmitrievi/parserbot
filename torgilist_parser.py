import requests
from bs4 import BeautifulSoup

REGIONS = ["Новосибирская область", "Омская область"]
TARGET_PURPOSES = ["СНТ", "ИЖС"]
MAX_PRICE = 3_000_000

def fetch_torgilist():
    results = []
    base_url = "https://torgilist.ru"
    headers = {"User-Agent": "Mozilla/5.0"}

    for region in REGIONS:
        page = 1
        while True:
            try:
                url = f"{base_url}/poisk/zemelnye_uchastki/{region.replace(' ', '_').lower()}/{page}"
                resp = requests.get(url, headers=headers, timeout=10)
                if resp.status_code != 200:
                    print(f"[torgilist] HTTP {resp.status_code} на {url}")
                    break

                soup = BeautifulSoup(resp.text, "html.parser")
                lots = soup.select("div.view-content div.views-row")
                if not lots:
                    break

                for lot in lots:
                    try:
                        title_tag = lot.select_one(".title a")
                        title = title_tag.text.strip()
                        url = base_url + title_tag.get("href", "")

                        price_tag = lot.select_one(".field-name-field-price")
                        if not price_tag:
                            continue
                        price_text = price_tag.text.strip().split()[0]
                        price = int(price_text.replace(" ", "").replace("₽", ""))

                        purpose = "СНТ" if "снт" in title.lower() else ("ИЖС" if "ижс" in title.lower() else "")
                        if not purpose or price > MAX_PRICE:
                            continue

                        results.append({
                            "title": title,
                            "price": price,
                            "url": url,
                            "region": region,
                            "purpose": purpose
                        })
                    except Exception as e:
                        print(f"[torgilist] Ошибка парсинга лота: {e}")
                        continue

                page += 1
            except Exception as e:
                print(f"[torgilist] Ошибка запроса: {e}")
                break

    return results
