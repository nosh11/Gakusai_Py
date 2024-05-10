import random

color_1 = "#72a1d3"
color_2 = "#777777"

def screen(canvas):
    canvas["bg"] = color_2
    canvas.create_text(250, 220, text="何かのゲーム", font=("adLib WGL4 BT",50), fill="white")
    canvas.create_text(250, 280, text="Enter で開始", font=("adLib WGL4 BT",20), fill="white")
    canvas.pack()

    def create_title(screen_timer):
        if screen_timer % 30 == 0:
            rx = random.randint(50,450)
            rz = random.randint(50,450)
            if random.random() > 0.8:
                canvas.create_rectangle(rx,rz,rz,rx,outline="white")
            else:
                canvas.create_arc(rx,rz,rz,rx,outline="white",start=random.randint(0,360))
        canvas.delete("loop")
        canvas.create_text(100, 50, text=f"timer:{screen_timer}", font=("adLib WGL4 BT",20), fill="white", tag="loop")
    return create_title