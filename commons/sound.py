from pygame import mixer

class MusicPlayer:
    def __init__(self, filename):
        mixer.init()
        mixer.music.load(filename)
        mixer.music.play(1)
    def loop(self,time=0.0):
        pos = mixer.music.get_pos()
        if int(pos) == -1:
            mixer.music.play(-1, time)