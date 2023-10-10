import RPi.GPIO as GPIO
from signal import pause
import time
import math
import random
#import soundfile as sf
#import simpleaudio as sa
import os
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

# track if the song started or stopped
music_state = "resume"

# load xwing module I made
xwing = Xwing("pi")

def getSoundsDurations(path_to_files):
    sounds = os.listdir(path_to_files)
    durations = []
    for file in sounds:
        f = sf.SoundFile(path_to_files+"/"+file)
        samples = len(f)
        sampleRate = f.samplerate
        duration = math.ceil(samples/sampleRate)
        durations.append(duration)
    
    return sounds, durations
   
'''
cookieSounds, cookieSoundsDurations = getSoundsDurations("wav_files")
hornSounds, hornSoundsDurations = getSoundsDurations("horn_sounds")

cc = random.randint(0, len(cookieSounds)-1)
hh = random.randint(0, len(hornSounds)-1)
'''

print(f"music_state = {music_state}")

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
    print(f"music_state = {music_state}")

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
    elif key == keyboard.KeyCode(char="4"):
        # play the previous song
        xwing.previous_song()
    elif key == keyboard.KeyCode(char="6"):
        # pay the next song
        xwing.next_song()
    elif key == keyboard.KeyCode(char="0"):
        # stop playing any song
        xwing.stop_song()
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


# use physical pin numbering
GPIO.setmode(GPIO.BOARD)

GPIO.setup(gunButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(engineButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(r2d2ButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

try:
    print(GPIO.VERSION) 
    #GPIO.add_event_detect(headlightButtonPin, GPIO.RISING, callback=toggleHeadlights, bouncetime=BOUNCETIME)
    
    while True:
        '''
        if (GPIO.input(cookieSoundsButtonPin)==GPIO.LOW) and (time.time() - t_cookieStart) > vtc_cookie:
            vtc_cookie = cookieSoundsDurations[cc]
            t_cookieStart = time.time()
            wave_obj = sa.WaveObject.from_wave_file("wav_files/"+cookieSounds[cc])
            play_obj = wave_obj.play()
            play_obj.wait_done()
            cc = (cc + 1) % len(cookieSounds)

        if (GPIO.input(hornButtonPin)==GPIO.LOW) and (time.time() - t_hornStart) > vtc_horn:
            vtc_horn = hornSoundsDurations[hh]
            t_hornStart = time.time()
            wave_obj = sa.WaveObject.from_wave_file("horn_sounds/"+hornSounds[hh])
            play_obj = wave_obj.play()
            play_obj.wait_done()
            hh = (hh + 1) % len(hornSounds)
        '''

except KeyboardInterrupt:
    GPIO.cleanup()
    listener.join()
