# Web Scraper for Authenticated Website
## 📌 Description
This Python script scrapes all customer data from an authenticated website and exports it to a CSV file. The script handles pagination and maintains login session using cookies.
## 🛠️ Prerequisites
```bash
Python 3.8+
Required Python packages (install via pip install -r requirements.txt)
```
## ⚙️ Setup
### 1. Environment Configuration
Create a .env file in the project root with the following variables:
#### Authentication Cookies
```bash
DELIGHTED_WEB="{\"your_cookie_value_here\"}"
PHPSESSID="your_php_session_id"
REMEMBERME="your_remember_me_token"
```
#### Website Configuration
```bash
BASE_URL="your base_url"
INITIAL_URL="your initial url
```
### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
## 🚀 Usage
Run the scraper:
```bash    
python scrapping_all.py (get data all page)
python scrapping.py (get data one page)
```

# The script will
1. Authenticate using cookies from .env
2. Scrape all paginated customer data
3. Save results to data/customers.csv

# 📂 Output
1. CSV file containing all scraped custiomer data
2. Column Automatically detected from table headers
3. Location: data/customers.csv

# 🔧 Customization
To modify what data is scrapped:
1. Adjust the table selectors in extra_page_data() function
2. Modify the csv header in writing section

# ⚠️ Important Notes
1. Legal Compliance: Ensure you have permission to scrape this data
2. Rate Limiting: Add delays between requests if needed
3. Session Management: Cookies will expire - update .env as needed
4. Error Handling: The script includes basic error handling
    
# 📜 License
This project is for educational purposes only. Use responsibly and in compliance with the website's Terms of Service.

    