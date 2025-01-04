#! /usr/bin/env python

import drivers
from time import *
from datetime import datetime


display = drivers.Lcd()


try:
    print("Writing to display")
    display.lcd_display_string("Time", 2)  
    display.lcd_display_string("18 Dec 2024", 3)
    display.lcd_display_string("Date", 4) 

    while True:
        # Write just the time to the display
        time_object = time.localtime()
        local_time = time.strftime("%H:%M:%S", time_object) 
        display.lcd_display_string(str(local_time), 1)
        
        
except KeyboardInterrupt:
    print("Cleaning up!")
    display.lcd_clear()
