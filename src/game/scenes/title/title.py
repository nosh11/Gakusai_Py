import pygame
from game.app.scene import Scene
from common.util.file_manager import get_asset_file_path
from game.consts import SCREEN_WIDTH, SCREEN_HEIGHT
from game.scenes.title.choice import Choice, QuitChoice, SceneChangeChoice, ScenePushChoice
from game.scenes.title.option import OptionScene

class TitleScene(Scene):
    def get_screen_id(self) -> str:
        return "title"

    def setup(self):
        self.root_surface.fill((100, 150, 30))
        self.background_image = pygame.image.load(get_asset_file_path("img/croissant_boy.png"))
        self.choices: list[Choice] = [
            ScenePushChoice(self.app, "options", OptionScene),
            QuitChoice(self.app, "quit")
        ]
        self.current_choice = 0
        self.cursor = pygame.font.Font(self.app.get_language().get_font(), 50).render(f">", True, (255, 0, 0))

    def draw(self):
        self.root_surface.blit(self.background_image, (0, 0))
        row = 0
        for choice in self.choices:
            self.root_surface.blit(choice.label, (SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT // 2 + row * 50))
            row += 1
        self.root_surface.blit(self.cursor, (SCREEN_WIDTH // 2 + 130, SCREEN_HEIGHT // 2 + self.current_choice * 50))

    def tick(self):
        # 上下キーで選択肢を移動
        if pygame.event.get(pygame.KEYDOWN):
            if pygame.key.get_pressed()[pygame.K_RETURN]:
                print("selected")
                choice = self.choices[self.current_choice]
                choice.on_select()
            elif pygame.key.get_pressed()[pygame.K_UP]:
                self.current_choice = (self.current_choice - 1) % len(self.choices)
                self.draw()
            elif pygame.key.get_pressed()[pygame.K_DOWN]:
                self.current_choice = (self.current_choice + 1) % len(self.choices)
                self.draw()