from enum import Enum
import pygame
import yaml

class Language(Enum):
    # (id, language-id, name, font)
    Japanese = (1, "ja-jp", "日本語", "unifont.otf")
    English = (2, "en-us", "English", "unifont.otf")

    def __init__(self, id: int, lang_id: str, name: str, font: str):
        self.id = id
        self.lang_id = lang_id
        self.displayname = name
        self.__font = font

    def get_font(self, size=32) -> pygame.font.Font:
        return pygame.font.Font(f"static/fonts/{self.__font}", size)
    
    def get_display_name(self) -> str:
        return self.displayname

def get_lang_texts(lang: Language) -> dict:
    with open(f"static/lang/{lang.lang_id}.yml", "r", encoding="utf-8") as f:
        return yaml.load(f, Loader=yaml.FullLoader)
    
def get_langs() -> list:
    return [lang.name for lang in Language]
