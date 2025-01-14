import pygame


class Button:
    def __init__(self, rect, text, font, idle_color, hover_color, click_color, action=None):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.idle_color = idle_color
        self.hover_color = hover_color
        self.click_color = click_color
        self.action = action
        self.state = "idle"  # 可选值：'idle', 'hover', 'click'

    def draw(self, screen):
        # 根据当前状态选择颜色
        if self.state == "hover":
            color = self.hover_color
        elif self.state == "click":
            color = self.click_color
        else:
            color = self.idle_color

        # 绘制按钮背景
        pygame.draw.rect(screen, color, self.rect)

        # 绘制按钮文字
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def update(self, mouse_pos, mouse_down):
        # 判断鼠标是否悬停在按钮上
        if self.rect.collidepoint(mouse_pos):
            self.state = "click" if mouse_down else "hover"
        else:
            self.state = "idle"

    def is_clicked(self):
        return self.state == "click" and self.action is not None
