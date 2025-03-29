import pygame
from commons.view import View
from commons.widget import UIWidget
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from commons.languages import get_lang_texts


class Sender:
    def __init__(self, name: str, font: pygame.font.Font, color=(255, 255, 255)):
        self.name = name
        self.color = color
        self.font = font


class Message:
    def __init__(self, text: str, sender: Sender):
        self.sender = sender
        self.text = text
        self.color = sender.color
        self.font = sender.font

    def __init__(self, text: str, font: pygame.font.Font, color=(255, 255, 255), sender=None):
        self.sender = sender
        self.color = color
        self.text = text
        self.font = font

class MessageManager:
    def __init__(self):
        self.messages: list[Message] = []

    def add_message(self, message: Message):
        self.messages.append(message)
        

class MessageBox(UIWidget):
    def __init__(self, view_display_surface: pygame.Surface, x, y):
        self.view_display_surface = view_display_surface
        padding = 100
        self.pos = (x + padding, y + padding)
        self.showing_image = pygame.Surface((SCREEN_WIDTH - padding, SCREEN_HEIGHT // 4 - padding))

        self.current_message: Message = None
        self.current_chars = 0

    def show_message(self, message: Message):
        self.current_message = message
        self.current_chars = 0
        self.showing_image = self.showing_image.convert_alpha()

    def update(self):
        message = self.current_message
        self.showing_image.fill((0, 0, 0))
        if message is None:
            return False
        
        text_surface: pygame.Surface
        if self.current_chars >= len(self.current_message.text):
            text_surface = message.font.render(message.text, True, message.color)
        else:
            text_surface = message.font.render(message.text[:self.current_chars], True, message.color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (10, 10)  # Add padding for better visibility
        self.showing_image.blit(text_surface, text_rect)
        self.view_display_surface.blit(self.showing_image, self.pos)
        self.current_chars += 1
        return True

class GameView(View):
    def load_text(self):
        pass

    def setup(self):
        self.message = MessageManager()
        desc = get_lang_texts(self.get_language())["pause_menu"]["description"]
        for text in desc:
            message = Message(text, self.get_language().get_font(20))
            self.message.add_message(message)
        self.message_box = MessageBox(self.display_surface, 0, 0)
        self.space_pressed = False
        self.show_next_message()

    def display(self):
        self.display_surface.fill((224, 224, 224))
        self.message_box.update()
        self.message_box.draw()

    def tick(self):
        for event in pygame.event.get():
            # space pressed
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.handle_space_key()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self._app_controller.set_next_view(1)
            else:
                self.space_pressed = False

    def handle_space_key(self):
        print("space pressed")
        if self.space_pressed:
            return
        self.space_pressed = True
        self.show_next_message()

    def show_next_message(self):
        if self.message.messages:
            message = self.message.messages.pop(0)
            self.message_box.show_message(message)
        else:
            message = Message("qwqweucqroivwrwmqeorciweyqrwinowqencrwqetcwrwdiwmeynweiywoqcm", self.get_language().get_font(20))
            self.message_box.show_message(message)