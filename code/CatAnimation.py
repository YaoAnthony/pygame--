import os
import pygame

class CatAnimation:
    def __init__(self, cat, image_base_path, size, frame_rate):
        """
        初始化动画管理类

        :param cat: Cat 实例
        :param image_base_path: 动画图片的根目录
        :param size: 动画每帧的缩放尺寸
        :param frame_rate: 动画帧速率
        """
        self.cat = cat  # 保存对 Cat 实例的引用
        self.image_base_path = image_base_path
        self.size = size
        self.animations = {
            "up": [], "up_idle": [],
            "down": [], "down_idle": [],
            "left": [], "left_idle": [],
            "right": [], "right_idle": [],
            "sleep1": [], "sleep2": [],
            "stretch": []
        }
        self.frame_rate = frame_rate
        self.frame_index = 0
        #self.status = "down_idle"  # 默认状态

        # 加载所有动画资源
        self.import_assets()
    
    @property
    def status(self):
        """动态从 Cat 实例中获取状态"""
        return self.cat.status

    def import_assets(self):
        """导入图片资源"""
        for direction in self.animations.keys():
            folder_path = os.path.join(self.image_base_path, direction)
            if os.path.exists(folder_path):
                for file_name in sorted(os.listdir(folder_path)):
                    if file_name.endswith(('.png', '.jpg')):
                        image_path = os.path.join(folder_path, file_name)
                        image = pygame.image.load(image_path).convert_alpha()
                        # 缩放图片
                        image = pygame.transform.scale(image, (self.size["width"], self.size["height"]))
                        self.animations[direction].append(image)
            else:
                print(f"警告：路径 {folder_path} 不存在")

    def set_frame(self, index):
        """
        设置当前帧索引
        :param index: 帧索引
        """
        self.frame_index = index


    def update(self, dt):
        """
        更新动画帧
        :param dt: 帧时间间隔
        """
        self.frame_index += self.frame_rate * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0  # 重置帧索引

    def get_current_frame(self):
        """
        获取当前帧图像
        :return: 当前帧的图像
        """
        if self.animations[self.status]:
            return self.animations[self.status][int(self.frame_index)]
        else:
            print(f"警告：状态 '{self.status}' 没有加载动画帧")
            return None
    