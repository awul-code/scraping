import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs, urlencode, urlunparse
import csv

load_dotenv()
# Load environment variables
cookies = {
    "_delighted_web": os.getenv("DELIGHTED_WEB"),
    "PHPSESSID": os.getenv("PHPSESSID"),
    "REMEMBERME": os.getenv("REMEMBERME"),
}

headers = {"User-Agent": "Mozilla/5.0"}

base_url = os.getenv("BASE_URL")
initial_url = os.getenv("INITIAL_URL")
data_path = "data/kunjungan.csv"


def extract_page_data(url):
    try:
        response = requests.get(url, cookies=cookies, headers=headers, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error mengakses {url}: {str(e)}")
        return [], None

    soup = BeautifulSoup(response.text, "html.parser")

    # Extracting data from the table
    rows = soup.select("table tr")
    data = []
    for row in rows:
        cols = [td.get_text(strip=True) for td in row.find_all("td")]
        if cols:
            data.append(cols)

    # Detecting the next page
    next_link = None
    pagination = soup.select_one(".pagination")

    if pagination:
        # search button "Selanjutnya" or ">"
        next_btn = pagination.select("li.page-item:not(.disabled) a.page-link")
        for btn in next_btn:
            if "Selanjutnya" in btn.text or ">" in btn.text:
                next_link = btn.get("href")
                break

        # if next button is not found try to find active page.
        if not next_link:
            last_page_btn = pagination.select_one("li.page-item.disabled a.page-link")
            if (
                last_page_btn
                and "Selanjutnya" in last_page_btn.text
                or ">" in last_page_btn.text
            ):
                print("ℹ️ Sudah mencapai halaman terakhir")
        return data, next_link


# Open CSV file for writing
with open(data_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    headers_written = False
    current_url = initial_url
    page_count = 0
    total_records = 0

    while current_url:
        page_count += 1
        print(f"📖 Mengambil halaman {page_count}: {current_url}")

        data, next_link = extract_page_data(current_url)
        if not data:
            print(f"⚠️ Tidak ditemukan data di halaman {page_count}")
            current_url = next_link if next_link else None
            continue
        # Write headers only once
        if not headers_written:
            header_row = [
                th.get_text(strip=True)
                for th in BeautifulSoup(
                    requests.get(current_url, cookies=cookies, headers=headers).text,
                    "html.parser",
                ).select("table thead th")
            ] or [f"Kolom {i+1}" for i in range(len(data[0]))]
            writer.writerow(header_row)
            headers_written = True

        # Write data
        writer.writerows(data)
        total_records += len(data)
        print(f"✅ Halaman {page_count}: {len(data)} records ditambahkan")

        # Check is there is a next page
        if next_link:
            # make sure the next link is absolute
            if not next_link.startswith("http"):
                next_link = urljoin(base_url, next_link)
            current_url = next_link
        else:
            current_url = None

    print(f"\n✨ Proses selesai!")
    print(f"• Total halaman: {page_count}")
    print(f"• Total records: {total_records}")
    print(f"• File disimpan: {data_path}")
