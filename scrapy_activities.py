from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import re
import os

def extractor(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)    
    driver.get(url)
    time.sleep(5)

    types = driver.find_elements(By.CSS_SELECTOR, "button[class*='sc-iLLODe sc-fPrdXf']")
    activitiy_types = [type.get_attribute("class") for type in types]

    name_list= []
    price_list = []
    
    for type in types:
        button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(type)
            )
        
        button.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h2.sc-emIrwa.ehqbgH"))
            ) 

        name_tags = driver.find_elements(By.CSS_SELECTOR, "h2.sc-emIrwa.ehqbgH")
        price_tags = driver.find_elements(By.CSS_SELECTOR, "div.sc-fUkmAC.gJFjUX")
        name_list.extend([name_tag.text for name_tag in name_tags])
        price_list.extend([price_tag.text for price_tag in price_tags])

        time.sleep(1)
           
    return name_list, price_list

def transformer(name_list, price_list):
    activities = []

    for name_tag, price_tag in zip(name_list, price_list): 
        name = re.sub(r"\s*\d{4}[/\-\d]*$", "", name_tag).strip()
        price_re = re.search(r"[\d,]+", price_tag)
        price = price_re.group(0).replace(",", "").strip()
        activities.append([name, price])        
    return activities


def loader(activities):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = os.path.join(current_directory, "activity.csv")

    with open(csv_file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter="\t")
        writer.writerow(["賽事名稱", "每人最低價"])
        writer.writerows(activities)
    return csv_file_path

def scrapy_activities(url):
    name_list, price_list = extractor(url)
    activities = transformer(name_list, price_list)
    csv_file_path = loader(activities)
    print(f"已將資料儲存到 {csv_file_path}")

if __name__ == "__main__":
    url = "https://asiayo.com/zh-tw/package/sport-activities"

    scrapy_activities(url)