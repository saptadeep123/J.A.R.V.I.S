import pyautogui
import time

print("Move your mouse to the button and note the coordinates...")
print("Press Ctrl+C to exit.")

try:
    while True:
        x, y = pyautogui.position()
        print(f"X: {x}, Y: {y}", end="\r")
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nDone.")