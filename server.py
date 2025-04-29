from flask import Flask
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

app = Flask(__name__)

@app.route('/api/news')
def crawl_news():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get("https://pokemongo.com/news?hl=ko")
        time.sleep(2)

        items = driver.find_elements(By.CSS_SELECTOR, "div.NewsList-content-block a")
        result = ""
        for item in items[:5]:
            title = item.text
            link = item.get_attribute("href")
            result += f"<b>{title}</b><br><a href='{link}'>{link}</a><br><br>"

        return result
    finally:
        driver.quit()
