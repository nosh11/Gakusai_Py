import pygame
import app_state
from commons.file_manager import get_static_file_path
from commons.view import View
from commons.widget import UIWidget
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from model.languages import get_lang_texts

class Sender:
    def __init__(self, name: str, font: pygame.font.Font, color=(255, 255, 255)):
        self.name = name
        self.color = color
        self.font = font

class Message:
    def __init__(self, text: str, font: pygame.font.Font, color=(255, 255, 255), sender: str=None):
        self.sender = sender
        self.color = color
        self.text = text
        self.font = font
        
WIDTH_PADDING = 0.025

class MessageBox(UIWidget):
    def __init__(self, view_display_surface: pygame.Surface):
        super().__init__(view_display_surface, SCREEN_WIDTH * WIDTH_PADDING, SCREEN_HEIGHT * 0.6)
        self.set_showing_image(pygame.Surface((SCREEN_WIDTH * (1 - WIDTH_PADDING*2), SCREEN_HEIGHT * 0.35)).convert_alpha())
        self.message_surface: pygame.Surface = pygame.Surface((SCREEN_WIDTH * (1 - WIDTH_PADDING*2), SCREEN_HEIGHT * 0.2))
        self.sender_surface: pygame.Surface  = None

        self.messages: list[Message] = []
        self.current_message: Message = None
        self.current_chars = 0

    def add_message(self, message: Message):
        self.messages.append(message)
        if self.current_message == None:
            self.current_message = self.messages.pop(0)
            self.reset_sender_surface()
    
    def next(self):
        if self.messages:
            self.show_message(self.messages.pop(0))
        else:
            self.current_message = None
            self.is_hidden = True

    def show_message(self, message: Message):
        self.current_message = message
        self.current_chars = 0
        self.showing_image = self.showing_image.convert_alpha()
        self.reset_sender_surface()

    def reset_sender_surface(self):
        if self.current_message.sender != None:
            sender_label = self.current_message.font.render(self.current_message.sender, True, (255, 255, 255, 255), (0, 0, 0, 255))
            self.sender_surface = pygame.Surface((sender_label.get_width() + 50, SCREEN_HEIGHT * 0.1))
            rect = sender_label.get_rect()
            rect.center = self.sender_surface.get_width() // 2, self.sender_surface.get_height() // 2
            self.sender_surface.blit(sender_label, rect)
            pygame.draw.rect(self.sender_surface, (0, 0, 0, 255), self.sender_surface.get_rect(), 5)
            print("sender is not none")
        else:
            print("sender is none")
            self.sender_surface = None

    # テキストが完全に表示しきったかどうか
    def is_text_complete(self) -> bool:
        if self.current_message is None:
            return False
        if self.current_chars >= len(self.current_message.text):
            return True
        return False
    
    # テキストを完全に表示する
    def show_text_complete(self):
        if self.current_message is None:
            return
        self.current_chars = len(self.current_message.text)

    def update(self):
        self.showing_image.fill((100, 100, 100, 0))
        message = self.current_message
        if message is None:
            return False
        
        # Message Sender
        if self.sender_surface != None:
            self.showing_image.blit(self.sender_surface, (0, 0))


        self.message_surface.fill((0, 0, 0, 255))
        text_surface: pygame.Surface
        if self.current_chars >= len(self.current_message.text):
            text_surface = message.font.render(message.text, True, message.color)
        else:
            text_surface = message.font.render(message.text[:self.current_chars], True, message.color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (10, SCREEN_HEIGHT * 0.025)
        self.message_surface.blit(text_surface, text_rect)
        self.showing_image.blit(self.message_surface, (0, SCREEN_HEIGHT * 0.15))
        self.current_chars += 1
        return True


class GamePlayer:
    def __init__(self, view_surface):
        self.x = 0
        self.y = 0
        self.view_surface = view_surface
        self.surface = pygame.image.load(get_static_file_path("img/apple.png"))

    def move(self):
        if pygame.key.get_pressed()[pygame.K_UP]:
            self.y -= 10
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            self.y += 10
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.x -= 10
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.x += 10
    
    def draw(self):
        self.view_surface.blit(self.surface, (self.x, self.y))
        



SKIP_CD = 10

class GameView(View):
    def define_text_labels(self):
        font = self.get_language().get_font(50)
        pause_menu_label = font.render("test", True, (255, 255, 255))
        self.set_text_label("pause_menu", 
                             pause_menu_label)

    def setup(self):
        self.message_box = MessageBox(self.display_surface)
        desc = get_lang_texts(self.get_language())["pause_menu"]["description"]
        for text in desc:
            message = Message(text, self.get_language().get_font(50), sender="ゆに")
            self.message_box.add_message(message)
        self.space_pressed = False
        self.skip_pressed = False
        self.skip = False
        self.skip_cd = SKIP_CD
        self.player = GamePlayer(self.display_surface)

        self.background_image = pygame.image.load(get_static_file_path("img/haikei.png"))

    def display(self):
        self.display_surface.blit(self.background_image, (0, 0))
        self.message_box.update()
        self.message_box.draw()
        self.player.draw()

        self.display_surface.blit(
            self.get_text_label("pause_menu"),
            (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50)
        )

    def tick(self):
        self.player.move()
        if pygame.event.get(pygame.KEYDOWN):
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self.space_key_pressed()
            elif pygame.key.get_pressed()[pygame.K_a]:
                self.message_box.is_hidden = not self.message_box.is_hidden
            elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
                self._app_controller.set_transition_type("slide>slide")
                self._app_controller.set_transition_seconds((0.01, 0.01))
                self._app_controller.set_next_view("pause")
            elif pygame.key.get_pressed()[pygame.K_z]:
                self.z_key_pressed()
        else:
            self.space_pressed = False
            self.skip_pressed = False
        if self.skip:
            self.skip_cd -= 1
        if self.skip_cd <= 0:
            self.next_message()

    def space_key_pressed(self):
        if self.space_pressed:
            return
        self.space_pressed = True
        self.next_message()

    def next_message(self):
        if not self.message_box.is_text_complete():
            self.message_box.show_text_complete()
            return
        self.show_next_message()

    def z_key_pressed(self):
        if self.skip_pressed:
            return
        self.skip_pressed = True
        self.skip = not self.skip

    def show_next_message(self):
        self.skip_cd = SKIP_CD
        self.message_box.next()

    def on_load(self):
        if app_state.flags.get("bgm") != "bgm/bgm_2.wav":
            pygame.mixer.music.load(get_static_file_path("bgm/bgm_2.wav"))
            app_state.flags["bgm"] = "bgm/bgm_2.wav"
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.unpause()