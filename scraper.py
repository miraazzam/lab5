import time
import csv
from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://www.ebay.com/globaldeals/tech"

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(url)

wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.dne-itemtile-detail")))

while True:
    last_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    try:
        wait.until(lambda d: d.execute_script("return document.body.scrollHeight") > last_height)
    except:
        break

products = driver.find_elements(By.CSS_SELECTOR, "div.dne-itemtile-detail")
data = []

for product in products:
    try:
        title = product.find_element(By.CSS_SELECTOR, "span.dne-itemtile-title").text
    except:
        title = "N/A"

    try:
        price = product.find_element(By.CSS_SELECTOR, "span.first").text
    except:
        price = "N/A"

    try:
        original_price = product.find_element(By.CSS_SELECTOR, "span.itemtile-price-strikethrough").text
    except:
        original_price = "N/A"

    try:
        shipping = product.find_element(By.CSS_SELECTOR, "span.dne-itemtile-delivery").text
    except:
        shipping = "N/A"

    try:
        item_url = product.find_element(By.TAG_NAME, "a").get_attribute("href")
    except:
        item_url = "N/A"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data.append([timestamp, title, price, original_price, shipping, item_url])

driver.quit()






file_name = "ebay_tech_deals.csv"
columns = ["timestamp", "title", "price", "original_price", "shipping", "item_url"]

try:
    existing = pd.read_csv(file_name)
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(file_name, mode="a", header=False, index=False)

except FileNotFoundError:
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(file_name, index=False)

