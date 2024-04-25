import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
from PIL import Image, ImageTk
from localconfig import config
from backend import start_manga_download

def submit_action():
    manga = dropdown.get()
    von = entry1.get()
    bis = entry2.get()
    directory = directory_entry.get()
    log_text_widget = create_log_widget()
    start_manga_download(manga, von, bis, log_text_widget, directory)

def open_directory():
    directory = filedialog.askdirectory()
    if directory:
        directory_entry.delete(0, tk.END)
        directory_entry.insert(0, directory)

def create_log_widget():
    manga = dropdown.get()
    von = entry1.get()
    bis = entry2.get()
    log_window = tk.Toplevel(root)
    log_window.title(f"Download log {manga} Chapter {von} bis Chapter {bis}")
    text_widget = scrolledtext.ScrolledText(log_window, width=80, height=20)
    text_widget.pack(pady=20, padx=20)
    return text_widget

root = tk.Tk()
root.title('MangaDownloader')
root.geometry('1000x800')

options = config['options']
dropdown = ttk.Combobox(root, values=options, state="readonly")
dropdown.pack(pady=20)
dropdown.set("Wähle einen Anime")

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
