class AppState:
    def __init__(self, current_state: str):
        self.current_state = current_state
        self.lang = 0
    def get(self):
        return self.current_state
    def set(self, state):
        self.current_state = state