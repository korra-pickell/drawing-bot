import numpy as np
from PIL import Image, ImageFilter
import win32api, win32con
import os, time, keyboard, sys, random
import pyautogui as pog
import time

# The commented out section on line 9 returns the filename for the first file in a subfolder named 'img_to_draw'
img_to_draw_path = '' # os.path.join(os.path.dirname(os.path.realpath(__file__)),'img_to_draw',os.listdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'img_to_draw'))[0])
bbox = {'top':150,'left':450,'width':900,'height':900} # Specify the canvas area on screen
IMG_DIM = 500 # Specify the HxW target dimensions for the image


def get_lines(arr):
    """ Returns an array of line segments """

    lines = []
    on_line = False
    starting_line_index = 0
    for r,row in enumerate(arr):
        for index,value in enumerate(row):
            if value == False and on_line == False: # If you are at the start of a line
                on_line = True
                starting_line_index = index
            elif value == True and on_line == True: # If you are at the end of a line
                on_line = False
                lines.append((r,starting_line_index,index-1))
    return lines

def process_img_full_lines(path):
    """ Opens Image, resizes it, converts it to grayscale, only takes values greater 
    than the average, and computes the lines needed to draw the image"""

    img = Image.open(path)
    
    img = img.resize((IMG_DIM,IMG_DIM)).convert('L')

    img_arr = np.array(img) > np.average(img)

    lines = get_lines(img_arr)

    return lines

def draw_line(y,x1,x2):
    win32api.SetCursorPos((x1,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    win32api.SetCursorPos((x2,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)


startTime = time.time()

lines = process_img_full_lines(img_to_draw_path)

for line in lines:
    draw_spot_x1 = int((line[1]/IMG_DIM)*bbox['width']+bbox['left'])
    draw_spot_x2 = int((line[2]/IMG_DIM)*bbox['width']+bbox['left'])
    draw_spot_y = int((line[0]/IMG_DIM)*bbox['height']+bbox['top'])

    draw_line(draw_spot_y,draw_spot_x1,draw_spot_x2)

    if keyboard.is_pressed('q'):
            sys.exit()

executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))
