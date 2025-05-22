import pygame
from core.model.stage import StageMap, Stage
from game.app.scene import Scene


class MapScene(Scene):
    def get_screen_id(self) -> str:
        return "map"

    def load_text(self):
        pass

    def setup(self):
        self.root_surface.fill((100, 150, 30))

        self.map_data = StageMap()
        self.map_data.add_stage(Stage(0, "Test", (100, 100)))
        self.map_data.add_stage(Stage(1, "Test_2", (500, 600)))
        self.map_data.add_egde((0, 1))

    def draw(self):
        self.root_surface.fill((100, 150, 30))

        for stage in self.map_data.stages:
            pygame.draw.circle(self.root_surface, (255, 0, 0), stage.pos, 50)
            font = pygame.font.Font(None, 20)
            text_surface = font.render(stage.name, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=stage.pos)
            self.root_surface.blit(text_surface, text_rect)

        for edge in self.map_data.edges:
            start_stage = self.map_data.stages[edge[0]]
            end_stage = self.map_data.stages[edge[1]]
            pygame.draw.line(self.root_surface, (255, 255, 255), start_stage.pos, end_stage.pos, 1)
        pygame.display.flip()

    def tick(self):
        if pygame.event.get(pygame.KEYDOWN):
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                self.app.back_scene()