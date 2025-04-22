from game.commons.view import Scene
from game.ui.scenes import *

def create_title_scene_group(app_controller):
    title_scene_group = SceneGroup()
    title_scene_group.add(TitleScene(app_controller))
    title_scene_group.add(PauseScene(app_controller))
    title_scene_group.add(GameScene(app_controller))
    return title_scene_group

class SceneGroup:
    def __init__(self, scenes: map[str, Scene]):
        self.children: map[str, Scene] = scenes
        self.__showing_scene_index: str = self.children[0].get_name()

    def add(self, child):
        self.children.append(child)

    def remove(self, child):
        self.children.remove(child)

class SceneGroupHolder:
    def __init__(self, scene_group: SceneGroup):
        self.scene_group = scene_group

    def get_scene(self, name: str) -> Scene:
        return self.scene_group.children[name]

    def get_showing_scene(self) -> Scene:
        return self.scene_group.children[self.scene_group.__showing_scene_index]

    def set_showing_scene(self, name: str):
        self.scene_group.__showing_scene_index = name

    def set_scene_group(self, scene_group: SceneGroup):
        self.scene_group = scene_group