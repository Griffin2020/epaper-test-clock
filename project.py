#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
from datetime import datetime
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in7
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
from gpiozero import Button
import calendar
logging.basicConfig(level=logging.DEBUG)

screen = 0
bmp = Image.open('rightarrow.png')       
bmp = bmp.resize((50, 50))
bmp = bmp.crop((10, 10, 60, 60))
medium_font = ImageFont.truetype('/usr/share/fonts/truetype/piboto/Piboto-Regular.ttf', 20)
big_font = ImageFont.truetype('/usr/share/fonts/truetype/piboto/Piboto-Regular.ttf', 50)
small_font = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf', 14)
current_month = datetime.now().month
current_year = datetime.now().year
my_month = current_month
my_year = current_year
def cycleScreen():
    logging.info("button pressed")

    global screen
    if screen == 1:
        screen = 0
    else:
        screen += 1

    drawScreen(screen)
def addMonth():
    global my_month
    global my_year
    global screen
    if my_month == 12:
        my_month = 1
        my_year += 1
    else:
        my_month += 1
    drawScreen(screen)
def subMonth():
    global my_month
    global my_year
    global screen
    if my_month == 1:
        my_month = 12
        my_year -= 1
    else:
        my_month -= 1
    drawScreen(screen)
    
def drawScreen(screen):
        global bmp
        Himage = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH), 255)
        draw = ImageDraw.Draw(Himage)
        
        # Draws next arrow
        Himage.paste(bmp, (4, 8))

        # Draws dividing lines
        draw.line((0, epd2in7.EPD_WIDTH / 4, 36, epd2in7.EPD_WIDTH / 4))
        draw.line((0, epd2in7.EPD_WIDTH / 2, 36, epd2in7.EPD_WIDTH / 2))
        draw.line((0, 3 * (epd2in7.EPD_WIDTH / 4), 36, 3 * (epd2in7.EPD_WIDTH / 4)))
        draw.line((36, 0, 36, epd2in7.EPD_WIDTH))

        
        if(screen == 0):
            print(epd2in7.EPD_WIDTH, epd2in7.EPD_HEIGHT)
            button2.when_pressed = addMonth
            button4.when_pressed = subMonth
            
            now = datetime.now()
        
            current_time = now.strftime("%H:%M")
            current_date = now.strftime("%b %d")
            current_day = now.strftime("%A")
            today = datetime.today()
            
            draw.rectangle((16, 56, 20, 76), fill = 0)
            draw.rectangle((8, 64, 28, 68), fill = 0)
            draw.rectangle((8, 152, 28, 156), fill = 0)
            draw.line((36, epd2in7.EPD_WIDTH / 4, epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH / 4))
            
            draw.line((228, epd2in7.EPD_WIDTH / 4, 228, epd2in7.EPD_WIDTH))
            draw.text((40, -12), current_time, font = big_font, fill = 0)
            
            draw.text((180, 20), current_date, font = medium_font, fill = 0)
            draw.text((180, -2), current_day, font = medium_font, fill = 0)
            draw = ImageDraw.Draw(Himage)
            
            # puts a box around current day 
            if current_month == my_month and current_year == my_year:
                
                current_calendar = calendar.month(current_year, current_month)
                counted_string = ""
                for i in range(5):
                    counted_string += current_calendar.split("\n")[i + 2]
                    counted_string += "n"
                counted_string = counted_string.split(str(today.day))
                
                
                y_offset = counted_string[0].count('n') + 1
                    
                x_offset = (len(counted_string[0]) - y_offset) % 20
                
                if today.day > 10:
                    x_offset = x_offset + 1
                x_offset = x_offset % 20
                
                
                draw.rectangle((50 + (x_offset * 8), 60 + (y_offset * 16), 70 + (x_offset * 8), 75 + (y_offset * 16)))
                draw.text((52 + (x_offset * 8), 62 + (y_offset * 16)), str(today.day), font = small_font, fill = 0)
            draw.text((52, 45), calendar.month(my_year, my_month), font = small_font, fill = 0)
            
            logging.info("Screen 0")   

        if(screen == 1):
            
    
            logging.info("Screen 1")
        #Himage.show()
        epd.display_4Gray(epd.getbuffer_4Gray(Himage))

    
try:
    epd = epd2in7.EPD()
    
    epd.Init_4Gray()
    epd.Clear(0xFF)
    corner4 = "Cycle"
    screen = 0
    
    button1 = Button(5)
    button2 = Button(6)
    button3 = Button(13)
    button4 = Button(19)
    button1.when_pressed = cycleScreen
    

    while True:
        
        drawScreen(screen)
        
        time.sleep(30)
    
    epd.Clear(0xFF)
    epd.sleep()
    

except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in7.epdconfig.module_exit()
    exit()
