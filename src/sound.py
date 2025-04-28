import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.channels = {}

    def play_background_music(self, file_path, volume=0.5, loop=-1):
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(loop)

    def stop_background_music(self):
        pygame.mixer.music.stop()

    def load_sound(self, name, file_path):
        self.sounds[name] = pygame.mixer.Sound(file_path)
        self.channels[name] = pygame.mixer.Channel(len(self.channels) + 1)

    def play_sound(self, name, volume=1.0, loop=False):
        if name in self.sounds:
            sound = self.sounds[name]
            channel = self.channels[name]
            if not channel.get_busy():
                sound.set_volume(volume)
                channel.play(sound, loops=-1 if loop else 0)

    def stop_sound(self, name):
        if name in self.channels:
            channel = self.channels[name]
            if channel.get_busy():
                channel.stop()

    def stop_all_sounds(self):
        pygame.mixer.stop()

    def pause_background_music(self):
        pygame.mixer.music.pause()

    def unpause_background_music(self):
        pygame.mixer.music.unpause()

    def set_background_music_volume(self, volume):
        pygame.mixer.music.set_volume(volume)

    def set_sound_effects_volume(self, volume):
        for sound in self.sounds.values():
            sound.set_volume(volume)

sound_manager = SoundManager()

sound_manager.load_sound('zombie_attack', 'assets/sounds/555420__tonsil5__zombie-hit-1.wav')
sound_manager.load_sound('zombie_die', 'assets/sounds/555412__tonsil5__zombie-death-1.wav')
sound_manager.load_sound('zombie_walk', 'assets/sounds/zombie-heavy-walking-moaning-dan-barracuda-1-00-15.mp3')
sound_manager.load_sound('player_walk', 'assets/sounds/walking-96582.mp3')
sound_manager.load_sound('player_run', 'assets/sounds/person-running-loop-245173.mp3')
sound_manager.load_sound('ambient', 'assets/sounds/forest-atmosphere-localization-poland-320813.mp3')
sound_manager.load_sound('round_start', 'assets/sounds/round_start.mp3')
