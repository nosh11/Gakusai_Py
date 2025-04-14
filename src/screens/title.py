import random
import pygame
from commons.view import View
from commons.file_manager import get_static_file_path
from model.languages import Language
from settings import *

credit_surface: pygame.Surface

def make_credit_surface():
    global credit_surface
    credit_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    font_console = pygame.font.Font(get_static_file_path(f"fonts/unifont.otf"), 10)
    font_console.set_bold(True)
    credit_surface.blit(font_console.render("credit", True, (255, 255, 255)), (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
    credit_surface.blit(font_console.render("press Enter to return", True, (255, 255, 255)), (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 50))

    text = """
    croissant-boy

    制作 nosssy
    音楽制作 nosssy
    その他 nosssy
    special thanks
    coffee
    additional thanks to the community
    for their support and feedback.
    ありがとうございます。
    arigato gozaimasu.
    """

    font_console = pygame.font.Font(get_static_file_path(f"fonts/unifont.otf"), 20)
    for line in text.strip().split('\n'):
        credit_surface.blit(font_console.render(line, True, (255, 255, 255)), (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 30 * text.strip().split('\n').index(line)))




class TitleView(View):
    def define_text_labels(self):
        font = self.get_language().get_font(50)

        choices = [
            "start", "continue", "sound_room", "options", "quit"
        ]

        self.choices = {c: font.render(self.get_text(c), True, (0, 0, 0)) for c in choices}
        

    def setup(self):
        self.display_surface.fill((100, 150, 30))
        self.background_image = pygame.image.load(get_static_file_path("img/croissant_boy.png"))
        self.current_choice = 0
                             

    def display(self):
        self.display_surface.blit(self.background_image, (0, 0))

        row = 0
        for choice in self.choices:
            text_surface = self.choices[choice]
            self.display_surface.blit(text_surface, (SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT // 2 + row * 50))
            row += 1

        # 選択中の選択肢の横に > を表示
        selected_choice = list(self.choices.keys())[self.current_choice]
        selected_text_surface = self.choices[selected_choice]
        selected_text_surface = self.get_language().get_font(50).render(f">", True, (255, 0, 0))
        self.display_surface.blit(selected_text_surface, (SCREEN_WIDTH // 2 + 130, SCREEN_HEIGHT // 2 + self.current_choice * 50))
        
            


    def tick(self):
        # 上下キーで選択肢を移動
        if pygame.event.get(pygame.KEYDOWN):
            if pygame.key.get_pressed()[pygame.K_RETURN]:
                if self.current_choice == 0:
                    self._app_controller.set_next_view("game")
                elif self.current_choice == 1:
                    self._app_controller.set_next_view("continue")
                elif self.current_choice == 2:
                    self._app_controller.set_next_view("sound_room")
                elif self.current_choice == 3:
                    self._app_controller.set_transition_seconds((0.02, 0.02))
                    self._app_controller.set_transition_type("fade")
                    self._app_controller.set_next_view("options")
                elif self.current_choice == 4:
                    self._app_controller.quit()
            elif pygame.key.get_pressed()[pygame.K_UP]:
                self.current_choice = (self.current_choice - 1) % len(self.choices)
            elif pygame.key.get_pressed()[pygame.K_DOWN]:
                self.current_choice = (self.current_choice + 1) % len(self.choices)

class OptionView(View):
    def define_text_labels(self):
        font = self.get_language().get_font(50)

        choices = [
            "language", "credit", "back"
        ]

        self.choices = {c: font.render(self.get_text(c), True, (0, 0, 0)) for c in choices}
        self.is_showing_credit = False
        

    def setup(self):
        self.current_choice = 0
        make_credit_surface()
                             

    def display(self):
        if self.is_showing_credit:
            self.display_surface.blit(credit_surface, (0, 0))
            return
        self.display_surface.fill((100, 150, 30))
        row = 0
        for choice in self.choices:
            text_surface = self.choices[choice]
            self.display_surface.blit(text_surface, (SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT // 2 + row * 50))
            row += 1

        # 選択中の選択肢の横に > を表示
        selected_choice = list(self.choices.keys())[self.current_choice]
        selected_text_surface = self.choices[selected_choice]
        selected_text_surface = self.get_language().get_font(50).render(f">", True, (255, 0, 0))
        self.display_surface.blit(selected_text_surface, (SCREEN_WIDTH // 2 + 130, SCREEN_HEIGHT // 2 + self.current_choice * 50))

        
            


    def tick(self):
        # 上下キーで選択肢を移動
        if pygame.event.get(pygame.KEYDOWN):
            if pygame.key.get_pressed()[pygame.K_RETURN]:
                if self.current_choice == 0:
                    languages = list(Language)
                    lang = languages[(languages.index(self.get_language()) + 1) % len(languages)]
                    self._app_controller.set_language(lang)
                elif self.current_choice == 1:
                    self.is_showing_credit = not self.is_showing_credit
                    if self.is_showing_credit:
                        self.display_surface.blit(credit_surface, (0, 0))
                    else:
                        self.display_surface.fill((100, 150, 30))
                elif self.current_choice == 2:
                    self._app_controller.set_transition_seconds((0.02, 0.02))
                    self._app_controller.set_transition_type("fade")
                    self._app_controller.set_next_view("title")
            elif self.is_showing_credit:
                return
            elif pygame.key.get_pressed()[pygame.K_UP]:
                self.current_choice = (self.current_choice - 1) % len(self.choices)
            elif pygame.key.get_pressed()[pygame.K_DOWN]:
                self.current_choice = (self.current_choice + 1) % len(self.choices)