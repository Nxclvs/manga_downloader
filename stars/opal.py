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

chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--log-level=3") 
chrome_options.add_experimental_option('detach', True)

browser = Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)  
browser.maximize_window()

browser.get('https://www.crunchyroll.com')
time.sleep(2)