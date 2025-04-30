import pygame

from common.models.talk.message import Message
from common.utils.file_manager import get_asset_file_path
from game.commons.widget import UIWidget
from game.consts.screen_settings import SCREEN_HEIGHT, SCREEN_WIDTH
from game.ui.scenes.components.text_line import MessageSingleLine
        
WIDTH_PADDING = 0.025


class MessageSenderLabel:
    def __init__(self, sender):
        self.sender = sender
        self.surface = None

    def render(self):
        # テキストレンダリング（前景色:白、背景色:黒）
        sender_label = self.sender.font.render(
            self.sender.name, True, (255, 255, 255, 255), (0, 0, 0, 255)
        )
        # 表示領域を用意（テキスト幅に余白を追加）
        self.surface = pygame.Surface(
            (sender_label.get_width() + 50, SCREEN_HEIGHT * 0.1)
        )
        rect = sender_label.get_rect()
        # テキストを中央に配置
        rect.center = (
            self.surface.get_width() // 2,
            self.surface.get_height() // 2,
        )
        self.surface.blit(sender_label, rect)
        # 枠線を描画
        pygame.draw.rect(self.surface, (0, 0, 0, 255), self.surface.get_rect(), 5)
        return self.surface


class MessageBox(UIWidget):
    def __init__(self, view_display_surface: pygame.Surface):
        super().__init__(view_display_surface, SCREEN_WIDTH * WIDTH_PADDING, SCREEN_HEIGHT * 0.6)
        self.set_showing_image(pygame.Surface((SCREEN_WIDTH * (1 - WIDTH_PADDING*2), SCREEN_HEIGHT * 0.35)).convert_alpha())
        self.message_surface: pygame.Surface = pygame.Surface((SCREEN_WIDTH * (1 - WIDTH_PADDING*2), SCREEN_HEIGHT * 0.2))
        self.sender_surface: pygame.Surface = None

        self.messages: list[Message] = []
        self.current_message: Message = None
        self.message_lines: list[MessageSingleLine] = []
        self.font = pygame.font.Font(None, 36)  # フォントの設定（適宜変更）

    def add_message(self, message: Message):
        self.messages.append(message)
        if self.current_message is None:
            self.current_message = self.messages.pop(0)
            self.reset_sender_surface()
            self.split_message_into_lines()

    def split_message_into_lines(self):
        self.message_lines = []
        if self.current_message:
            words = self.current_message.text.split(' ')
            line = ""
            for word in words:
                test_line = f"{line} {word}".strip()
                test_surface = self.font.render(test_line, True, (255, 255, 255))
                if test_surface.get_width() > self.message_surface.get_width():
                    self.message_lines.append(MessageSingleLine(line, self.font))
                    line = word
                else:
                    line = test_line
            if line:
                self.message_lines.append(MessageSingleLine(line, self.font))

    def next(self):
        if self.messages:
            self.show_message(self.messages.pop(0))
        else:
            self.current_message = None
            self.is_hidden = True

    def show_message(self, message: Message):
        self.current_message = message
        self.split_message_into_lines()
        self.reset_sender_surface()

    def reset_sender_surface(self):
        if self.current_message.sender is not None:
            # MessageSenderLabelを利用してsender_surfaceを生成
            label = MessageSenderLabel(self.current_message.sender)
            self.sender_surface = label.render()
        else:
            self.sender_surface = None

    def is_text_complete(self) -> bool:
        return all(line.current_length >= len(line.message_text) for line in self.message_lines)

    def show_text_complete(self):
        for line in self.message_lines:
            line.render_complete()

    def update(self):
        self.showing_image.fill((100, 100, 100, 0))
        if self.current_message is None:
            return False

        # Message Sender
        if self.sender_surface is not None:
            self.showing_image.blit(self.sender_surface, (0, 0))

        # Message Text
        self.message_surface.fill((0, 0, 0, 255))
        y_offset = 0
        for line in self.message_lines:
            if not line.update_message():
                continue
            if line.surface:
                self.message_surface.blit(line.surface, (10, y_offset))
            y_offset += self.font.get_linesize()

        self.showing_image.blit(self.message_surface, (0, SCREEN_HEIGHT * 0.15))
        return True