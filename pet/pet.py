
import random
import pygame

from nodes import SpriteNode
from sprites import AnimatedSprite

# Don't want to bother importing from main.
FPS = 30

# Window Width/Height
WIDTH = 0
HEIGHT = 0

class Pet(SpriteNode):
    '''The node that represents our virtual pet.'''
    def __init__(self, name="pet"):
        sprite = AnimatedSprite("gfx/fawx/walk_side.png", frame_width=128, frame_height=126, fps=25*2)
        print sprite
        super(Pet, self).__init__(sprite, name)

        # Should preload walking and sleeping and eating sprites
        # Should pre-set a sprite to use.

        # Which direction are we currently wandering?
        self.wander_direction = "left" 

        # How many pixels should we move per tick.
        # TODO: Should be a percentage of the screen.
        self.speed = 5


        # Set up the height/width globals for this module.
        _info = pygame.display.Info()
        global WIDTH, HEIGHT
        HEIGHT = _info.current_h
        WIDTH = _info.current_w

        # Start in the center of the display.
        self.sprite.rect.center = (WIDTH/2, HEIGHT/2)
        print "Starting at %d, %d" % (WIDTH/2, HEIGHT/2)


    def update(self):
        # Stuff that needs to happen before drawing
        self.think()
        self.sprite.update()
        super(Pet, self).update()

    def think(self):
        # Brains go here.
        self.wander()

    def wander(self):
        '''This is the default action for a Pet.
        There is a small chance (once every few seconds or so) that it will
        change direction and start walking that way for a while.
        '''

        # TODO: Percentage chance to change direction depending on how far away 
        # from the center of the screen we are.
        # 100% chance to go right at x=0
        # 0% chance to go right at x=WIDTH/2
        # 100% chance to go left at x=WIDTH

        # 1 in (FPS*4) chance to change direction
        if random.randint(1, FPS*5) == 1:
            self.wander_direction = random.choice(("left", "right"))
            print self.wander_direction

        #If heading right and x is less than 1/4 of screen width, keep heading right.
        # And vice versa.

        dirmods = {"left": -1, "right": +1}
        for direction, mod in dirmods.iteritems():
            if direction == self.wander_direction:
                self.sprite.rect.x = self.sprite.rect.x+(mod*self.speed)
        
        # Hard limit on left and right boundaries.
        if self.sprite.rect.left <= 0:
            self.sprite.rect.left = 0
            self.wander_direction = "right"

        if self.sprite.rect.right >= WIDTH:
            self.sprite.rect.right = WIDTH
            self.wander_direction = "left"

        # TODO: Update active sprite depending on which direction we're facing.
