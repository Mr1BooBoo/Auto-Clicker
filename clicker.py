# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 16:02:14 2024

@author: bilal
"""

import time
import threading
from pynput.mouse import Controller, Button
from pynput.keyboard import Listener, KeyCode
import tkinter as tk

clicking = False
mouse = Controller()
click_interval = 1.0
toggle_key = "+"
stop_event = threading.Event()

def clicker():
    while not stop_event.is_set():
        if clicking:
            mouse.click(Button.left, 1)
        time.sleep(click_interval)

def toggle_event(key):
    global clicking
    if key == KeyCode(char=toggle_key):
        clicking = not clicking

def on_closing():
    global clicking, listener
    clicking = False
    stop_event.set()
    listener.stop()
    root.destroy()

def update_click_interval(val):
    global click_interval
    click_interval = 1.0 / float(val)

def update_toggle_key(val):
    global toggle_key
    toggle_key = val

click_thread = threading.Thread(target=clicker)
click_thread.daemon = True
click_thread.start()

root = tk.Tk()
root.title("Auto Clicker")
root.geometry("300x200")
root.resizable(False, False)

frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(fill="both", expand=True, padx=10, pady=10)

clicks_label = tk.Label(frame, text="Clicks per second:", bg="#f0f0f0", font=("Arial", 12))
clicks_label.pack(pady=5)

clicks_slider = tk.Scale(frame, from_=1, to=100, orient='horizontal', command=update_click_interval, bg="#f0f0f0", font=("Arial", 10))
clicks_slider.set(5)
clicks_slider.pack(pady=5)

key_label = tk.Label(frame, text="Set a custom key:", bg="#f0f0f0", font=("Arial", 12))
key_label.pack(pady=5)

key_entry = tk.Entry(frame, font=("Arial", 10))
key_entry.insert(0, toggle_key)
key_entry.pack(pady=5)

def update_key():
    update_toggle_key(key_entry.get())

update_key_button = tk.Button(frame, text="Update Key", command=update_key, font=("Arial", 10), bg="#4caf50", fg="white")
update_key_button.pack(pady=5)

root.protocol("WM_DELETE_WINDOW", on_closing)

listener = Listener(on_press=toggle_event)
listener.start()

root.mainloop()
listener.stop()
listener.join()
