# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 19:54:55 2023

@author: bsmig
"""
import os
import vlc
import numpy as np
import time

class Xwing:
    
    def __init__(self, runtime_loc):
        # make sure DigiAmp+ is unmuted
        self.unmuted = False
        self.song_playing = False
        if (runtime_loc == "pi"):
            self.path = "/home/pi/repos/HalloweenXWing_2023/Empire_Strikes_Back_Soundtrack"
        elif (runtime_loc == "home"):
            self.path = "C:/Users/bsmig/Documents/repos/HalloweenXWing_2023/Empire_Strikes_Back_Soundtrack"
        self.music_list = os.listdir(self.path)
        print(f"there are {len(self.music_list)} songs")
        self.counter = 0

        # initialize empty constructor so I don't have to use play_song as very first command ever run
        self.media = vlc.MediaPlayer()       

        # initialize R2D2 sounds media player
        self.r2d2 = vlc.MediaPlayer()

        #if (not self.unmuted):
        #    os.system('dtoverlay=rpi-digiampplus,unmute_amp')
        #    os.system('dtoverlay=iqaudio-digiampplus,unmute_amp')
        #    self.unmuted = True
    
    def play_song(self):
        if (self.media.is_playing()):
            # don't want to do anything if something already playing
            return
        else:
            self.media = vlc.MediaPlayer(self.path+"/"+self.music_list[self.counter])
            self.media.play()

    def pause_song(self):
        # any non-zero value pauses it
        self.media.set_pause(1)
        
    def resume_song(self):
        # an argument of 0 makes it pause
        self.media.set_pause(0)
        
    def stop_song(self):
        self.media.stop()
        self.media.release()
        
    def next_song(self):
        self.stop_song()
        self.counter += 1
        if (self.counter >= len(self.music_list)):
            self.counter = np.mod(self.counter, len(self.music_list))
        print(f"counter={self.counter}")
        self.play_song()
        
    def previous_song(self):
        self.stop_song()
        self.counter -= 1
        if (self.counter < 0):
            self.counter = np.mod(self.counter, len(self.music_list))
        print(f"counter={self.counter}")
        self.play_song()
        
    def set_volume(self, volume):
        if (volume < 0 or volume > 100):
            return
        else:
            self.media.audio_set_volume(volume)

    def get_volume(self):
        return self.media.audio_get_volume()
        
    
        
        
