from appstats import ViewManager

class AppController:
    def __init__(self, app_stats: ViewManager):
        self.__app_stats = app_stats

    def set_next_view(self, view: int):
        self.__app_stats.set_current_view(view)

    def get_app_stats(self) -> ViewManager:
        return self.__app_stats