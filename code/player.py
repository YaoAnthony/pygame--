import pygame
from code.settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.Surface((64, 32))
        self.image.fill('white')
        self.rect = self.image.get_rect(center=pos)

        # 初始化目标位置为当前位置
        self.target_pos = pygame.Vector2(pos)
        self.speed = 3000  # 设置每秒移动速度

    def update(self, dt):
        """每帧更新位置，进行平滑移动"""
        current_pos = pygame.Vector2(self.rect.center)
        direction = self.target_pos - current_pos
        distance = direction.length()

        if distance > 1:  # 如果距离大于1像素，继续移动
            direction = direction.normalize()  # 归一化方向向量
            new_pos = current_pos + direction * self.speed * dt
            self.rect.center = new_pos
    
    def move_to(self, pos):
        """设置鼠标点击的新位置"""
        self.target_pos = pygame.Vector2(pos)
