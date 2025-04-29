from flask import Flask
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time

app = Flask(__name__)

@app.route('/api/news')
def crawl_news():
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = uc.Chrome(options=options)

    try:
        driver.get("https://pokemongo.com/news?hl=ko")
        time.sleep(2)
        items = driver.find_elements(By.CSS_SELECTOR, "div.NewsList-content-block a")

        result = ""
        for item in items[:5]:
            title = item.text.strip()
            link = item.get_attribute("href")
            result += f"<b>{title}</b><br><a href='{link}'>{link}</a><br><br>"

        return result

    finally:
        driver.quit()
