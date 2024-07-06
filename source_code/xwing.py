import os
import vlc
import numpy as np
import time
from RPLCD.gpio import CharLCD
import RPi.GPIO as GPIO
import threading

class Xwing:
    
    def __init__(self, label):
        self.label = label
        self.song_playing = False
        if (label == "music"):
            # make sure DigiAmp+ is unmuted
            #self.unmuted = False
            self.path = "/home/pi/repos/HalloweenXWing_2023/Empire_Strikes_Back_Soundtrack"
			#if (not self.unmuted):
            #    os.system('dtoverlay=rpi-digiampplus,unmute_amp')
            #    os.system('dtoverlay=iqaudio-digiampplus,unmute_amp')
            #    self.unmuted = True 
        elif (label == "r2d2"):
            self.path = "/home/pi/repos/HalloweenXWing_2023/r2d2_sounds_mp3s"
        elif (label == "gun"):
            self.path = "/home/pi/repos/HalloweenXWing_2023/gun_sounds_mp3s"
        elif (label == "engine"):
            self.path = "/home/pi/repos/HalloweenXWing_2023/engine_sounds_mp3s"

        self.music_list = os.listdir(self.path)
        print(f"there are {len(self.music_list)} sounds or music")

        # set sounds/music counter = 0 initially
        self.counter = 0

        # track release status since trying to release more
        # than once can cause issues
        self.is_released = False

        # track if we will be looping through songs
        self.is_looping = False

        # track the volume since every time
        # self.media is released the volume is set equal
        # to 0 again
        self.curr_volume = 75

<<<<<<< HEAD
        # initialize empty constructor so I don't have to use play_song as very first command ever run
=======
        # initialize empty constructor so I don't have to use play_song as very first command ever ru
>>>>>>> devel
        self.media = vlc.MediaPlayer()

    def play_song(self):
        if (self.media.is_playing()):
            # don't want to do anything if something already playing
            return
        else:
            self.media = vlc.MediaPlayer(self.path+"/"+self.music_list[self.counter])
            self.media.play()
            print(f"Current volume = {self.curr_volume}")
            self.media.audio_set_volume(self.curr_volume)
            self.is_released = False
<<<<<<< HEAD
=======

>>>>>>> devel

    def is_playing(self):
        return self.media.is_playing()

    def change_looping_status(self):
        self.is_looping = not self.is_looping
        print(f"Looping status now set to {self.is_looping}")

    def release(self):
        if (not self.is_released):
            self.media.release()
            self.is_released = True

    def did_song_end(self):
        if (self.media.get_state() == vlc.State.Ended):
            return True
        else:
            return False

    def check_playback_status(self):
        while True:
            if not self.is_playing():
                print(f"State = {self.media.get_state()}")
                if self.media.get_state() == vlc.State.Ended:
                    print(f"Song finished playing")
                    self.release()
                    break
            time.sleep(0.5)

    def change_counter(self, inc_or_dec):
        if (inc_or_dec == "inc"):
            # increase counter
            self.counter += 1
        elif (inc_or_dec == "dec"):
            # decrease counter
            self.counter -= 1

        if (self.counter >= len(self.music_list) or self.counter < 0):
            self.counter = np.mod(self.counter, len(self.music_list))

    def pause_song(self):
        # any non-zero value pauses it
        self.media.set_pause(1)
        
    def resume_song(self):
        # an argument of 0 makes it resume
        self.media.set_pause(0)
        
    def stop_song(self):
        if (self.media.get_state() == vlc.State.Ended):
            # if song has ended and I try to call
            # self.media.stop(), I'll get a seg fault
            self.release()
        else:
            self.media.stop()
            self.release()
        
    def next_song(self):
        self.stop_song()
        self.change_counter("inc")
        print(f"counter={self.counter}")
        self.play_song()
        
    def previous_song(self):
        self.stop_song()
        self.change_counter("dec")
        print(f"counter={self.counter}")
        self.play_song()

    def set_volume(self, volume):
        if (volume < 0 or volume > 100):
            return
        else:
            self.curr_volume = volume
            self.media.audio_set_volume(volume)

    def get_volume(self):
        return self.curr_volume
<<<<<<< HEAD
        #return self.media.audio_get_volume()
=======
>>>>>>> devel
       
    
        
        
