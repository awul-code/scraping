import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs, urlencode, urlunparse
import csv

load_dotenv()

cookies = {
    "_delighted_web": os.getenv("DELIGHTED_WEB"),
    "PHPSESSID": os.getenv("PHPSESSID"),
    "REMEMBERME": os.getenv("REMEMBERME")
}

headers ={
    "User-Agent": "Mozilla/5.0"
}

url = os.getenv("INITIAL_URL")
data_path = 'data/user.csv'
response = requests.get(url, cookies=cookies, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.select('table tr')
    with open(data_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for row in rows:
            cols = [td.get_text(strip=True) for td in row.find_all('td')]
            if cols:
                writer.writerow(cols)
                print(f"✅ Data berhasil diambil dan disimpan ke {data_path}")
            else:
                print(f"❌ Gagal mengambil data. Status code: {response.status_code}")

