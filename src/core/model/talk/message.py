class Message:
    def __init__(self, text: list[str], sender_name: str, font: str, color: tuple = (255, 255, 255)):
        self.text = text
        self.sender_name = sender_name
        self.font = font
        self.color = color