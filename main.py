from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import os
import requests
from fake_useragent import UserAgent


driver = webdriver.Firefox()
driver.implicitly_wait(10)
wait = WebDriverWait(driver, 500)
ua = UserAgent()


def scrapeImages(key: str) -> None:
    max_count = 1100
    numbers_of_scrolls = max_count / 300 + 1
    print(type(numbers_of_scrolls))
    url = f"https://yandex.ru/images/search?text={key}"
    driver.get(url=url)

    # скороллинг страницы
    # for x in range(int(numbers_of_scrolls)):
    #     for xx in range(10):
    #         driver.execute_script("window.scrollTo(0, 1000000)")
    #         time.sleep(2)
    #     time.sleep(10)
    #     try:
    #         print("Поиск кнопки")
    #         driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div/div[3]/a").click()
    #         print("Кнопка нажата")
    #     except:
    #         break

    time.sleep(10)

    images_small = driver.find_elements(By.CSS_SELECTOR, "img.serp-item__thumb")
    images_big = driver.find_elements(By.CSS_SELECTOR, "a.serp-item__link")

    print(len(images_big))
    print(len(images_small))

    print("-------------------------------------------")
    
    for i in range(0, max_count + 1):
        # кликаем на большую картинку
        try:
            images_big[i].click()
            time.sleep(2)
            img_element = driver.find_element(By.CSS_SELECTOR, ".MMImage-Origin")
            img_url_big = img_element.get_attribute("src")

            img_url_small = images_small[i].get_attribute("src")

            # создание имен картинок
            file_name = f"{str(i).rjust(4, '0')}.jpg"

            # Скачивание большой картинки
            img_path_big = os.path.join(f"dataset/big/{key}", file_name)
            responce_big = requests.get(img_url_big, headers={
                "User-Agent" : ua.random,
            }, verify=False)
            with open(img_path_big, "wb") as f:
                f.write(responce_big.content)

            # Закрыть окно с большим изображением
            driver.find_element(By.CSS_SELECTOR, 'div.MMViewerModal-Close').click()
            
            # Скачивание маленькой картинки
            img_path_small = os.path.join(f"dataset/small/{key}", file_name)
            response_small = requests.get(img_url_small, headers={
                "User-Agent" : ua.random,
            }, verify=False)
            with open(img_path_small, "wb") as f:
                f.write(response_small.content)
            
            print(f"Скачано изображение {i + 1}/{max_count}")
        except:
            continue

    time.sleep(10)

    driver.close()
    driver.quit()

def createFolders() -> None:
    try:
        os.makedirs("dataset", exist_ok=True)
        os.makedirs("dataset/big", exist_ok=True)
        os.makedirs("dataset/small", exist_ok=True)
        os.makedirs("dataset/big/tiger", exist_ok=True)
        os.makedirs("dataset/big/leopard", exist_ok=True)
        
        os.makedirs("dataset/small/tiger", exist_ok=True)
        os.makedirs("dataset/small/leopard", exist_ok=True)
    except:
        print("Error")


def main():
    createFolders()
    scrapeImages("tiger")


if __name__ == "__main__":
    main()