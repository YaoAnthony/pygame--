import pygame
from code.settings import *

class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, groups, surf=None, z=LAYERS['main']):
        super().__init__(groups)
        # 如果没有提供 surf，则创建一个黑色背景的默认 Surface
        if surf is None:
            surf = pygame.Surface((100, 100)).convert_alpha()  # 指定宽高，例如 100x100
            surf.fill((0, 0, 0))  # 填充为黑色
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z
