import RPi.GPIO as GPIO
from signal import pause
import time
import math
import random
#import soundfile as sf
#import simpleaudio as sa
import os
import keyboard
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

# load xwing module I made
xwing = Xwing("pi")

# track if the song started or stopped
music_state = "resume"

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

# use physical pin numbering
GPIO.setmode(GPIO.BOARD)

GPIO.setup(gunButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(engineButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(r2d2ButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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

        if keyboard.read_key() == "8":
            vol = xwing.get_volume()
            vol += 10
            xwing.set_volume(vol)

        if keyboard.read_key() == "2":
            vol = xwing.get_volume()
            vol -= 10
            xwing.set_volume()

        if keyboard.read_key() == "6":
            xwing.next_song()

        if keyboard.read_key() == "4":
            xwing.previous_song()

        if keyboard.read_key() == "5":
            if (music_state == "start"):
                xwing.pause_song()
                music_state = "pause"
            elif (music_state == "pause"):
                xwing.resume_song()
                music_state = "start"

        if keyboard.read_key() == "enter":
            xwing.play_song()

        if keyboard.read_key() == "0":
            xwing.stop_song()

except KeyboardInterrupt:
    GPIO.cleanup()
