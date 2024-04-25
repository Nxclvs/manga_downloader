import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
from PIL import Image, ImageTk
from backend import start_manga_download
import json
import os

def load_config():
    path = os.path.abspath(__file__)
    path = os.path.dirname(path)
    os.chdir(path)
    with open('config.json', 'r') as file:
        return json.load(file)
    
def save_config(config):
    os.chdir(r'C:\Users\nicla\Desktop\Dev\Python\Automation\manga_downloader\advanced')
    with open('config.json', 'w') as file:
        json.dump(config, file, indent=4)

        return

config = load_config()
name_entry = None
ulr_entry = None
add_window = None

def submit_action():
    manga = dropdown.get()
    von = entry1.get()
    bis = entry2.get()

    directory = directory_entry.get()
    log_text_widget = create_log_widget()
    start_manga_download(manga, von, bis, log_text_widget, directory)

    return

def open_directory():
    directory = filedialog.askdirectory()
    if directory:
        directory_entry.delete(0, tk.END)
        directory_entry.insert(0, directory)

    return

def create_log_widget():
    manga = dropdown.get()
    von = entry1.get()
    bis = entry2.get()

    log_window = tk.Toplevel(root)
    log_window.title(f"Download log {manga} Chapter {von} bis Chapter {bis}")
    text_widget = scrolledtext.ScrolledText(log_window, width=80, height=20)
    text_widget.pack(pady=20, padx=20)
    
    return text_widget

def add_manga():
    global add_window
    add_window = tk.Toplevel(root)
    add_window.title('Füge einen neuen Manga hinzu')
    add_window.geometry('550x300')

    content_frame = ttk.Frame(add_window)
    content_frame.pack(pady=10)

    global name_entry, url_entry
    name_label = ttk.Label(content_frame, text='Name')
    url_label = ttk.Label(content_frame, text='url')
    name_label.grid(row=0, column=0, padx=5, pady=10)
    url_label.grid(row=1, column=0, padx=5, pady=10)

    name_entry = ttk.Entry(content_frame, width=65)
    url_entry = ttk.Entry(content_frame, width=80)
    name_entry.grid(row=0, column=1)
    url_entry.grid(row=1, column=1)

    add_button = ttk.Button(add_window, text='Hinzufügen', command=add_maga_to_config)
    add_button.pack(pady=10)

def add_maga_to_config():
    global name_entry, url_entry
    name = name_entry.get()
    url = url_entry.get()

    config[name] = url
    config['options'].append(name)
    save_config(config)

    dropdown['values'] = config['options']
    add_window.destroy()
    print(name)
    print(url)



root = tk.Tk()
root.title('MangaDownloader')
root.geometry('1000x800')

options = config['options']

choose_frame = ttk.Frame(root)
choose_frame.pack(pady=10)

dropdown = ttk.Combobox(choose_frame, values=options, state="readonly")
dropdown.grid(row=0, column=0)
dropdown.set("Wähle einen Anime")

add_manga_button = ttk.Button(choose_frame, text='Hinzufügen', command=add_manga)
add_manga_button.grid(row=0 ,column=1, padx=10)

directory_frame = ttk.Frame(root)
directory_frame.pack(pady=10)

directory_entry = ttk.Entry(directory_frame, width=80)
directory_entry.grid(row=0, column=0, padx=5, pady=10, sticky=tk.W)

browse_button = ttk.Button(directory_frame, text="Durchsuchen", command=open_directory)
browse_button.grid(row=0, column=1, padx=5, pady=10)

input_frame = ttk.Frame(root)
input_frame.pack(pady=10)

label1 = ttk.Label(input_frame, text="Von Chapter: ")
label1.grid(row=0, column=0, padx=5, sticky=tk.W)

entry1 = ttk.Entry(input_frame, width=30)
entry1.grid(row=1, column=0, padx=5)

label2 = ttk.Label(input_frame, text="Bis Chapter: ")
label2.grid(row=0, column=1, padx=5, sticky=tk.W)

entry2 = ttk.Entry(input_frame, width=30)
entry2.grid(row=1, column=1, padx=5)

button = ttk.Button(root, text="Start", command=submit_action)
button.pack(pady=20)

root.mainloop()
