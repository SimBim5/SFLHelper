import pyautogui
import cv2
import numpy as np
import os

def find_goblins_on_screen(goblin_image, screenshot_gray, threshold=0.5):
    """Find all instances of goblin_image in the provided screenshot."""
    goblin_gray = cv2.cvtColor(goblin_image, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(screenshot_gray, goblin_gray, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= threshold)
    h, w = goblin_gray.shape[:2]
    goblins = []
    for pt in zip(*locations[::-1]):  # Switch x and y positions
        center_x = pt[0] + w // 2
        center_y = pt[1] + h // 2
        goblins.append((center_x + 1443, center_y + 759))
    return goblins

def process_goblins(directory_path):
    """Load goblin images, find them on the screen, and click each one three times."""
    goblin_image_paths = [os.path.join(directory_path, file) for file in os.listdir(directory_path) if file.endswith('.png')]
    
    x1, y1 = 1443, 759
    x2, y2 = 2392, 1372
    width = x2 - x1
    height = y2 - y1
    
    screenshot = pyautogui.screenshot(region=(x1, y1, width, height))
    screenshot_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    screenshot_gray = cv2.cvtColor(screenshot_gray, cv2.COLOR_BGR2GRAY)
    
    found_goblins = 0
    for goblin_image_path in goblin_image_paths:
        goblin_image = cv2.imread(goblin_image_path, cv2.IMREAD_UNCHANGED)
        if goblin_image is None:
            print(f"Failed to read the goblin image from {goblin_image_path}. Check the file path and try again.")
            continue
        
        if goblin_image.shape[2] == 4:
            goblin_image = cv2.cvtColor(goblin_image, cv2.COLOR_BGRA2BGR)

        goblins = find_goblins_on_screen(goblin_image, screenshot_gray, 0.7)
        if goblins:
            for goblin in goblins:
                print(f"Clicking three times at {goblin} for goblin image: {goblin_image_path}")
                pyautogui.moveTo(goblin)
                #pyautogui.click(goblin)
                found_goblins += 1
                if found_goblins >= 3:
                    return  # Stop after finding and clicking three goblins
    print("Less than three goblins found, or none at all.")

if __name__ == '__main__':
    directory_path = 'capture_images/goblins'  # Update to the correct directory
    process_goblins(directory_path)