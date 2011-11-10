
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
        self.speed = 5

        # FunStats(tm)
        self.hunger = 50
        self.social = 50
        self.bladder = 50
        self.hygiene = 50
        self.energy = 50

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
        self.tick_stats()
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
            self.wander_direction = random.choice(("left", "right", "up", "down"))
            print self.wander_direction

        #If heading right and x is less than 1/4 of screen width, keep heading right.
        # And vice versa.

        direct = self.wander_direction
        print direct
        modx, mody = 0, 0
        if direct == "left":
            modx = -1
        elif direct == "right":
            modx = +1
        elif direct == "up":
            mody = -1
        elif direct == "down":
            mody = +1
        
        print modx, mody 

        self.sprite.rect.x += (modx*self.speed)
        self.sprite.rect.y += (mody*self.speed)
        
        print self.sprite.rect.x, self.sprite.rect.y
        print self.sprite.rect.left, self.sprite.rect.right, self.sprite.rect.top, self.sprite.rect.bottom
        print WIDTH, HEIGHT

        # Hard limit on boundaries.
        if self.sprite.rect.left <= 0:
            self.sprite.rect.left = 0
            self.wander_direction = "right"

        if self.sprite.rect.top <= 0:
            self.sprite.rect.top = 0
            self.wander_direction = "down"

        if self.sprite.rect.right >= WIDTH:
            self.sprite.rect.right = WIDTH
            self.wander_direction = "left"

        if self.sprite.rect.bottom >= HEIGHT:
            self.sprite.rect.bottom = HEIGHT
            self.wander_direction = "up"

        print self.sprite.rect.left, self.sprite.rect.right, self.sprite.rect.top, self.sprite.rect.bottom
        print
        # TODO: Update active sprite depending on which direction we're facing.

    def tick_stats(self):
        '''This ticks down the SuperFunTimeStats.'''
        stats = (self.hunger, self.social, self.bladder, self.hygiene, self.energy)
        for s in stats:
            s -= 1

        print "Happiness: %d" % (sum(stats)/len(stats))
