from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import os
import requests


driver = webdriver.Firefox()
driver.implicitly_wait(10)
wait = WebDriverWait(driver, 500)

def scrapeImages(key: str):
    max_count = 1100
    numbers_of_scrolls = max_count / 300 + 1
    print(type(numbers_of_scrolls))
    url = f"https://yandex.ru/images/search?text={key}"
    driver.get(url=url)

    downloaded_img_count = 0
    # скороллинг страницы
    for x in range(int(numbers_of_scrolls)):
        for xx in range(10):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2)
        time.sleep(5)

        try:
            driver.find_element("xpath", "/html/body/div[4]/div[2]/div/div[2]/a").click()
        except:
            break

    time.sleep(10)

    images_small = driver.find_elements(By.CSS_SELECTOR, "img.serp-item__thumb")
    images_big = driver.find_elements(By.CSS_SELECTOR, "a.serp-item__link")

    print(len(images_big))
    print(len(images_small))



    time.sleep(100)

    driver.close()
    driver.quit()

def main():

    os.makedirs("dataset", exist_ok=True)
    scrapeImages("tiger")


if __name__ == "__main__":
    main()