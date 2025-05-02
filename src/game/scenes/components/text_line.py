import pygame


class MessageSingleLine:
    def __init__(self, message_text: str, font: pygame.font.Font):
        self.message_text: str = message_text
        self.current_length: int = 0
        self.surface: pygame.Surface = None
        self.font: pygame.font.Font = font

    def update_message(self):
        if self.current_length >= len(self.message_text):
            return False
        self.current_length += 1
        self.surface = self.font.render(self.message_text[:self.current_length], True, (255, 255, 255))
        return True

    def render_complete(self):
        self.surface = self.font.render(self.message_text, True, (255, 255, 255))
        self.current_length = len(self.message_text)