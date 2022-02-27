import os
import sys
import logging
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
                        "vocals": None, 
                        "melody": None, 
                        "instrumental": None
                        } 

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
        for channel, sound in self.active_loops.items():
            if sound is not None and os.path.isfile(self.sounds_dir + channel + "/" + sound):
                sound_path = self.sounds_dir + channel + "/" + sound  
                self.channels[channel].play(pygame.mixer.Sound(sound_path), -1)
                logging.info(f"Playing {sound} on {channel} channel")

    def stop_all_playback(self):
        pygame.mixer.stop()
        self.player_state = "stopped"
        logging.info(f"Stopped playback")

    def init_mixer(self):
        pygame.init()
        pygame.mixer.init()
        self.player_state = "stopped"
        logging.info(f"Initialized Stem Player")

    def set_channel_sound(self, channel, sound):
        if os.path.isfile(self.sounds_dir + channel + "/" + sound):
            if self.active_loops[channel] != sound:
                self.active_loops[channel] = sound
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
    
    def trigger_sample(self):
        pass

if __name__ == "__main__":
    pass