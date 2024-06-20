import pygame

# Screen
SCREEN_WIDTH  = 1280
SCREEN_HEIGHT = 720
TILE_SIZE = 32


bullet_speed = {"up": (0, -1, 90), 
                "down": (0, 1, 270), 
                "right": (1, 0, 0), 
                "left": (-1, 0, 180)}


# How To Play
# 0 -> JP, 1 -> EN

BACK = {0: "もどる", 1: "Back"}
LANG = {0: "English", 1: "にほんご"}

HOW_TO_PLAY = {
        0: [
            "あそびかた",
            "",
            "すぺーすきー で じゅうをうてます",
            "せまりくるてき から べっどを",
            "まもりましょう"
        ],
        1: [
            "How To Play",
            "",
            "Press the space key to shoot the gun.",
            "Defend the bed from enemies"
        ]
}
