import requests
from bs4 import BeautifulSoup

REGIONS = ["Омская область", "Новосибирская область"]
TARGET_PURPOSES = ["СНТ", "ИЖС"]
MAX_PRICE = 3_000_000


def fetch_bankrotbaza():
    results = []
    base_url = "https://bankrotbaza.ru"
    for region in REGIONS:
        page = 1
        while True:
            url = f"{base_url}/search?what=&category=zemelnye-uchastki-bankrotov&region={region}&page={page}"
            resp = requests.get(url, timeout=10)
            if resp.status_code != 200:
                break
            soup = BeautifulSoup(resp.text, "html.parser")
            lots = soup.select(".object-item")
            if not lots:
                break
            for lot in lots:
                try:
                    title = lot.select_one(".object-title a").text.strip()
                    url = base_url + lot.select_one(".object-title a")["href"]
                    price_text = lot.select_one(".object-price").text.strip().split()[0]
                    price = int(price_text.replace(" ", ""))
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
                except Exception:
                    continue
            page += 1
    return results
