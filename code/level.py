import pygame,sys
from code.settings import *
from code.overlay import Overlay

from code.Sprites import Generic
from code.BackgroundMusicPlayer import BackgroundMusicPlayer

# Cat
from code.Cat_factory import CatFactory

# Save
from sql.init import init_database, save_game, load_game, list_saves


class Level:
    def __init__(self, save_id = -1):

        # 初始化 database
        init_database()

        # 存档 ID
        self.save_id = save_id

        # 初始化游戏状态变量
        self.days_played = 1
        self.current_time = "12:00"  # 示例时间
        self.current_weather = "晴天"
        self.player_money = 1000
        self.inventory = {101: 5, 102: 2}  # 示例背包内容
        self.store = {201: (10, 500), 202: (5, 300)}  # 示例商店商品
        self.cats = [
            {
                'name': 'qiuqiu', 
                'age': 2, 
                'energy': 80, 
                'hunger': 20
            }
        ]

        # Get the display surface
        self.display_surface = pygame.display.get_surface()

        # Sprite groups 用于绘画各种东西
        self.all_sprites = CameraGroup()

        # 背景音乐加载
        self.music_player = BackgroundMusicPlayer()
        
        self.setup()
        
        # 叠加层加载！要求screen和player, 用于加载各种菜单，道具等 ！目前暂时不添加player
        self.overlay = Overlay(self.display_surface)


    def setup(self):
        if self.save_id == -1:
            print("创建新的存档...")
            self.save_progress()  # 自动保存新存档
        else:
            print(f"加载存档 {self.save_id}...")
        game_state = load_game(self.save_id)
        if game_state:
            self.days_played = game_state['days_played']
            self.current_time = game_state['current_time']
            self.current_weather = game_state['current_weather']
            self.player_money = game_state['player_money']
            self.inventory = game_state['inventory']
            self.store = game_state['store']
            self.cats = game_state['cats']
        else:
            print(f"存档 {self.save_id} 不存在，创建新存档...")
            self.save_progress()
        
        
        # 启动背景音乐播放器
        self.music_player.start()

        # 猫咪工厂加载！
        self.cat_factory = CatFactory()
        
        # 创建不同的猫咪对象
        for cat in self.cats:
            self.cat_factory.create_cat(cat['name'], (200, 100), self.all_sprites)

        #self.qiuqiu = self.cat_factory.create_cat("qiuqiu", (200, 100), self.all_sprites)
        #self.momo = self.cat_factory.create_cat("momo", (300, 200), self.all_sprites)
        #self.mila = self.cat_factory.create_cat("qiuqiu", (400, 200), self.all_sprites)

        Generic(
            pos = (0,0),
            surf = pygame.image.load("assets/backgrounds/ground.png").convert_alpha(),
            groups=self.all_sprites,
            z=LAYERS['background']
        )

        self.addAction()
    
    def save_progress(self):
        self.save_id = save_game(
            self.days_played,
            self.current_time,
            self.current_weather,
            self.player_money,
            self.inventory,
            self.store,
            self.cats
        )
        print(f"存档 {self.save_id} 已保存！")


    def run(self,dt):
        self.display_surface.fill('black')

        self.all_sprites.customize_draw()
        self.all_sprites.update(dt)

        #这里放置各种菜单，道具显示
        self.overlay.display(pygame.event.get())

        # 事件处理，监听鼠标点击
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     mouse_pos = event.pos  # 获取鼠标点击的位置
            #     self.player.move_to(mouse_pos)  # 玩家移动到鼠标位置

    
 
        

    def addAction(self):
        # 添加行为链
        self.qiuqiu.add_action("rest", 1)  # 休息 2 秒
        self.qiuqiu.add_action("move", (1300,50))  # 向右移动 500 像素
        self.qiuqiu.add_action("rest", 5)  # 休息 2 秒
        self.qiuqiu.add_action("move", (500,100))  # 向下移动 200 像素

        # self.mila.add_action("rest", 2)  # 向右移动 500 像素
        # self.mila.add_action("rest", 1)  # 休息 2 秒
        # self.mila.add_action("move", (200,100))  # 向下移动 200 像素
        # self.mila.add_action("sleep", 5)  # 休息 2 秒
        # self.mila.add_action("move", (1500,275))  # 向下移动 200 像素

        # self.momo.add_action("rest", 1)  # 向右移动 500 像素
        # self.momo.add_action("move", (1000,100))  # 向下移动 200 像素
        # self.momo.add_action("rest", 2)  # 休息 2 秒
        # self.momo.add_action("move", (1400,295))  # 向下移动 200 像素


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

    def customize_draw(self, target = None):
        
        if target is not None:
            # 获取游戏窗口的大小
            screen_width, screen_height = self.display_surface.get_size()
            
            # 计算偏移量
            self.offset = target.rect.centerx - screen_width / 2, target.rect.centery - screen_height / 2
        else:
            self.offset = (0,0)


        for layer in LAYERS.values():
            for sprite in self.sprites():
                if sprite.z == layer:
                    offset_rect = sprite.rect.move(-self.offset[0], -self.offset[1])
                    self.display_surface.blit(sprite.image, offset_rect)

