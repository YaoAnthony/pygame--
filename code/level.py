import pygame,sys
from code.settings import *
from code.player import Player

# Cat
from code.Cat_factory import CatFactory

class Level:
    def __init__(self):

        # Get the display surface
        self.display_surface = pygame.display.get_surface()
        # Sprite groups 用于绘画各种东西
        self.all_sprites = pygame.sprite.Group()
        # 猫咪工厂加载！
        self.cat_factory = CatFactory()

        self.setup()

    def setup(self):
        self.player = Player((360,360), self.all_sprites)

        # 创建不同的猫咪对象
        self.qiuqiu = self.cat_factory.create_cat("qiuqiu", (200, 200), self.all_sprites)
        self.mila = self.cat_factory.create_cat("qiuqiu", (200, 200), self.all_sprites)
        # 添加行为链
        self.qiuqiu.add_action("move", (1500,300))  # 向右移动 500 像素
        self.qiuqiu.add_action("rest", 5)  # 休息 2 秒
        self.qiuqiu.add_action("move", (500,100))  # 向下移动 200 像素

        self.mila.add_action("rest", 2)  # 向右移动 500 像素
        self.mila.add_action("rest", 1)  # 休息 2 秒
        self.mila.add_action("move", (200,100))  # 向下移动 200 像素
        self.mila.add_action("rest", 1)  # 休息 2 秒
        self.mila.add_action("move", (1500,275))  # 向下移动 200 像素

    def run(self,dt):
        self.display_surface.fill('black')
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update(dt)

        # 事件处理，监听鼠标点击
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # 获取鼠标点击的位置
                self.player.move_to(mouse_pos)  # 玩家移动到鼠标位置

    def handle_event(self, event):
        #处理事件
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            self.player.move_to(mouse_pos)
