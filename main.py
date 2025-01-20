import pygame,os,json,sys

#Level
from code.level import Level
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

        self.ui_manager = UIManager(self.screen)  # 实例化 UIManager

        self.running = True
    
    def show_start_screen(self):
        """显示主菜单，处理用户点击"""
        while True:
            self.screen.fill((255, 228, 196))
            self.ui_manager.draw_main_menu()  # 绘制主菜单

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    mouse_pos = pygame.mouse.get_pos()
                    menu_option = self.ui_manager.handle_menu_click(mouse_pos)
                    if menu_option == "开始游戏":
                        return  # 退出主菜单，进入游戏循环
                    elif menu_option == "设置":
                        print("设置功能尚未实现")  # 可跳转到设置界面
                    elif menu_option == "退出":
                        pygame.quit()
                        sys.exit()

            pygame.display.flip()
            self.clock.tick(60)
    
    def run(self):
        self.show_start_screen()  # 显示主菜单

        #Level
        self.level = Level()
        
        while self.running:
            # delta time
            dt = self.clock.tick(60) / 1000
            self.level.run(dt)
            pygame.display.update()

        

        

if __name__ == "__main__":
    game = Game()
    game.run()