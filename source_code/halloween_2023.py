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
r2d2Sounds, r2d2SoundsDurations = getSoundsDurations("r2d2_sounds")
gunSounds, gunSoundsDurations = getSoundsDurations("gun_sounds")
engineSounds, engineSoundsDurations = getSoundDurations("engine_sounds")

rr = random.randint(0, len(r2d2Sounds)-1)
gg = random.randint(0, len(gunSounds)-1)
ee = random.randint(0, len(engineSounds)-1)
'''

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
    #print(GPIO.VERSION) 
    
    while True:
        '''
        if (GPIO.input(gunButtonPin)==GPIO.LOW) and (time.time() - t_gunStart) > vtc_gun:
            vtc_gun = gunSoundsDurations[gg]
            t_gunStart = time.time()
            wave_obj = sa.WaveObject.from_wave_file("gun_sounds/"+gunSounds[gg])
            play_obj = wave_obj.play()
            play_obj.wait_done()
            gg = (gg + 1) % len(gunSounds)

        if (GPIO.input(engineButtonPin)==GPIO.LOW) and (time.time() - t_engineStart) > vtc_engine:
            vtc_engine = engineSoundsDurations[hh]
            t_engineStart = time.time()
            wave_obj = sa.WaveObject.from_wave_file("engine_sounds/"+engineSounds[ee])
            play_obj = wave_obj.play()
            play_obj.wait_done()
            ee = (ee + 1) % len(engineSounds)

        if (GPIO.input(r2d2ButtonPin)==GPIO.LOW) and (time.time() - t_r2d2Start) > vtc_r2d2:
            vtc_r2d2 = r2d2SoundsDurations[rr]
            t_r2d2Start = time.time()
            wave_obj = sa.WaveObject.from_wave_file("r2d2_sounds/"+r2d2Sounds[rr])
            play_obj = wave_obj.play()
            play_obj.wait_done()
            rr = (rr + 1) % len(r2d2Sounds)
        '''

except KeyboardInterrupt:
    GPIO.cleanup()
    listener.join()
