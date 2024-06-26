from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
from webdriver_manager.chrome import ChromeDriverManager
import tkinter as tk
from tkinter import ttk, scrolledtext
import time
import threading
import os
import requests
import re
import json

def download_manga(manga, chapter_von, chapter_bis, log_widget, directory):

    def load_config():
        path = os.path.abspath(__file__)
        path = os.path.dirname(path)
        os.chdir(path)
        with open('config.json', 'r') as file:
            return json.load(file)
    config = load_config()

    headers = config['headers']
    main_url = config[manga][0]

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
        while ' ' in ch:
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
        if(chapter_text) == 'The Origin Of Obedience. Part 2':
            chapter_text = 'Chapter 55.5'
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
        if 'Extra' in chapter_text:
            chapter_text = f"Extra {i+1}"

        chapter_text = chapter_text.replace("Chapter ", "")

        if chapter_text == '':
            continue
        
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

def get_chapter_length(manga, url):
    def load_config():
        path = os.path.abspath(__file__)
        path = os.path.dirname(path)
        os.chdir(path)
        with open('config.json', 'r') as file:
            return json.load(file)
        
    def save_config(config):
        path = os.path.abspath(__file__)
        path = os.path.dirname(path)
        os.chdir(path)
        with open('config.json', 'w') as file:
            json.dump(config, file, indent=4)
        return

    config = load_config()

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--log-level=3") 
    chrome_options.add_experimental_option('detach', True)

    browser = Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)  
    browser.maximize_window()

    browser.get(url)
    time.sleep(3)

    accept_cookies_button = browser.find_element(By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[3]')
    accept_cookies_button.click()
    time.sleep(2)

    chapter_list = browser.find_element(By.XPATH, '//*[@id="row-content-chapter"]')
    chapters = chapter_list.find_elements(By.XPATH, './li/a')
    result = len(chapters)

    browser.quit()

    config[manga].append(result)

    save_config(config)

    
    return 

def calc_chapter_length(manga, url):
    get_chapter_length(manga, url)
    return

def start_manga_download(manga, von, bis, log_widget, directory):
    thread = threading.Thread(target=download_manga, args=(manga, von, bis, log_widget, directory))
    thread.start()
    return

