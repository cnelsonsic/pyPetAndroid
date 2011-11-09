
from helpers import load_sliced_sprites
import pygame

class AnimatedSprite(pygame.sprite.DirtySprite):
    def __init__(self, image, frame_width=16, frame_height=16, fps=10):
        super(AnimatedSprite, self).__init__()
        self._images = load_sliced_sprites(w=frame_width, h=frame_height, filename=image)

        # Track the time we started, and the time between updates.
        # Then we can figure out when we have to switch the image.
        self._start = pygame.time.get_ticks()
        self._delay = 1000 / fps
        self._last_update = 0
        self._frame = 0
        self.rect = pygame.Rect(0, 0, frame_width, frame_height)
        self.image = self._images[0]

        # Call update to set our first image.
        self.update()

    def update(self):
        # Note that this doesn't work if it's been more that self._delay
        # time between calls to update(); we only update the image once
        # then, but it really should be updated twice.

        t = pygame.time.get_ticks()
        if t - self._last_update > self._delay:
            self._frame += 1
            if self._frame >= len(self._images): self._frame = 0
            self.image = self._images[self._frame]
            self._last_update = t
            self.dirty = 1
