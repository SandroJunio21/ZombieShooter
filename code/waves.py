from settings import PHASES

class WaveManager:
    def __init__(self):
        self.phase = 1
        self.wave = 1

    def get_data(self):
        return PHASES[self.phase]