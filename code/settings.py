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
            "スペースキー: 銃を撃つ",
            "矢印キー: 移動",
            "",
            "降ってくるりんごを キャッチ または",
            "狙撃 すると ポイントが溜まります",
            "がいこつは 気合で さけましょう"
        ],
        1: [
            "How To Play",
            "",
            "Space key: Shoot the gun",
            "Arrow keys: Move",
            "",
            " - Catch or Shoot falling apples!",
            " - Avoid skulls!"
        ]
}
