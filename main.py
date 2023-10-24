from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import os
import requests


headers = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0"
}

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

    
    for i in range(0, max_count + 1):
        # кликаем на большую картинку
        images_big[i].click()

        img_element = driver.find_element(By.CSS_SELECTOR, ".MMImage-Origin")
        img_url_big = img_element.get_attribute("src")

        img_url_small = images_small[i].get_attribute("src")

        # создание имен картинок
        file_name = f"{str(i).rjust(4, '0')}.jpg"

        # Скачивание большой картинки
        img_path_big = os.path.join("dataset/big", file_name)
        responce_big = requests.get(img_url_big)
        with open(img_path_big, "wb") as f:
            f.write(responce_big.content)
    
        # Закрыть окно с большим изображением
        driver.find_element(By.CSS_SELECTOR, 'div.MMViewerModal-Close').click()

    time.sleep(100)

    driver.close()
    driver.quit()

def main():

    os.makedirs("dataset", exist_ok=True)
    os.makedirs("dataset/big", exist_ok=True)
    os.makedirs("dataset/small", exist_ok=True)
    os.makedirs("dataset/big/tiger", exist_ok=True)
    os.makedirs("dataset/big/leopard", exist_ok=True)
    
    os.makedirs("dataset/small/tiger", exist_ok=True)
    os.makedirs("dataset/small/leopard", exist_ok=True)

    scrapeImages("tiger")


if __name__ == "__main__":
    main()