from RPLCD.gpio import CharLCD
import RPi.GPIO as GPIO
from signal import pause
import time
import math
import random
import threading
import os
import numpy as np
from pynput import keyboard
from xwing import Xwing

# define bounce time
BOUNCETIME = 300 # (ms)

# define button pins
gunButtonPin = 18
engineButtonPin = 29
r2d2ButtonPin = 11

# default values
vtc_gun = 0
vtc_engine = 0
vtc_r2d2 = 0
t_gunStart = 0
t_engineStart = 0
t_r2d2Start = 0

# define lcd counter
lcd_counter = 10000

# track if the song started or stopped
music_state = "resume"

# load xwing module I made
xwing = Xwing("music")

def on_press(key):
    try:
        print(f"key {key.char} pressed")
    except AttributeError:
        print(f"special key {key} pressed")

def on_release(key):
    # Had to make this a global variable b/c what I think
    # is going on is that the thread executing this function
    # lost the scope of music_state. With it now as a
    # global variable it remembers it
    global music_state

    #print(f"key {key} released")
    if key == keyboard.KeyCode(char="8"):
        # raise the volume by +10
        print(f"Increasing volume by +10")
        vol = xwing.get_volume()
        vol += 10
        xwing.set_volume(vol)
    elif key == keyboard.KeyCode(char="2"):
        # lower the volume by -10
        vol = xwing.get_volume()
        vol -= 10
        xwing.set_volume(vol)
        print(f"Decreasing volume by -10")
    elif key == keyboard.Key.enter:
        # play the current song
        xwing.play_song()
        music_state = "resume"
    elif key == keyboard.KeyCode(char="4"):
        # play the previous song
        xwing.previous_song()
    elif key == keyboard.KeyCode(char="6"):
        # pay the next song
        xwing.next_song()
    elif key == keyboard.KeyCode(char="0"):
        # stop playing any song
        if (music_state != "stop"):
            xwing.stop_song()
            music_state = "stop"
    elif key == keyboard.KeyCode(char="5"):
        # if the music is initially playing
        # then pause it. If it's paused, then
        # resume playing
        if (music_state == "resume"):
            xwing.pause_song()
            music_state = "pause"
        elif (music_state == "pause"):
            xwing.resume_song()
            music_state = "resume"

def activate_range_counter(lcd_counter):
    # Make the top row of the LCD say "Range (km)"
    # Make the bottom row be a rapidly decreasing counter
	# such that when it hits 0, it wraps back around
	# again at the highest starting value
	lcd.clear()
	lcd.cursor_pos = (0,1)
	lcd.write_string(u'Target Range')
	lcd.lf()
	lcd.cursor_pos = (1,5)
	value = f'{lcd_counter}'
	if (lcd_counter == 10000):
		lcd.write_string(value)
	elif (lcd_counter < 10000 and lcd_counter >= 1000):
		lcd.write_string(value+' m')
	elif (lcd_counter < 1000 and lcd_counter >= 100):
		lcd.write_string(value+' m ')
	elif (lcd_counter < 100 and lcd_counter >= 10):
		lcd.write_string(value+' m  ')
	elif (lcd_counter < 10 and lcd_counter >= 1):
		lcd.write_string(value+' m   ')
	elif (lcd_counter == 0):
		lcd.write_string(u'BOOM!!!')
	#time.sleep(10)
	lcd_counter -= 1
	lcd_counter = np.mod(lcd_counter, 10000)

	return lcd_counter

def play_r2d2_sounds(instance_number):
    xwing = Xwing("r2d2")
    first_time_thru = True
    while True:
        # this simulates a user pushing the button
        was_button_pushed = random.randint(0, 50)
        #print(f"random num = {was_button_pushed}")

        if (was_button_pushed == 1 and first_time_thru):
            xwing.play_song()
            first_time_thru = False
            #print("FIRST TIME THRU")
        else:
            if (was_button_pushed == 1 and xwing.is_song_over()):
                xwing.increase_counter()
                xwing.play_song()
                #print("INCREMENTED SONG")
            #else:
                #print("WAITING FOR SONG TO END")
                
        time.sleep(0.1)


# define threads to use so I can layer sounds on top of music
threads = []
thread = threading.Thread(target=play_r2d2_sounds, args=(0,))
threads.append(thread)
thread.start()


# use physical pin numbering
GPIO.setmode(GPIO.BOARD)
# initialize GPIO pins
GPIO.setup(gunButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(engineButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(r2d2ButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# load correct LCD pins (as GPIO.BOARD = physical pin numbering)
# Cannot use physical pin 15 (GPIO22) since this is used by DigiAmp+
rs = 13
e  = 16
d4 = 19
d5 = 21
d6 = 23
d7 = 24
columns = 16
rows = 2

# initialize the LCD using the pins
lcd = CharLCD(numbering_mode=GPIO.BOARD, cols=columns, rows=rows, pin_rs=rs, pin_e=e, pins_data=[d4,d5,d6,d7])
lcd.clear()

# setup the keyboard and be prepared to listen for user input
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

try:
    print(f"GPIO version = {GPIO.VERSION}") 
    
    while True:
        # run the target range LCD
        lcd_counter = activate_range_counter(lcd_counter)
        time.sleep(0.05)

except KeyboardInterrupt:
    GPIO.cleanup()
    listener.join()
    lcd.clear()
    for thread in threads:
        thread.join()


