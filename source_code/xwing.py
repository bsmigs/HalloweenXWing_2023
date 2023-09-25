# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 19:54:55 2023

@author: bsmig
"""
import os
import vlc
import numpy as np
import time
from threading import Thread

class Xwing:
    
    def __init__(self):
        # make sure DigiAmp+ is unmuted
        self.unmuted = False
        self.song_playing = False
        self.path = "/home/pi/repos/HalloweenXWing_2023/Empire_Strikes_Back_Soundtrack"
        self.music_list = os.listdir(self.path)
        print(f"there are {len(self.music_list)} songs")
        self.counter = 0

        # initialize empty constructor so I don't have to use play_song as very first command ever run
        self.media = vlc.MediaPlayer()       

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
#        self.check_play_status()

    def _check_play_status(self):
        time.sleep(1) # needed b/c is_playing returns False if called immediately
        while (self.media.is_playing()):
            time.sleep(1)
        self.media.release()
        
    def check_play_status(self):
        Thread(target=self._check_play_status()).start()

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
        print(f"counter={self.counter}")
        if (self.counter >= len(self.music_list)):
            self.counter = np.mod(self.counter, len(self.music_list))
        self.play_song()
        
    def previous_song(self):
        self.stop_song()
        self.counter -= 1
        print(f"counter={self.counter}")
        if (self.counter < 0):
            self.counter = np.mod(self.counter, len(self.music_list))
        self.play_song()
        
    
        
    
        
        
