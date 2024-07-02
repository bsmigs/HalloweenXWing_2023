from RPLCD.gpio import CharLCD
import RPi.GPIO as GPIO
from signal import pause
import time
import math
import random
import threading
import os
import numpy as np
import serial
from xwing import Xwing
from evdev import InputDevice, list_devices, categorize, ecodes

# define bounce time
BOUNCETIME = 300 # (ms)

# define button pins
r2d2ButtonPin = 36
gunButtonPin = 37
engineButtonPin = 38

# use physical pin numbering
GPIO.setmode(GPIO.BOARD)
# initialize GPIO pins
GPIO.setup(r2d2ButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(gunButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(engineButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

lastR2D2ButtonState = GPIO.LOW
lastGunButtonState = GPIO.LOW
lastEngineButtonState = GPIO.LOW

# default values
lastTimeGunButtonPressed = 0
lastTimeEngineButtonPressed = 0
lastTimeR2D2ButtonPressed = 0

# define lcd counter
lcd_counter = 10000

# track if the song started or stopped
music_state = "resume"

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


# load xwing module I made
xwing = Xwing("music")

def take_external_keypad_input():
    devices = [InputDevice(fn) for fn in list_devices()]
    keypad = devices[0]
    print(f"Found external keypad device {keypad.name}")
    for event in keypad.read_loop():
        if event.type == ecodes.EV_KEY:
            key_event = categorize(event)
            if key_event.keystate == key_event.key_down:
                print(f"Pressed key: {key_event.keycode}")
            elif key_event.keystate == key_event.key_up:
                print(f"Released key: {key_event.keycode}")
                if (key_event.keycode == "KEY_KPENTER"):
                    xwing.play_song()
                    music_state = "resume"
                elif (key_event.keycode == "KEY_KP0"):
                    if (music_state != "stop"):
                        xwing.stop_song()
                        music_state = "stop"
                elif (key_event.keycode == "KEY_KP8"):
                    print(f"Increasing volume by +10")
                    vol = xwing.get_volume()
                    vol += 10
                    xwing.set_volume(vol)
                elif (key_event.keycode == "KEY_KP2"):
                    print(f"Decreasing volume by -10")
                    vol = xwing.get_volume()
                    vol -= 10
                    xwing.set_volume(vol)
                elif (key_event.keycode == "KEY_KP4"):
                    xwing.previous_song()
                elif (key_event.keycode == "KEY_KP6"):
                    xwing.next_song()
                elif (key_event.keycode == "KEY_KP7"):
                    xwing.change_looping_status()
                elif (key_event.keycode == "KEY_KP5"):
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


def play_sounds(instance_number):
    if (instance_number == 0):
        global lastR2D2ButtonState
        global lastTimeR2D2ButtonPressed
        lastButtonState = lastR2D2ButtonState
        lastTimeButtonPressed = lastTimeR2D2ButtonPressed
        buttonPin = r2d2ButtonPin
        xwing = Xwing("r2d2")
    elif (instance_number == 1):
        global lastGunButtonState
        global lastTimeGunButtonPressed
        lastButtonState = lastGunButtonState
        lastTimeButtonPressed = lastTimeGunButtonPressed
        buttonPin = gunButtonPin
        xwing = Xwing("gun")
    elif (instance_number == 2):
        global lastEngineButtonState
        global lastTimeEngineButtonPressed
        lastButtonState = lastEngineButtonState
        lastTimeButtonPressed = lastTimeEngineButtonPressed
        buttonPin = engineButtonPin
        xwing = Xwing("engine")

    # logic below is generic
    first_time_thru = True
    while True:
        buttonState = GPIO.input(buttonPin)
        # see if bouncetime expired
        if (time.time() - lastTimeButtonPressed > BOUNCETIME):
            # if greater than bounce time, make sure some action occurred
            if (buttonState != lastButtonState):
                # if an action occurred, log the last time it happened
                lastTimeButtonStateChanged = time.time()
                lastButtonState = buttonState

                # only do something non-trivial if the button was pushed
                if (buttonState == GPIO.HIGH):
                    if (first_time_thru):
                        xwing.play_song()
                        first_time_thru = False
			            #print("FIRST TIME THRU")
                    else:
                        if (xwing.did_song_end()):
                            xwing.next_song()
                            print("INCREMENTED SONG")
                        else:
                            print("WAITING FOR SONG TO END")
                
        time.sleep(0.1)


# define a serial object to Rx status regarding
# whether or not the button to spin R2D2 was
# pushed
ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)
# flush out any crap in the buffer
ser.reset_input_buffer()

def make_R2D2_squeak_while_spinning():
    r2d2 = Xwing("r2d2")
    
    while True:
        # check the buffer
        number = ser.read()
        print(f"number = {number}")

        # if Arduino doesn't send any bytes over it'll be empoty
        if number != b'':
            if int.from_bytes(number, byteorder='big') == 18:
                r2d2.next_song()
                ser.reset_input_buffer()

        time.sleep(0.05)


try:
    print(f"GPIO version = {GPIO.VERSION}") 
	
    # define threads to use so I can layer sounds on top of music
    threads = []
    for ii in range(0,3):
        thread = threading.Thread(target=play_sounds, args=(ii,))
        threads.append(thread)
        thread.start()

	# initialize the LCD using the pins
    lcd = CharLCD(numbering_mode=GPIO.BOARD, cols=columns, rows=rows, pin_rs=rs, pin_e=e, pins_data=[d4,d5,d6,d7])
    lcd.clear()

    # setup the keyboard and be prepared to listen for user input
    thread = threading.Thread(target=take_external_keypad_input)
    threads.append(thread)
    thread.start()

    thread_launched = False

    # define a thread for the spinning/R2D2 sounds
    sound_spin_thread = threading.Thread(target=make_R2D2_squeak_while_spinning)
    sound_spin_thread.start()

    while True:
        # run the target range LCD
        lcd_counter = activate_range_counter(lcd_counter)
        time.sleep(0.05)

        if (xwing.is_playing() and not thread_launched):
            playback_check_thread = threading.Thread(target=xwing.check_playback_status())
            playback_check_thread.start()
            thread_launched = True
        if (xwing.did_song_end() and thread_launched):
            if (xwing.is_looping):
                # if we're looping, just go to the next song
                xwing.next_song()
            else:
                # release the memory and join the thread back to the pool
                playback_check_thread.join()
                xwing.release()
                thread_launched = False
                print(f"Song over and joining thread")



except KeyboardInterrupt:
    GPIO.cleanup()
    lcd.clear()
    sound_spin_thread.join()
    for thread in threads:
        thread.join()


