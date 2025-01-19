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

        # 定时器
        self.start_ticks = pygame.time.get_ticks()  # 开始计时的时间戳
        self.timer_font = pygame.font.Font(None, 30)  # 时间字体

        # import 如果未来有什么工具道具需要导入的话，可以在这里导入 
        # example: 
        # overlay_path = './assets/overlay/'
        # self.tools = {tool: pygame.image.load(f'{overlay_path}{tool}.png') for tool in plyer.tools} }

    def get_time_left(self):
        elapsed_time = (pygame.time.get_ticks() - self.start_ticks) // 1000  # 已过秒数
        remaining_minutes = max(0, 45 - elapsed_time // 60)  # 剩余分钟
        remaining_seconds = max(0, 59 - elapsed_time % 60)  # 剩余秒
        return f"{remaining_minutes:02}:{remaining_seconds:02}"  # 返回格式化字符串

    def display(self):
        time_left = self.get_time_left()
        time_surface = self.timer_font.render(f"Time: {time_left}", True, (255, 255, 255))
        self.display_surface.blit(time_surface, (20, 20))  # 左上角显示时间