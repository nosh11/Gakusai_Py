from enum import Enum
from common.utils.file_manager import get_asset_file_path, get_resource_file_path
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
        self.font = font

    def get_font(self, size=32) -> pygame.font.Font:
        file_path = get_asset_file_path(f"fonts/{self.font}")
        return pygame.font.Font(file_path, size)
    
    def get_display_name(self) -> str:
        return self.displayname

def get_lang_texts(lang: Language) -> dict:
    file_path = get_resource_file_path(f"lang/{lang.lang_id}.yml")
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.load(f, Loader=yaml.FullLoader)
    
def get_screen_texts(screen_id: str, lang: Language) -> dict:
    file_path = get_resource_file_path(f"lang/screen/{screen_id}/{lang.lang_id}.yml")
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.load(f, Loader=yaml.FullLoader)
    
def get_langs() -> list:
    return [lang.name for lang in Language]