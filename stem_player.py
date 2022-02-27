from audio_playback import StemPlayer
import tkinter as tk
from tkinter import ttk
import csv
import pygame
import logging
import sys

file_handler = logging.FileHandler(filename='logs/stem_player.log')
stdout_handler = logging.StreamHandler(sys.stdout)
handlers = [file_handler, stdout_handler]
logging.basicConfig(level=logging.INFO, handlers=handlers, format='[%(asctime)s] : %(message)s')

root = tk.Tk()
sp = StemPlayer()
sounds_dir = "./sounds/"

root.columnconfigure((0,1), weight=1)
big_frame = ttk.Frame(root)
big_frame.pack()
big_frame.columnconfigure(tuple(range(3)), weight=1)

# Top row - overall playback controls

playback_controls = ttk.Frame(big_frame)
playback_controls.grid(row=0, column=1, rowspan = 1, padx=5, pady=5)
play_button = ttk.Button(playback_controls, text=u"Play/Pause", command = sp.play_pause)
play_button.grid(column=0, row=0, sticky='ew', padx=5)
stop_button = ttk.Button(playback_controls, text=u"Stop", command = sp.stop_all_playback)
stop_button.grid(column=0, row=1, sticky='ew', padx=5)
reset_button = ttk.Button(playback_controls, text=u"Launch Loop", command = sp.replay_all_loops)
reset_button.grid(column=0, row=2, sticky='ew', padx=5)

# First row - labels and sliders

loop_controls = ttk.Frame(big_frame)
loop_controls.grid(row=0, column=0, rowspan = 3)

def instrumental_volume_changed(event):  
    volume = instrumental_slider.get()
    sp.set_channel_volume("instrumental", volume)

instrumental_label = ttk.Label(loop_controls, text="INSTRUMENTAL")
instrumental_label.grid(column=0, row=1, sticky='n', padx=5, pady=5)
instrumental_slider = ttk.Scale(loop_controls, from_=0, to=1, orient="horizontal", command=instrumental_volume_changed)
instrumental_slider.grid(column=0, row=2, sticky='n', padx=5, pady=5)
instrumental_slider.set(100)

def melody_volume_changed(event):  
    volume = melody_slider.get()
    sp.set_channel_volume("melody", volume)

melody_label = ttk.Label(loop_controls, text="MELODY")
melody_label.grid(column=1, row=1, sticky='n', padx=5, pady=5)
melody_slider = ttk.Scale(loop_controls, from_=0, to=1, orient="horizontal", command=melody_volume_changed)
melody_slider.grid(column=1, row=2, sticky='n', padx=5, pady=5)
melody_slider.set(100)

def vocals_volume_changed(event):  
    volume = vocals_slider.get()
    sp.set_channel_volume("vocals", volume)

vocals_label = ttk.Label(loop_controls, text="VOCALS")
vocals_label.grid(column=2, row=1, sticky='n', padx=5, pady=5)
vocals_slider = ttk.Scale(loop_controls, from_=0, to=1, orient="horizontal", command=vocals_volume_changed)
vocals_slider.grid(column=2, row=2, sticky='n', padx=5, pady=5)
vocals_slider.set(100)

# Second row - selectors for loops

instrumental_library = {}
with open(sounds_dir + 'instrumental.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        instrumental_library[row[0]] = row[1]

melody_library = {}
with open(sounds_dir + 'melody.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        melody_library[row[0]] = row[1]

vocals_library = {}
with open(sounds_dir + 'vocals.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        vocals_library[row[0]] = row[1]

def instrumental_combo_selector(event):
    selection = instrumental_selector.get()
    sound = instrumental_library[selection]
    sp.set_instrumental(sound)

def melody_combo_selector(event):
    selection = melody_selector.get()
    sound = melody_library[selection]
    sp.set_melody(sound)

def vocals_combo_selector(event):
    selection = vocals_selector.get()
    sound = vocals_library[selection]
    sp.set_vocals(sound)

instrumental_selector = ttk.Combobox(loop_controls)
instrumental_selector['values'] = tuple(instrumental_library.keys())
instrumental_selector['state'] = 'readonly'
instrumental_selector.grid(row=3, column=0, sticky='nsew', padx=5)
instrumental_selector.bind("<<ComboboxSelected>>", instrumental_combo_selector)

melody_selector = ttk.Combobox(loop_controls)
melody_selector['values'] = tuple(melody_library.keys())
melody_selector['state'] = 'readonly'
melody_selector.grid(row=3, column=1, sticky='nsew', padx=5)
melody_selector.bind("<<ComboboxSelected>>", melody_combo_selector)

vocals_selector = ttk.Combobox(loop_controls)
vocals_selector['values'] = tuple(vocals_library.keys())
vocals_selector['state'] = 'readonly'
vocals_selector.grid(row=3, column=2, sticky='nsew', padx=5)
vocals_selector.bind("<<ComboboxSelected>>", vocals_combo_selector)

# Bottom row - sample grid

samples_library = {}
with open(sounds_dir + 'samples.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        samples_library[row[0]] = row[1]

def samples_volume_changed(event):  
    volume = samples_slider.get()
    sp.set_channel_volume("samples", volume)

def sample_pad_trigger(selection):
    sound = samples_library[selection]
    sp.trigger_sample(sound)

samples_label = ttk.Label(big_frame, text="SAMPLES")
samples_label.grid(column=0, row=5, sticky='n', padx=5, pady=5)
samples_slider = ttk.Scale(big_frame, from_=0, to=1, orient="horizontal", command=samples_volume_changed)
samples_slider.grid(column=0, row=6, sticky='n', padx=5, pady=5)
samples_slider.set(100)

sample_pads_frame = ttk.Frame(big_frame)
sample_pads_frame.grid(column=0, row=7, sticky='n', padx=5, pady=5)
sample_buttons = {}

# Latency compensation control

def delay_changed():
    latency = int(delay_setting.get())
    sp.set_latency(latency)

delay_frame = ttk.Frame(big_frame)
delay_frame.grid(column=1, row=8, sticky='e', pady=50)
delay_label = ttk.Label(delay_frame, text='Latency (ms)')
delay_label.grid(column=0, row=0, sticky='e', padx=5, pady = 5)
delay_value = tk.StringVar(value=140)
delay_setting = ttk.Spinbox(delay_frame, from_=0, to=500, textvariable=delay_value, wrap=True, width=3, command=delay_changed)
delay_setting.grid(column=1, row=0, sticky='e', padx=5, pady = 5)

for idx, sample in enumerate(samples_library.keys()):
    button_grid_size = 4
    sample_buttons[sample] = ttk.Button(sample_pads_frame, text=sample, command = lambda c=sample: sample_pad_trigger(sample_buttons[c].cget("text")))
    sample_buttons[sample].grid(column = idx % button_grid_size, row = idx // button_grid_size, sticky='nsew', padx=5, pady=5)

root.title("697M Stem Player")
root.geometry('800x360')
root.minsize(400, 180)

running = True

def close_window():
  global running
  running = False  # turn off while loop
  logging.info("Exiting Stem Player")

root.protocol("WM_DELETE_WINDOW", close_window)

# Main event loop

while running:
    root.update_idletasks()
    root.update()
    for e in pygame.event.get():
        if e.type == pygame.USEREVENT and sp.player_state == "playing":
            sp.replay_all_loops()
            logging.info(f"Looping")