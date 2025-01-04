#! /usr/bin/env python
import time
import drivers
from time import sleep
from __future__ import print_function
import sys
import wave
import getopt
import alsaaudio

display = drivers.Lcd()


cc = drivers.CustomCharacters(display)

time_object = time.localtime()
local_time = time.strftime("%H:%M:%S", time_object)

line1 = ""
line2 = ""


def play(device, f):    

    print('%d channels, %d sampling rate\n' % (f.getnchannels(),
                                               f.getframerate()))

    # sign 8 bit wave in wav files
    if f.getsampwidth() == 1:
        format = alsaaudio.PCM_FORMAT_U8
    # take for arguements (8 bit var.)
    elif f.getsampwidth() == 2:
        format = alsaaudio.PCM_FORMAT_S16_LE
    elif f.getsampwidth() == 3:
        format = alsaaudio.PCM_FORMAT_S24_LE
    elif f.getsampwidth() == 4:
        format = alsaaudio.PCM_FORMAT_S32_LE
    else:
        raise ValueError('Unsupported format')

    periodsize = f.getframerate() // 8

    device = alsaaudio.PCM(channels=f.getnchannels(), rate=f.getframerate(), format=format, periodsize=periodsize, device=device)
    
    data = f.readframes(periodsize)
    while data:
        # Read data from stdin
        device.write(data)
        data = f.readframes(periodsize)


def usage():
    print('usage: playwav.py [-d <device>] <file>', file=sys.stderr)
    sys.exit(2)


# Change from the default characters given:
# Char 1
cc.char_1_data = ["00001",
                  "00001",
                  "00001",
                  "00001",
                  "00001",
                  "00001",
                  "00001",
                  "00001"]

# Char 2
cc.char_2_data = ["11111",
                  "00001",
                  "00001",
                  "00001",
                  "00001",
                  "00001",
                  "10001",
                  "11111"]

# Char 3
cc.char_3_data = ["11111",
                  "00001",
                  "00001",
                  "00001",
                  "00001",
                  "00001",
                  "00001",
                  "00001"]

# Char 4
cc.char_4_data = ["10000",
                  "10000",
                  "10000",
                  "10000",
                  "10000",
                  "10001",
                  "10001",
                  "11111"]

# Char 5
cc.char_5_data = ["11111",
                  "10000",
                  "10000",
                  "10000",
                  "10000",
                  "10000",
                  "10000",
                  "10000"]

# Char 6
cc.char_6_data = ["11111",
                  "10001",
                  "10001",
                  "10001",
                  "10001",
                  "10001",
                  "10001",
                  "11111"]

# Char 7
cc.char_7_data = ["11111",
                  "10001",
                  "10001",
                  "10001",
                  "10001",
                  "10001",
                  "10001",
                  "10001"]

# Char 8
cc.char_8_data = ["10001",
                  "10001",
                  "10001",
                  "10001",
                  "10001",
                  "10001",
                  "10001",
                  "11111"]
# Load custom characters  to local storage for recalling:
cc.load_custom_characters_data()

def create_lines():
    global local_time, line1, line2
    for i in local_time:
        if i == 1:
            line1 +={0x00}
            line2 +={0x00}
        if i == 2:
            line1 +={0x01}
            line2 +={0x03}
        if i ==3:
            line1+={0x01}
            line2+={0x01}
        if i ==4:
            line1+={0x03}
            line2+={0x00}
        if i ==5:
            line1+={0x04}
            line2+={0x01}
        if i ==6:
            line1+={0x00}
            line2+={0x05}
        if i ==7:
            line1+={0x04}
            line2+={0x00}
        if i ==8:
            line1+={0x06}
            line2+={0x05}
            
        if i ==9:
            line1+={0x05}
            line2+={0x00}
        if i ==0:
            line1+= {0x06}
            line2+= {0x07}
        if i == ":":
            line1+="  "
            line2+="  "
    

# Configuring the speaker type, in case of non default type. 

if __name__ == '__main__':

    device = 'default'
    opts, args = getopt.getopt(sys.argv[1:], 'd:')
    for o, a in opts:
        if o == '-d':
            device = a

    if not args:
        usage()
        
    f = wave.open(args[0], 'rb')

    play(device, f)

    f.close()



# Main body of code for display section
try:
    while True:

        print("Printing the time:")
        create_lines()
        display.lcd_display_extended_string(line1, 1)  # Write line of text to first line of display
        display.lcd_display_extended_string(line2, 2)  # Write line of text to second line of display
        sleep(1) # Refresh evey 1 second
except KeyboardInterrupt:
    
    print("Cleaning up!")
    display.lcd_clear()
