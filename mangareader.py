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


os.chdir(config['image_path'])
accept_cookies_xpath = '//*[@id="st-cmp-v2"]/div/div[2]/div/div[4]/div[2]/div[1]/span/div'
search_bar_xpath = '//*[@id="search-home-form"]/input'



chrome_options = Options()
chrome_options.add_experimental_option('detach', True)

browser = Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)  
browser.maximize_window()
time.sleep(2)
# #  manga = pyautogui.prompt(title='Manga')
# manga = 'Boruto'
# def cookie_bypass(browser):
#     pyautogui.moveTo(960, 640)
#     pyautogui.click()
#     time.sleep(2)

#     main_window = browser.current_window_handle
#     handles = browser.window_handles
#     for handle in handles:
#         if handle != main_window:
#             browser.switch_to.window(handle)
#             browser.close()
#             browser.switch_to.window(main_window)
#     time.sleep(2)

def js_click(browser, element):
    browser.execute_script("arguments[0].click();", element)

# main_url = "https://mangareader.to/search?keyword={}".format(manga)
# browser.get(main_url)
# time.sleep(2)

# while True:
#     try:
#         button = browser.find_element('xpath', '//*[@id="st-cmp-v2"]/div/div[2]/div/div[4]/div[2]/div[1]/span/div')
#         time.sleep(2)
#         js_click(browser, button)
#         break
#     except:
#         cookie_bypass(browser)
    

# manga_list = browser.find_element('xpath', '//*[@id="main-content"]/section/div[2]/div[1]')
# manga_list = manga_list.find_elements(By.XPATH, './*')
# for i in range(2):
#     manga_list.pop(-1)

# title = manga_list[0].find_element(By.XPATH, './div[1]/h3')
# title_coords = title.location
# pyautogui.moveTo(title_coords['x'], title_coords['y'])

# time.sleep(2)
# while True:
#     js_click(browser, title)
#     if main_url != browser.current_url:
#         break
#     time.sleep(2)

# time.sleep(2)
for k in range(20):
    chapter_url = 'https://mangareader.to/read/kagurabachi-67139/en/chapter-{}'.format(k+1)
    chapter_number = k+1
    time.sleep(1)

    browser.get(chapter_url)
    time.sleep(1)
    if k == 0:
        button = browser.find_element('xpath', '//*[@id="st-cmp-v2"]/div/div[2]/div/div[4]/div[2]/div[1]/span/div')
        time.sleep(2)
        js_click(browser, button)
        time.sleep(1)
        pyautogui.moveTo(960, 640)
        time.sleep(2)
        pyautogui.click()
        while True:
            if len(browser.window_handles) != 1:
                browser.switch_to.window(browser.window_handles[-1])
                time.sleep(1)
                browser.close()
                time.sleep(1)
                browser.switch_to.window(browser.window_handles[0])
                time.sleep(1)
                pyautogui.click()
            else:
                break
    os.chdir(r'C:\Users\nicla\Pictures\Kagurabachi\Chapter ' + str(chapter_number))
    print(os.getcwd())
    time.sleep(3)

    image_container = browser.find_element(By.XPATH, '//*[@id="vertical-content"]')
    images = image_container.find_elements(By.XPATH, './*')

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    src_list = []
    for i in range(len(images)):
        src = images[i].get_attribute('data-url')
        src_list.append(src)
        print(src)
        print(os.getcwd())
        
        response = requests.get(src, headers=headers)
        if response.status_code == 200:
            with open("Bild {}.jpg".format(i), 'wb') as file:
                file.write(response.content)
                time.sleep(2)
        # with open ("list.txt", "w") as file:
        #     file.write(str(src_list))
    continue
time.sleep(1)
