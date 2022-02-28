import os
import sys
import logging
from threading import Thread

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

file_handler = logging.FileHandler(filename='logs/stem_player.log')
stdout_handler = logging.StreamHandler(sys.stdout)
handlers = [file_handler, stdout_handler]
logging.basicConfig(level=logging.INFO, handlers=handlers, format='[%(asctime)s] : %(message)s')

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
        self.loop_length = 18431
        self.latency = 150

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
        # pygame.mixer.stop()
        self.player_state = "playing"
        threads = []
        threads.append(Thread(target = self.play_instrumental))
        threads.append(Thread(target = self.play_melody))
        threads.append(Thread(target = self.play_vocals))
        threads.append(Thread(target = self.set_replay_timer))
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

    def set_replay_timer(self):
        pygame.time.set_timer(pygame.USEREVENT, self.loop_length - self.latency)
    
    def play_instrumental(self):
        sound = self.active_loops["instrumental"]
        obj = sound["obj"]
        loc = sound["location"]
        if obj is not None:
            self.channels["instrumental"].play(obj)
            self.loop_length = int(obj.get_length() * 1000)
            logging.info(f"Playing {loc} on instrumental channel with length {self.loop_length}")       

    def play_melody(self):
        sound = self.active_loops["melody"]
        obj = sound["obj"]
        loc = sound["location"]
        if obj is not None:
            self.channels["melody"].play(sound["obj"])
            self.loop_length = int(obj.get_length() * 1000)
            logging.info(f"Playing {loc} on melody channel with length {self.loop_length}")

    def play_vocals(self):
        sound = self.active_loops["vocals"]
        obj = sound["obj"]
        loc = sound["location"]
        if obj is not None:
            self.channels["vocals"].play(sound["obj"])
            self.loop_length = int(obj.get_length() * 1000)
            logging.info(f"Playing {loc} on vocals channel with length {self.loop_length}")

    def stop_all_playback(self):
        pygame.mixer.stop()
        self.player_state = "stopped"
        logging.info(f"Stopped playback")

    def init_mixer(self):
        pygame.init()
        pygame.mixer.pre_init(frequency=48000, size=-16, channels=2, buffer=512)
        pygame.mixer.init()
        pygame.mixer.quit()
        pygame.mixer.init(frequency=48000, size=-16, channels=2, buffer=512)
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

    def set_latency(self, latency):
        self.latency = latency
        logging.info(f"Set loop latency compensation to {latency} ms")

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