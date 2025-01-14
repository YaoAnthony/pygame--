class Settings:
    def __init__(self, config):
        self.language = config.get("language", "中文")
        self.volume = config.get("volume", 0.5)

    def toggle_language(self):
        self.language = "English" if self.language == "中文" else "中文"

    def adjust_volume(self, amount):
        self.volume = max(0, min(1, self.volume + amount))
