from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
from webdriver_manager.chrome import ChromeDriverManager
from localconfig import config
import time
import os
import pyautogui
import requests


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--log-level=3") 
chrome_options.add_experimental_option('detach', True)

browser = Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)  
browser.maximize_window()
time.sleep(2)

print('Navigiere zur Seite')
browser.get('https://ww10.readonepiece.com/manga/one-piece-digital-colored-comics/')
time.sleep(2)

agree_cookies_btn = browser.find_element(By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]')
agree_cookies_btn.click()
time.sleep(2)

chapter_von = input('Von Chapter: ')
chapter_bis = input('Bis Chapter: ')

result_list = []

for i in range(int(chapter_von) - 1, int(chapter_bis)):
    result = [str(i+1)]

    chapter_list = browser.find_element(By.XPATH, '/html/body/div[7]/div/div/div[2]')
    chapters = chapter_list.find_elements(By.XPATH, './*')
    chapters.reverse()

    print("Chapter {}".format(i+1))
    chapter_button = chapters[i].find_element(By.XPATH, './div/div[2]/div/a')
    chapter_button.click()
    time.sleep(3)

    image_list = browser.find_element(By.XPATH, '//*[@id="top"]/div[3]/div[1]')
    images = image_list.find_elements(By.XPATH, './child::*[img]')

    for k in range(len(images)):
        image = images[k].find_element(By.XPATH, './img')
        src = image.get_attribute('src')
        result.append(src)
        print(src)

    result_list.append(result)
    browser.get('https://ww10.readonepiece.com/manga/one-piece-digital-colored-comics/')
    time.sleep(3)

browser.quit()

for entries in result_list:

    if not os.path.exists(r'F:\OnePiece\Chapter ' + entries[0]):
        os.mkdir(r'F:\OnePiece\Chapter ' + entries[0])

    os.chdir(r'F:\OnePiece\Chapter ' + entries[0])
    print("Downloade Chapter {}".format(entries[0]))
    entries.pop(0)
    for i in range(len(entries)):
        percentage = 100/len(entries)
        response = requests.get(entries[i])
        if response.status_code == 200:
            with open("Bild {}.png".format(i+1), 'wb') as file:
                file.write(response.content)
        process = round(percentage*(i+1))      
        print(f"\r{process}%", end="")
    print("\n")  

print("Fertig")