import pyautogui
import cv2
import numpy as np
import os

def find_chest_on_screen(chest_image):
    x1, y1 = 1443, 759
    x2, y2 = 2392, 1372
    width = x2 - x1
    height = y2 - y1
    
    screenshot = pyautogui.screenshot(region=(x1, y1, width, height))
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    
    chest_gray = cv2.cvtColor(chest_image, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(screenshot_gray, chest_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val > 0.7:
        h, w = chest_gray.shape[:2]
        center_x = max_loc[0] + w // 2
        center_y = max_loc[1] + h // 2
        return (center_x+x1, center_y+y1)
    return None

def click_chest_center(directory_path):
    chest_image_paths = [os.path.join(directory_path, file) for file in os.listdir(directory_path) if file.endswith('.png')]
    
    for chest_image_path in chest_image_paths:
        chest_image = cv2.imread(chest_image_path, cv2.IMREAD_UNCHANGED)
        if chest_image is None:
            print(f"Failed to read the chest image from {chest_image_path}. Check the file path and try again.")
            continue

        if chest_image.shape[2] == 4:
            chest_image = cv2.cvtColor(chest_image, cv2.COLOR_BGRA2BGR)

        center_position = find_chest_on_screen(chest_image)
        if center_position:
            print(f"Clicking at {center_position} for chest image: {chest_image_path}")
            pyautogui.moveTo(center_position)  # Move to the position for demonstration
            return  # Exit function after finding the first chest
    print("No chest found.")

    
directory_path = 'capture_images/chests'
click_chest_center(directory_path)