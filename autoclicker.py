import pyautogui
import cv2
import numpy as np
import time
import threading
import keyboard

# Otomatik tıklamanın aktif olup olmadığını belirleyen bayrak
clicking = False

# Yeşil rengin geniş HSV değer aralığını belirleyin
lower_green = np.array([30, 40, 40])
upper_green = np.array([90, 255, 255])

# Ekran görüntüsü alıp yeşil renkli nesneleri tespit eden işlev
def find_and_click_green(region, threshold=0.8):
    screen = pyautogui.screenshot(imageFilename="ss.png",region=region)
    screen_np = np.array(screen)
    screen_hsv = cv2.cvtColor(screen_np, cv2.COLOR_RGB2HSV)
    
    mask = cv2.inRange(screen_hsv, lower_green, upper_green)
    mask = cv2.erode(mask, None, iterations=3)
    mask = cv2.dilate(mask, None, iterations=3)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        if cv2.contourArea(contour) > 200:  # Kontur alanı filtresi (gereksiz küçük konturları yok sayar)
            x, y, w, h = cv2.boundingRect(contour)
            pyautogui.click(region[0] + x + w // 2, region[1] + y + h // 2)
            return True
    return False

# Otomatik tıklama işlevi
def clicker():
    global clicking
    region = (0, 300, 500, 500)  # Ekranın belirli bir bölgesini yakala
    while True:
        if clicking:
            if find_and_click_green(region):
                print("Yeşil nesne bulundu ve tıklandı.")
            else:
                print("Hiçbir hedef bulunamadı.")
        time.sleep(0.002)  # Tıklama aralığı

# Başlatmak ve durdurmak için klavye dinleyicisi
def keyboard_listener():
    global clicking
    while True:
        if keyboard.is_pressed('s'):  # 's' tuşuna basıldığında başlat
            clicking = True
        elif keyboard.is_pressed('d'):  # 'd' tuşuna basıldığında durdur
            clicking = False
        time.sleep(0.1)

# Thread'leri başlat
click_thread = threading.Thread(target=clicker)
keyboard_thread = threading.Thread(target=keyboard_listener)

click_thread.start()
keyboard_thread.start()
