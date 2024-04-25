from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
from webdriver_manager.chrome import ChromeDriverManager
import tkinter as tk
from tkinter import ttk, scrolledtext
from localconfig import config
import time
import threading
import os
import requests
import re
def download_manga(manga, chapter_von, chapter_bis, log_widget, directory):
    headers = config['headers']
    main_url = config[manga]

    def log_message(message):
        if log_widget:
            log_widget.insert(tk.END, message + "\n")
            log_widget.see(tk.END)

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--log-level=3") 
    chrome_options.add_experimental_option('detach', True)

    browser = Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)  
    browser.maximize_window()

    browser.get(main_url)
    time.sleep(3)

    accept_cookies_button = browser.find_element(By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[3]')
    accept_cookies_button.click()
    time.sleep(2)

    threads = []

    def download_chapter(result):
        if not os.path.exists(directory + manga + r'/Chapter ' + result[0]):
            os.makedirs(directory + manga + r'/Chapter ' + result[0])
            

        ch = result [0]
        result.pop(0)
        
        ch = ch.replace(' ', '')
        for i in range(len(result)):
            path = directory + manga + r'/Chapter ' + ch
            response = requests.get(result[i], headers=headers)
            if response.status_code == 200:
                with open(f"{path}\Bild {i+1}.png", 'wb') as file:
                    file.write(response.content)
        
        log_message('Chapter {} wurde heruntergeladen'.format(ch))
        return

    for i in range(int(chapter_von) - 1, int(chapter_bis)):
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
        if ':' in chapter_text:
            chapter_text = chapter_text.split(':')[0]
        if 'Vol.' in chapter_text:
            clean_text = re.sub(r'Vol\.\d+\s+', '', chapter_text)
            chapter_text = clean_text

        chapter_text = chapter_text.replace("Chapter ", "")
        result.append(chapter_text)

        chapters[i].click()
        time.sleep(3)
        try:
            image_list = browser.find_element(By.XPATH, '/html/body/div[3]/div[3]')
        except:
            image_list = browser.find_element(By.XPATH, '/html/body/div[2]/div[3]')

        images = image_list.find_elements(By.XPATH, './img')

        for k in range(len(images)):
            src = images[k].get_attribute('src')
            result.append(src)    

        thread = threading.Thread(target=download_chapter, args=(result,))
        thread.start()
        threads.append(thread)
        

        browser.get(main_url)
        time.sleep(3)

    browser.quit()

    for t in threads:
        t.join()

    log_message('Chapter {} bis Chapter {} wurden erfolgreich heruntergeladen'.format(chapter_von, chapter_bis))

    return

def start_manga_download(manga, von, bis, log_widget, directory):
    thread = threading.Thread(target=download_manga, args=(manga, von, bis, log_widget, directory))
    thread.start()
    return

