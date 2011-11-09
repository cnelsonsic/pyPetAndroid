from __future__ import division
import pygame

import random

from colors import COLORS

# Import the android module. If we can't import it, set it to None - this
# lets us test it, and check to see if we want android-specific behavior.
try:
    import android
except ImportError:
    android = None

# Project imports
from helpers import load_image
from nodes import SpriteNode, ROOT
from pet import Pet

# Event constant.
TIMEREVENT = pygame.USEREVENT

# The FPS the game runs at.
FPS = 30

# Window Width/Height
WIDTH = 0
HEIGHT = 0
RATIO = 1

# Color constants.
RED = (255, 0, 0, 255)
GREEN = (0, 255, 0, 255)

def _random_color():
    return [random.randint(1, 255) for _ in xrange(3)]

def _random_rect():
    smallest = min(HEIGHT, WIDTH)
    left = random.randint(0, smallest)
    top = random.randint(0, smallest)
    width = min(WIDTH, random.randint(0, WIDTH-left))
    height = min(HEIGHT, random.randint(0, HEIGHT-top))
    print left, top, left+width, top+height
    return pygame.Rect(left, top, width, height)

def setup_ui():
    # Main Background
    # A, B, C Buttons
    # LCD Background
    pass

def setup_pet():
    # Initialize Pet object
    # Attach it to the LCD Node
    pet = Pet()
    ROOT.children.append(pet)
    pass

def update_ui():
    pass

def setup():
    for i in xrange(20):
        continue
        #ROOT.children.append(RectNode(_random_color(), _random_rect()))

        sprite = pygame.sprite.DirtySprite(SpriteNode.spritegroup)
        sprite.image, sprite.rect = load_image("icon.png")
        node = SpriteNode(sprite)
        x, y = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
        sprite.rect.center = x, y
        ROOT.children.append(node)

    for c in ROOT.children:
        print c.sprite.rect

    setup_ui()
    setup_pet()

def update():
    update_ui()
    ROOT.update()

def draw():
    ROOT.draw()
    pygame.display.update()
    pygame.display.flip()

def handle_click():
    print "MouseClick:", pygame.mouse.get_pos()

def main():
    pygame.init()

    print pygame.display.list_modes()
    if not android:
        # Pick a size one smaller than our desktop to save room for WM stuff.
        modes = pygame.display.list_modes()
        if len(modes) > 1: mode = modes[1]
        else: mode = modes[0]
        screen_w, screen_h = mode
    else:
        # Fullscreen always
        _info = pygame.display.Info()
        screen_w = _info.current_w
        screen_h = _info.current_h
    global WIDTH, HEIGHT
    WIDTH = screen_w
    HEIGHT = screen_h

    #This means we must scale everything horizontally by screen_ratio
    global RATIO
    RATIO = WIDTH/HEIGHT

    # Set the screen size.
    pygame.display.set_mode((screen_w, screen_h))

    # Map the back button to the escape key.
    if android:
        android.init()
        android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)

    # Use a timer to control FPS.
    pygame.time.set_timer(TIMEREVENT, int(1000 / FPS))

    # Set up our scenegraph
    setup()

    while True:

        ev = pygame.event.wait()

        # Android-specific:
        if android:
            if android.check_pause():
                android.wait_for_resume()

        # Draw the screen based on the timer.
        if ev.type == TIMEREVENT:
            update()
            draw()

        # When the touchscreen is pressed, change the color to green.
        elif ev.type == pygame.MOUSEBUTTONDOWN:
            handle_click()

        # When the user hits back, ESCAPE is sent. Handle it and end
        # the game.
        elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
            break

# This isn't run on Android.
if __name__ == "__main__":
    import doctest
    doctest.testmod()
    main()
