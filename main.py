import pygame,os,json,sys

#Level
from code.level import Level

from code.settings import Settings
from code.game_logic import GameLogic
from code.ui_elements import UIManager
from code.Button import Button


# 加载配置
def load_config():
    with open("config.json", "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(config):
    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)



class Game:
    '''
    parameter:
        clock: game time
        screen: game screen
        running: judge whether game is running
        level: game

    '''
    def __init__(self):
        # 初始化 Pygame
        pygame.init()

        # 加载配置文件
        config = load_config()
        settings = Settings(config)

        # 设置窗口
        info = pygame.display.Info()  # 获取屏幕分辨率
        screen_width = info.current_w  # 当前屏幕的宽度
        screen_height = info.current_h  # 当前屏幕的高度
        # 设置窗口位置在屏幕下方
        window_height = screen_height // 3
        window_y_pos = screen_height - window_height  # y 坐标在屏幕底部
        os.environ['SDL_VIDEO_WINDOW_POS'] = f"0,{window_y_pos}"  # x=0, y=窗口高度
        self.screen = pygame.display.set_mode((screen_width, window_height), pygame.NOFRAME)

        #不设置title
        pygame.display.set_caption("")

        #clock
        self.clock = pygame.time.Clock()

        #Level
        self.level = Level()

        self.running = True
    
    def run(self):
        while self.running:
            # delta time
            dt = self.clock.tick(60) / 1000
            self.level.run(dt)
            pygame.display.update()

        

        

if __name__ == "__main__":
    game = Game()
    game.run()
    #main()
