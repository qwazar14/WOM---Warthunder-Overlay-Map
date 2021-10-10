#PYTHON VERSION 3.9.7
import pygame
import sys
import os
# import Tkinter as tk
import socket
import requests
import json
import win32api
import win32con
import win32gui
from io import BytesIO
from PIL import Image


W = 435
H = 435
IP_ADDRESS = socket.gethostbyname(socket.gethostname())
URL_MAP_IMG = 'http://{}:8111/map.img'.format(IP_ADDRESS)
URL_MAP_OBJ = 'http://{}:8111/map_obj.json'.format(IP_ADDRESS)
URL_MAP_INFO = 'http://{}:8111/map_info.json'.format(IP_ADDRESS)


def Get_Game_Window():
    hwnd = win32gui.FindWindow(None, "War Thunder - В бою")
    windowrect = win32gui.GetWindowRect(hwnd)
    x = windowrect[0] - 5  # -5 so it lines up perfectly
    y = windowrect[1]
    width = windowrect[2] - x
    height = windowrect[3] - y
    return x, y, width, height


def Get_Map_Image():
    response = requests.get(URL_MAP_IMG)
    img = Image.open(BytesIO(response.content))
    img = img.resize((W, H), Image.ANTIALIAS)
    # img.show()
    img.save("temp_map.png")


pygame.init()
pygame.display.set_caption('')

# Get_Game_Window()
sc = pygame.display.set_mode((W, H))
sc.fill((255, 0, 128))

# screen = pygame.display.set_mode(
#     (Get_Game_Window()[1], Get_Game_Window()[2]), pygame.NOFRAME)

screen = pygame.display.set_mode((H, W), pygame.NOFRAME)

hwnd = pygame.display.get_wm_info()["window"]
# hwnd = win32gui.SetWindowPos(pygame.display.get_wm_info()[
#                              "window"], -1, 0, 0, 0, 0, 0x000)
# hwnd = win32gui.SetWindowPos(
#     hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
fuchsia = (255, 0, 128)

win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
win32gui.SetLayeredWindowAttributes(
    hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)
win32gui.SetWindowPos(pygame.display.get_wm_info()['window'], -1, 1485, 650, 0, 0, 0x0001)

#data = json.loads(URL_MAP_OBJ)
# print(data)
Get_Map_Image()
image_loader = pygame.image.load("temp_map.png")
os.remove("temp_map.png")
image_shower = image_loader.get_rect(
    bottomright=(W, H))
sc.blit(image_loader, image_shower)

pygame.display.update()

while 1:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()

    pygame.time.delay(20)
