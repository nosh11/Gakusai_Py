import pygame
from game.common.scene import Scene
from common.model.stage import StageMap, Stage


class MapScene(Scene):
    def __init__(self, app_controller, language, screen_id: str = "map"):
        super().__init__(app_controller, language, screen_id)

    def load_text(self):
        pass

    def setup(self):
        self.display_surface.fill((100, 150, 30))

        self.map_data = StageMap()
        self.map_data.add_stage(Stage(0, "Test", (100, 100)))
        self.map_data.add_stage(Stage(1, "Test_2", (500, 600)))
        self.map_data.add_egde((0, 1))

    def display(self):
        self.display_surface.fill((100, 150, 30))

        for stage in self.map_data.stages:
            pygame.draw.circle(self.display_surface, (255, 0, 0), stage.pos, 50)
            font = pygame.font.Font(None, 20)
            text_surface = font.render(stage.name, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=stage.pos)
            self.display_surface.blit(text_surface, text_rect)

        for edge in self.map_data.edges:
            start_stage = self.map_data.stages[edge[0]]
            end_stage = self.map_data.stages[edge[1]]
            pygame.draw.line(self.display_surface, (255, 255, 255), start_stage.pos, end_stage.pos, 1)
        pygame.display.flip()

    def tick(self):
        pass

    def define_text_labels(self):
        pass