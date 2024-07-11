import pyautogui
import customtkinter as ctk
from threading import Thread
import json
import os
import sys

reference_point = None


def fire_pit_cooker():
    print('hello')


def set_reference_point():
    global reference_point
    print("Move mouse to reference point and press 'r'.")
    root.bind('<r>', capture_reference_point)

def capture_reference_point(event):
    global reference_point
    reference_point = pyautogui.position()
    ref_point_entry.delete(0, ctk.END)
    ref_point_entry.insert(0, f"X:{reference_point.x}   Y:{reference_point.y}")
    root.unbind('<r>')  
    root.lift()  

def click_relative_to_reference(coords, clicks):
    first_coord = relative_coordinates[0]
    x, y = (reference_point.x + first_coord[0], reference_point.y + first_coord[1])
    pyautogui.click(x, y)
    
    for coord in coords:
        x, y = (reference_point[0] + coord[0], reference_point[1] + coord[1])
        for _ in range(clicks):
            pyautogui.click(x, y)

def start_clicking():
    t = Thread(target=click_relative_to_reference, args=(relative_coordinates, 1))
    t.daemon = True
    t.start()

def start_cutting():
    t = Thread(target=click_relative_to_reference, args=(tree_coordinates, 3))
    t.daemon = True
    t.start()

def start_collecting_stones():
    t = Thread(target=click_relative_to_reference, args=(stone_coordinates, 3))
    t.daemon = True
    t.start()

def start_mining_iron():
    t = Thread(target=click_relative_to_reference, args=(iron_coordinates, 3))
    t.daemon = True
    t.start()

def start_collecting_eggs():
    t = Thread(target=click_relative_to_reference, args=(egg_coordinates, 3))
    t.daemon = True
    t.start()

exe_dir = os.path.dirname(os.path.abspath(__file__))
paths = ['harvest_coordinates.json', 'tree_coordinates.json', 'stone_coordinates.json', 'iron_coordinates.json', 'eggs_coordinates.json']
coordinates = [json.load(open(os.path.join(exe_dir, path))) for path in paths]
relative_coordinates, tree_coordinates, stone_coordinates, iron_coordinates, egg_coordinates = coordinates

root = ctk.CTk()
root.title("SFL Cheater")
root.geometry('300x500')
root.attributes('-topmost', True) 

ref_label = ctk.CTkLabel(root, text="Reference Point:", font=('Arial', 20))
ref_label.pack(pady=10)
ref_point_entry = ctk.CTkEntry(root, width=200, placeholder_text="NaN", font=('Arial', 20))
ref_point_entry.pack(pady=5)

# Buttons
bg = '#55E74C'
button_params = {'font': ('Arial', 20), 'fg_color': bg, 'hover_color': '#47c93a', 'text_color': 'black', 'corner_radius': 10, 'width': 280, 'height': 40}
ref_button = ctk.CTkButton(root, text="Set Reference Point 🎯", command=set_reference_point, **button_params)
ref_button.pack(pady=10)
harvest_button = ctk.CTkButton(root, text="Harvest/Set Crops 🌻", command=start_clicking, **button_params)
harvest_button.pack(pady=10)
cut_trees_button = ctk.CTkButton(root, text="Cut Trees 🌲", command=start_cutting, **button_params)
cut_trees_button.pack(pady=10)
collect_stones_button = ctk.CTkButton(root, text="Mine Stones 🔨", command=start_collecting_stones, **button_params)
collect_stones_button.pack(pady=10)
mine_iron_button = ctk.CTkButton(root, text="Mine Iron ⛏️", command=start_mining_iron, **button_params)
mine_iron_button.pack(pady=10)
collect_eggs_button = ctk.CTkButton(root, text="Collect Eggs 🥚", command=start_collecting_eggs, **button_params)
collect_eggs_button.pack(pady=10)


root.mainloop()
