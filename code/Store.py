import pygame

class Store:
    """
    商店类，用于显示商店界面及其逻辑
    """
    def __init__(self, screen):
        self.screen = screen
        self.is_open = False  # 商店是否打开
        # 加载支持中文的字体
        self.font = pygame.font.Font("font/cn-YRDZST.ttf", 36)  # 使用中文字体
        self.title_font = pygame.font.Font("font/cn-YRDZST.ttf", 48)  # 标题字体
        self.items = ["A", "B", "C"]  # 商品列表
        self.background_color = (50, 50, 50)  # 背景颜色
        self.text_color = (255, 255, 255)  # 文字颜色

    def toggle(self):
        """切换商店的打开状态"""
        self.is_open = not self.is_open

    def close(self):
        """关闭商店"""
        self.is_open = False

    def display(self, events):
        """
        显示商店界面
        :param events: Pygame事件列表
        """
        if self.is_open:
            # 绘制商店背景
            self.screen.fill(self.background_color)

            # 绘制商品列表
            y_offset = 100
            for item in self.items:
                item_surface = self.font.render(f"商品: {item}", True, self.text_color)
                self.screen.blit(item_surface, (100, y_offset))
                y_offset += 60

            # 绘制关闭提示
            close_surface = self.font.render("点击任意位置退出商店", True, (200, 200, 200))
            self.screen.blit(close_surface, (100, y_offset + 40))

            # 处理关闭商店的事件
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.close()
