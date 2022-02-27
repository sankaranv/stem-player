import os
import sys
import logging
from threading import Thread

logging.basicConfig(level=logging.INFO)
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame


class StemPlayer:

    def __init__(self):

        self.init_mixer()
        self.sounds_dir = "./sounds/"
        self.channels = {
                        "samples" : pygame.mixer.Channel(3), 
                        "vocals": pygame.mixer.Channel(2), 
                        "melody": pygame.mixer.Channel(1), 
                        "instrumental": pygame.mixer.Channel(0)
                        }
        self.active_loops = {
                        "vocals": {"location": None, "obj": None}, 
                        "melody": {"location": None, "obj": None}, 
                        "instrumental": {"location": None, "obj": None}
                        } 
        self.loop_length = 18.431995391845703

    def play_pause(self):

        if self.player_state == "stopped":
            logging.info(f"Play/Pause - current state is {self.player_state}, so now replaying all loops")
            self.replay_all_loops()
        elif self.player_state == "paused":
            logging.info(f"Play/Pause - current state is {self.player_state}, so now unpausing")
            pygame.mixer.unpause()
            self.player_state = "playing"
        else:
            logging.info(f"Play/Pause - current state is {self.player_state}, so now pausing")
            pygame.mixer.pause()
            self.player_state = "paused"

    def replay_all_loops(self):
        pygame.mixer.stop()
        self.player_state = "playing"
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        threads = []
        threads.append(Thread(target = self.play_instrumental))
        threads.append(Thread(target = self.play_melody))
        threads.append(Thread(target = self.play_vocals))
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                for thread in threads:
                    thread.start()
                for thread in threads:
                    thread.join()

    
    def play_instrumental(self):
        sound = self.active_loops["instrumental"]
        obj = sound["obj"]
        loc = sound["location"]
        if obj is not None:
            self.channels["instrumental"].play(obj, -1)
            self.loop_length = obj.get_length()
            logging.info(f"Playing {loc} on instrumental channel with length {self.loop_length}")
            

    def play_melody(self):
        sound = self.active_loops["melody"]
        obj = sound["obj"]
        loc = sound["location"]
        if obj is not None:
            self.channels["melody"].play(sound["obj"], -1)
            self.loop_length = obj.get_length()
            logging.info(f"Playing {loc} on melody channel with length {self.loop_length}")

    def play_vocals(self):
        sound = self.active_loops["vocals"]
        obj = sound["obj"]
        loc = sound["location"]
        if obj is not None:
            self.channels["vocals"].play(sound["obj"], -1)
            self.loop_length = obj.get_length()
            logging.info(f"Playing {loc} on vocals channel with length {self.loop_length}")

    def stop_all_playback(self):
        pygame.mixer.stop()
        self.player_state = "stopped"
        logging.info(f"Stopped playback")

    def init_mixer(self):
        pygame.init()
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.mixer.init()
        self.player_state = "stopped"
        logging.info(f"Initialized Stem Player")

    def set_channel_sound(self, channel, sound):
        sound_path = self.sounds_dir + channel + "/" + sound
        if os.path.isfile(sound_path):
            if self.active_loops[channel]["location"] != sound_path:
                self.active_loops[channel]["location"] = sound_path
                self.active_loops[channel]["obj"] = pygame.mixer.Sound(sound_path)
                logging.info(f"Set {sound} on {channel} channel")
            else:
                logging.info(f"Already playing {sound} on {channel} channel")
        else:
            logging.info(f"Sound {sound} not found!")
    
    def set_channel_volume(self, channel, value):
        self.channels[channel].set_volume(value)
        logging.debug(f"Volume of {channel} is now {value}")

    def set_vocals(self, sound):
        self.set_channel_sound("vocals", sound)

    def set_melody(self, sound):
        self.set_channel_sound("melody", sound)

    def set_instrumental(self, sound):
        self.set_channel_sound("instrumental", sound)
    
    def trigger_sample(self, sound):
        if os.path.isfile(self.sounds_dir + "samples/" + sound):
            sound_path = self.sounds_dir + "samples/" + sound
            self.channels["samples"].play(pygame.mixer.Sound(sound_path))
            logging.info(f"Triggered sample {sound}")

if __name__ == "__main__":
    pass