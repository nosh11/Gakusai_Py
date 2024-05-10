#
# なにかのゲーム
#
# Created by nosssy
# 処理研2024 Programming部 出展

import os
import tkinter as tk
from pygame import mixer
import math
import random
from PIL import ImageGrab

from commons.sound import MusicPlayer
from commons.ui import title, game

import time

current_screen = "title"
screen_timer = 0
root = tk.Tk()
root.title(u"何かのゲーム")
root.geometry("500x500")
root.resizable(False, False)
root.iconphoto(False, tk.PhotoImage(file = "assets\icon.png"))
canvas = tk.Canvas(root, width=500, height=500)
graphic = tk.Canvas(root, width=500, height=500, bd=0, highlightthickness=0)

# Functions
def update():
    global screen_timer, rect_index, scr
    screen_timer += 1
    scr(screen_timer)
    root.after(10, update)

def change_ui(to):
    global screen_timer, current_screen, scr
    canvas.delete("all")
    screen_timer = 0
    current_screen = to
    if (to == "title"):
        music.play()
        sound_back.play()
        scr = title.screen(canvas)
    elif (to == "game"):
        music.stop()
        sound_done.play()
        scr = game.screen(canvas)

# Events
def keypress_event(e):
    if (current_screen == "title"):
        if (e.keysym == "Return"):
            change_ui("game")
    elif (current_screen == "game"):
        if (e.keysym == "Escape"):
            change_ui("title")

def mouse_click_event(e):
    canvas.create_text(e.x, e.y, text=f"{e.x}, {e.y}", font=("Unifont",20), fill="white")
    
        


root.bind("<KeyPress>", keypress_event)

root.bind("<Button-1>", mouse_click_event)

scr = title.screen(canvas)

GAME_FOLDER = os.path.dirname(__file__)
MUSICS_FOLDER = os.path.join(GAME_FOLDER, "musics")
SE_FOLDER = os.path.join(GAME_FOLDER, "sounds")

mixer.init()
music = mixer.Sound(os.path.join(MUSICS_FOLDER, "title.wav"))
sound_back = mixer.Sound(os.path.join(SE_FOLDER, "back.wav"))
sound_done = mixer.Sound(os.path.join(SE_FOLDER, "done.wav"))

music.play()

update()
root.mainloop()