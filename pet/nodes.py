
import pygame

class Node(object):
    '''Node objects will only draw their children, and not themselves.
    Child nodes will be drawn on top of the parent node.
    There is no such thing as local coordinates.
    '''
    def __init__(self, name=""):
        self.children = []
        self.name = name

    def draw(self):
        for c in self.children:
            c.draw()

    def update(self):
        for c in self.children:
            c.update()

    def get_child(self, name):
        ''' get_child will get a Node's child that matches a given name.
        >>> n = Node("root")
        >>> child1 = Node("child1")
        >>> n.children.append(child1)
        >>> n.get_child("child1") == child1
        True

        It also works recursively:
        >>> child2 = Node("child2")
        >>> child1.children.append(child2)
        >>> n.get_child("child2") == child2
        True

        Names may be duplicated, but only the first instance of a name is returned.
        >>> child2notreally = Node("child2")
        >>> n.get_child("child2") == child2notreally
        False
        >>> n.get_child("child2") == child2
        True
        
        It also handles PEBCAK errors as well:
        >>> n.get_child(n.name) == n
        True

        '''

        if self.name == name:
            return self

        for c in self.children:
            if c.name == name:
                return c
            else:
                r = c.get_child(name)
                if r.name == name:
                    return r

class CustomNode(Node):
    def __init__(self, draw_func, draw_args=None, name=""):
        super(CustomNode, self).__init__()
        self.draw_func = draw_func
        self.draw_args = draw_args

    def draw(self):
        if self.draw_func and self.draw_args:
            self.draw_func(*self.draw_args)
        super(CustomNode, self).draw()

    @staticmethod
    def make_rectnode(color, rect, linewidth=0, name=""):
        '''Returns an instance of CustomNode set up to act like a RectNode.
        '''
        def _draw_rect(color, rect, linewidth=0):
            pygame.draw.rect(pygame.display.get_surface(), color, rect, linewidth)

        return CustomNode(_draw_rect, color, rect, linewidth, name=name)

class RectNode(Node):
    def __init__(self, color, rect, linewidth=0):
        super(RectNode, self).__init__()
        self.color = color
        self.rect = rect
        self.linewidth = linewidth

    def draw(self):
        pygame.draw.rect(pygame.display.get_surface(),
                self.color, self.rect, self.linewidth)
        super(RectNode, self).draw()

class SpriteNode(Node):
    spritegroup = pygame.sprite.LayeredDirty()
    drawn_group = False

    def collide(self, x=None, y=None, rect=None):
        if x and y:
            for s in self.spritegroup.sprites:
                if s.collidepoint(x, y):
                    return s
        elif rect:
            for s in self.spritegroup.sprites:
                if s.colliderect(rect):
                    return s

    def __init__(self, sprite, name=""):
        super(SpriteNode, self).__init__()
        self.sprite = sprite
        self.sprite.add(self.spritegroup)

    def draw(self):
        # This is drawn automatically by the draw() function,
        # which draws the spritegroup.
        if self.drawn_group is False:
            self.spritegroup.draw(pygame.display.get_surface())
            self.drawn_group = True
        super(SpriteNode, self).draw()

    def collide_point(self, x, y):
        return self.sprite.collidepoint(x, y)

    def collide_rect(self, rect):
        return self.sprite.colliderect(rect)


    def update(self):
        self.spritegroup.update()
        self.drawn_group = False
        super(SpriteNode, self).update()


# Root node for free
ROOT = Node("root")
