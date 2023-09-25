# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 19:54:55 2023

@author: bsmig
"""
import os
import vlc
import numpy as np

class Xwing:
    
    def __init__(self):
        # make sure DigiAmp+ is unmuted
        self.unmuted = False
        self.song_playing = False
        self.music_list = os.listdir("/home/pi/repos/Halloween_2023/Empire_Strikes_Back_Soundtrack")
        self.counter = 0
        
        #if (not self.unmuted):
        #    os.system('dtoverlay=rpi-digiampplus,unmute_amp')
        #    os.system('dtoverlay=iqaudio-digiampplus,unmute_amp')
        #    self.unmuted = True
    
    def play_song(self, song_name):
        self.media = vlc.MediaPlayer(song_name)
        self.media.play()
        
    def pause_song(self):
        # any non-zero value pauses it
        self.media.set_pause(1)
        
    def resume_song(self):
        # an argument of 0 makes it pause
        self.media.set_pause(0)
        
    def stop_song(self):
        self.media.stop()
        
    def next_song(self):
        self.stop_song()
        self.counter += 1
        if (self.counter > len(self.music_list)):
            self.counter = np.mod(self.counter, len(self.music_list))
        self.play_song(self.music_list[self.counter])
        
    def previous_song(self):
        self.stop_song()
        self.counter -= 1
        if (self.counter < 0):
            self.counter = np.mod(self.counter, len(self.music_list))
        self.play_song(self.music_list[self.counter])
        
    
        
    
        
        