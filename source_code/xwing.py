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

        # initialize empty constructor so I don't have to use play_song as very first command ever run
        self.media = vlc.MediaPlayer()
  

    def play_song(self):
        if (self.media.is_playing()):
            # don't want to do anything if something already playing
            return
        else:
            self.media = vlc.MediaPlayer(self.path+"/"+self.music_list[self.counter])
            self.media.play()
            self.media.audio_set_volume(50)

            # start a new thread to check the playback status
            self.thread = threading.Thread(target=self.check_playback_status)
            self.thread.start()

    def is_playing(self):
        return self.media.is_playing()

    def release(self):
        self.media.release()

    def is_song_over(self):
        if (self.media.get_state() == vlc.State.Ended):
            self.media.release()
            return True
        else:
            return False

    def check_playback_status(self):
        while True:
            if not self.is_playing():
                print(f"state = {self.media.get_state()}")
                if self.media.get_state() == vlc.State.Ended:
                    print(f"Song finished playing")
                    self.release()
                    break
            time.sleep(0.5)

    def increase_counter(self):
        self.counter += 1
        if (self.counter >= len(self.music_list)):
            self.counter = np.mod(self.counter, len(self.music_list))

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
       
    
        
        
