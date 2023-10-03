import requests
from bs4 import BeautifulSoup
import os
from fake_useragent import UserAgent
import time

def get_proxy(filename : str) -> []:
    file = open(filename, "r", encoding="utf-8")
    proxy = [line.strip() for line in file]
    return proxy

def downloadImage(text: str, proxy: []) -> set:
    ua = UserAgent()
    arr = set()
    max_count = 1100  # Минимально количество изображений для загрузки
    main_url = "https://yandex.ru/images/search?text=" + text + "&p="
    for a in range(1, 100 + 1):   # На одной странице 30 картинок, поэтому должно хватить :D
        print(main_url + str(a))
        result = requests.get(main_url + str(a), headers=
                            {
                                "User-Agent" : str(ua.random)
                            },
                            proxies={
                                "http" : "http://" + proxy[a - 1]
                            })
            
        soup = BeautifulSoup(result.content, "lxml")
        links = soup.findAll("img", class_ = "serp-item__thumb justifier__thumb")
        print(links)
        for link in links:
            link = link.get("src")
            print(link)
            arr.add(link)

        if len(arr) > max_count:
            break
        time.sleep(5)
    return arr


def main():
    arr = ["tiger_big", "leopard_big", "tiger_small", "leopard_small"]
    downloadImage(arr[0], get_proxy("proxy.txt"))

if __name__ == "__main__":
    main()