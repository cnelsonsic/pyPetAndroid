
import os
import pygame

_IMAGES = {}
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if fullname in _IMAGES:
        return (_IMAGES[fullname][0], _IMAGES[fullname][1].copy())

    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message

    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)

    _IMAGES[fullname] = (image, image.get_rect())

    return image, image.get_rect().copy()


def load_sliced_sprites(w, h, filename):
    '''
    Specs :
        Master can be any height.
        Sprites frames width must be the same width
        Master width must be len(frames)*frame.width
    '''
    images = []
    master_image = load_image(filename)[0].convert_alpha()

    master_width, master_height = master_image.get_size()
    for i in xrange(int(master_width/w)):
        images.append(master_image.subsurface((i*w,0,w,h)))
    return images
