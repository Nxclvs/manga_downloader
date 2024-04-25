from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
from webdriver_manager.chrome import ChromeDriverManager
from localconfig import config
import time
import threading
import os
import pyautogui
import sys
import requests
import re

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

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--log-level=3") 
chrome_options.add_experimental_option('detach', True)

browser = Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)  
browser.maximize_window()
time.sleep(2)

browser.get('https://chapmanganelo.com/manga-er89137')
time.sleep(3)

accept_cookies_button = browser.find_element(By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[3]')
accept_cookies_button.click()
time.sleep(2)

chapter_von = input('Von Chapter: ')
chapter_bis = input('Bis Chapter: ')

result_list = []
threads = []
line_number = []


def download_chapter(result):
    if not os.path.exists(r'F:\TokyoGhoulRE\Chapter ' + result[0]):
        os.mkdir(r'F:\TokyoGhoulRE\Chapter ' + result[0])
        
    #os.chdir(r'F:\TokyoGhoulRE\Chapter ' + result[0])
    # print("Downloade Chapter {}".format(result[0]))
    ch = result [0]
    result.pop(0)

    for i in range(len(result)):
        path = r'F:\TokyoGhoulRE\Chapter ' + ch
        percentage = (i + 1) * 100/len(result)
        response = requests.get(result[i], headers=headers)
        if response.status_code == 200:
            with open(f"{path}\Bild {i+1}.png", 'wb') as file:
                file.write(response.content)
        
        #print(f"\rDownloade Chapter{ch}: {process}%", end="")
    print('Chapter {} wurde heruntergeladen'.format(ch))
    return

for i in range(int(chapter_von), int(chapter_bis) + 1):
# for i in range(2):
    result = []

    chapter_list = browser.find_element(By.XPATH, '//*[@id="row-content-chapter"]')
    chapters = chapter_list.find_elements(By.XPATH, './li/a')
    chapters.reverse()

    chapter_text = chapters[i].get_attribute('innerText')
    match = re.search(r'Chapter (\d+):', chapter_text)
    if match:
        chapter_text = match.group(1)
    else:
        pass


    if i == 0:
        chapter_text = '0'

    result.append(chapter_text)

    chapters[i].click()
    time.sleep(3)

    image_list = browser.find_element(By.XPATH, '/html/body/div[3]/div[3]')
    images = image_list.find_elements(By.XPATH, './img')

    for k in range(len(images)):
        src = images[k].get_attribute('src')
        result.append(src)    

    thread = threading.Thread(target=download_chapter, args=(result,))
    thread.start()
    threads.append(thread)
    

    browser.get('https://chapmanganelo.com/manga-er89137')
    time.sleep(3)

browser.quit()

for t in threads:
    t.join()

print('\nChapter {} bis Chapter {} wurden erfolgreich heruntergeladen'.format(chapter_von, chapter_bis))

