from tkinter import Tk, Canvas
from math import sin, radians
color_1 = "#72a1d3"
color_2 = "#777777"

def screen(canvas):
    canvas["bg"] = color_1
    canvas.create_text(300, 300, text="ゲームノスクリーン", font=("adLib WGL4 BT",50), fill="white")
    canvas.create_text(300, 400, text="Escape で戻る", font=("adLib WGL4 BT",20), fill="white")
    def create_title(screen_timer):
        canvas.delete("loop")
        canvas.create_text(100, 250+80*sin(radians(screen_timer*2)), text=r"_/^\_", font=("adLib WGL4 BT",20), fill="white", tag="loop")
        
    return create_title