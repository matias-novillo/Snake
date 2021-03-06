import random
import pygame

from atlas import Atlas
from game_object import GameObject
from game_object_factory import GameObjectFactory


@GameObjectFactory.register("AnimatedTexture")
class AnimatedTexture(GameObject):

    def __init__(self, asset, duration, scale=1.0):
        super().__init__(asset.frames[0][0], False, scale)
        self.dirty_image = False
        self.asset = asset
        self.duration = duration
        self.animation_time = 0
        self.is_playing = False
        self.atlas_index = 0

    def update(self, delta):
        super().update(delta)

        if self.is_playing:
            # Figure out which frame to use and set the image
            progress = 1.0 * self.animation_time / self.duration
            frames = self.asset.frames[self.atlas_index]
            frame_index = round(progress * len(frames))
            if frame_index < len(frames):
                self.image = frames[frame_index]
                if self.scale != 1 or self.heading != 0:
                    self.image = pygame.transform.rotozoom(frames[frame_index], self.heading, self.scale)
#                     self.image = pygame.transform.scale(self.image,
#                                                         (self.image.get_rect().width * self.scale,
#                                                          self.image.get_rect().height * self.scale))
#                     print("WARNING! Scaling asset frames!")
                self.rect = self.image.get_rect()

            self.rect = self.image.get_rect()
            self.rect.x = self.pos[0] - round(self.image.get_rect().width / 2)
            self.rect.y = self.pos[1] - round(self.image.get_rect().height / 2)

            # Update animation time
            self.animation_time = self.animation_time + delta
            if self.animation_time > self.duration:
                self.reset()
                self.kill()

    def play(self):
        self.is_playing = True
        self.set_heading(random.randint(0, 360))
        self.atlas_index = random.randint(0, len(self.asset.frames) - 1)

    def reset(self):
        """Resets the animation and leaves the object ready to play from the start."""
        self.animation_time = 0
        self.is_playing = False
        self.kill()
