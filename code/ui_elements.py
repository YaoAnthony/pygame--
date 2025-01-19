import pygame


class UIManager:
    def __init__(self, screen):
        self.screen = screen

        # 加载支持中文的字体
        self.font = pygame.font.Font("font/cn-YRDZST.ttf", 36)  # 使用中文字体
        self.title_font = pygame.font.Font("font/cn-YRDZST.ttf", 48)  # 标题字体

    def draw_main_menu(self):
        # 获取屏幕尺寸
        screen_width, screen_height = self.screen.get_size()

        # 绘制主标题
        title_text = self.title_font.render("猫咪咖啡馆", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 4))
        self.screen.blit(title_text, title_rect)

        # 绘制菜单选项
        menu_items = ["开始游戏", "设置", "退出"]
        menu_start_y = screen_height // 2  # 菜单起始位置（屏幕中间）
        spacing = 50  # 每个菜单项之间的间距

        for i, item in enumerate(menu_items):
            # 渲染菜单文字
            text_surface = self.font.render(item, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(screen_width // 2, menu_start_y + i * spacing))
            self.screen.blit(text_surface, text_rect)

    def handle_menu_click(self, mouse_pos):
        """根据鼠标位置处理点击事件"""
        screen_width, screen_height = self.screen.get_size()
        menu_items = ["开始游戏", "设置", "退出"]
        menu_start_y = screen_height // 2
        spacing = 50

        for i, item in enumerate(menu_items):
            # 每个按钮的矩形区域
            rect = pygame.Rect(screen_width // 2 - 100, menu_start_y + i * spacing - 20, 200, 40)
            if rect.collidepoint(mouse_pos):
                return item  # 返回点击的菜单项
        return None
