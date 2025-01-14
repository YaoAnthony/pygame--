import pygame
from code.settings import * 

class Overlay:
    '''
    叠加层类，用于显示各种菜单，道具等
    '''
    def __init__(self, screen,player = None):
        # General setup
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.display_surface = pygame.display.get_surface()

        # Player
        self.player = player

        # import 如果未来有什么工具道具需要导入的话，可以在这里导入 
        # example: 
        # overlay_path = './assets/overlay/'
        # self.tools = {tool: pygame.image.load(f'{overlay_path}{tool}.png') for tool in plyer.tools} }

    def display(self):
        #self.display_surface.blit()
        pass