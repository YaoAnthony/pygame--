import pygame
from code.settings import * 
from code.Store import Store

class Overlay:
    '''
    叠加层类，用于显示各种菜单，道具等
    '''
    def __init__(self, screen):
        # General setup
        self.screen = screen
        self.display_surface = pygame.display.get_surface()

        # 加载支持中文的字体
        self.font = pygame.font.Font("font/cn-YRDZST.ttf", 36)  # 使用中文字体
        self.title_font = pygame.font.Font("font/cn-YRDZST.ttf", 48)  # 标题字体
        
        # 商店
        self.store = Store(screen)

        # 商店按钮的矩形区域
        self.shop_button_rect = pygame.Rect(self.display_surface.get_width() - 120, 20, 100, 40)


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

    def draw_time(self):
        '''显示计时器'''
        time_left = self.get_time_left()
        time_surface = self.timer_font.render(f"Time: {time_left}", True, (255, 255, 255))
        self.display_surface.blit(time_surface, (20, 20))  # 左上角显示时间
    
    def draw_shop_button(self):
        '''绘制商店按钮'''
        pygame.draw.rect(self.display_surface, (0, 128, 255), self.shop_button_rect)  # 按钮背景
        small_font = pygame.font.Font("font/cn-YRDZST.ttf", 24)  # 使用更小字号的字体
        shop_text = small_font.render("商店", True, (255, 255, 255))  # 中文文本
        text_rect = shop_text.get_rect(center=self.shop_button_rect.center)  # 居中对齐
        self.display_surface.blit(shop_text, text_rect)  # 绘制文本


    def display(self,events):
        '''显示叠加层'''

        if self.store.is_open:
            self.store.display(events)
        else:
            self.draw_time()
            self.draw_shop_button()

            # 处理商店按钮点击事件
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.shop_button_rect.collidepoint(event.pos):
                        self.store.toggle()  # 切换商店开关

            # 如果未来有什么工具道具需要显示的话，可以在这里显示
            # example: 
            # self.display_surface.blit(self.tools['tool_name'], (x, y)) 

            # 如果未来有什么其他道具需要显示的话，可以在这里显示
            # example: 
            # self.display_surface.blit(self.tools['tool_name'], (x, y))


    
