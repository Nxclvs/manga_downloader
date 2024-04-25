from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
from webdriver_manager.chrome import ChromeDriverManager
from localconfig import config
import time
import os
import pyautogui
import sys
import requests


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--log-level=3") 
chrome_options.add_experimental_option('detach', True)

browser = Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)  
browser.maximize_window()
time.sleep(2)

def js_click(browser, element):
    browser.execute_script("arguments[0].click();", element)


browser.get('https://chapmanganelo.com/manga-jh88927')
time.sleep(3)

accept_cookies_button = browser.find_element(By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[3]')
accept_cookies_button.click()
time.sleep(2)

chapter_von = input('Von Chapter: ')
chapter_bis = input('Bis Chapter: ')

result_list = []
for i in range(int(chapter_von), int(chapter_bis) + 1):

    result = [str(i)]

    chapter_list = browser.find_element(By.XPATH, '//*[@id="row-content-chapter"]')
    chapters = chapter_list.find_elements(By.XPATH, './li/a')
    chapters.reverse()
    chapters.pop(12)

    print("Chapter {}".format(i))
    chapters[i].click()
    time.sleep(3)

    image_list = browser.find_element(By.XPATH, '/html/body/div[3]/div[3]')
    images = image_list.find_elements(By.XPATH, './img')

    for k in range(len(images)):
        src = images[k].get_attribute('src')
        result.append(src)
        print(src)

    result_list.append(result)
    browser.get('https://chapmanganelo.com/manga-jh88927')
    time.sleep(3)

browser.quit()

headers = {
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache',
    'Referer': 'https://chapmanganato.to/',
    'Sec-Ch-Ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'image',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

for entries in result_list:

    if not os.path.exists(r'F:\FireForce\Chapter ' + entries[0]):
        os.mkdir(r'F:\FireForce\Chapter ' + entries[0])


    os.chdir(r'F:\FireForce\Chapter ' + entries[0])
    print("Downloade Chapter {}".format(entries[0]))
    entries.pop(0)

    for i in range(len(entries)):
        percentage = 100/len(entries)
        response = requests.get(entries[i], headers=headers)
        if response.status_code == 200:
            with open("Bild {}.png".format(i+1), 'wb') as file:
                file.write(response.content)
        process = round(percentage*(i+1))
        print(f"\r{process}%", end="")
    print("\n")

print("Fertig")