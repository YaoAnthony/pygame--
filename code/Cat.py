import pygame
import random
import os
from code.LinkedTaskQueue import LinkedTaskQueue
from code.settings import *
from code.CatAnimation import CatAnimation

#ai
from code.CatAI import CatAI

class Cat(pygame.sprite.Sprite):
    '''
        生成一只猫咪，包括猫咪的基本信息、动画、行为等
        目前存在变量
            name: 猫咪名字
            breed: 猫咪品种
            description: 猫咪描述
            age: 猫咪年龄
            size: 图片尺寸

    '''
    def __init__(self, pos, group, cat_info, image_base_path):
        super().__init__(group)

        # general setup
        self.name = cat_info["name"]
        self.breed = cat_info["breed"]
        self.description = cat_info["description"]
        self.age = cat_info["age"]

        self.hunger = cat_info.get("hunger", 100)
        self.energy = cat_info.get("energy", 100)
        self.hunger_rate = cat_info.get("hunger_rate", 1)


        self.size = cat_info.get("size", {"width": 64, "height": 64})  # 默认 64x64 尺寸
        self.frame_rate = cat_info.get("frame_rate", 2)  # 每帧间隔时间
        self._status = "down_idle"

        self._animation = CatAnimation(self, image_base_path, self.size, self.frame_rate)

        self.z = LAYERS["main"]
        # Default Settings

        # 设置初始图片
        self.image = self._animation.get_current_frame()
        self.rect = self.image.get_rect(center=pos)

        # 碰撞检测矩形
        self.hitbox = self.rect.copy().inflate((-20, -20))  

        # Behavior 
        self.actions = LinkedTaskQueue()

        # 动作状态
        self.is_resting = False


        self.is_sleeping = False
        self.sleep_timer = 0
        self.sleep_duration = 0

        self.rest_duration = 0  # 总休息时间
        self.rest_timer = 0  # 已休息时间
        self.dierction = pygame.math.Vector2()
        self.speed = 300  # 新增速度属性

        self.ai = CatAI(self, grid_size=(10, 10), area_bounds=((64, 64), (1000, 480)))


    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, new_status):
        if self._status != new_status:  # 仅在状态改变时重置帧索引
            self._status = new_status
            self._animation.set_frame(0)  # 重置帧索引


    #
    # 行为控制区
    #


    def process_current_action(self, dt):
        '''
            通过get_current_task获取队列中的任务,尝试分解并完成任务,
            目前已知任务有:
                move: 移动到指定位置
        '''
        _, action = self.actions.get_current_task()
        if action is None:
            return


        if action.task_name == "move":
            self.move_to_target(action.value, dt)
        elif action.task_name == "rest":
            self.rest(action.value)
            self.update_rest_status(dt)
        elif action.task_name == "sleep":
            # 随机播放其中一种睡觉动画 N秒
            self.sleep(action.value)
            self.update_sleeping(dt)

        else:
            print(f"未知任务 {action}")
            self.actions.pop_next_task()


    def add_action(self, action_type, duration_or_distance):
        """添加新动作"""
        self.actions.add_task(action_type, duration_or_distance)


    def move_to_target(self, target_point, dt):
        """
        恒速移动到目标位置（曼哈顿距离），dt 为帧间隔时间。
        """
        current_pos = pygame.math.Vector2(self.rect.center)
        target_pos = pygame.math.Vector2(target_point)

        # 计算水平方向和竖直方向的距离差
        delta_x = target_pos.x - current_pos.x
        delta_y = target_pos.y - current_pos.y

        # 判断水平或垂直方向移动的优先级
        if abs(delta_x) > 0:
            direction_x = 1 if delta_x > 0 else -1  # 向右为正，向左为负
            self.dierction = pygame.math.Vector2(direction_x, 0)  # 水平移动
            self.status = "right" if direction_x > 0 else "left"
            move_distance = self.speed * dt  # 根据帧间隔调整移动距离

            # 如果距离小于一步的距离，则直接到目标位置
            if abs(delta_x) < move_distance:
                move_distance = abs(delta_x)
            self.rect.centerx += direction_x * move_distance
            #self.hitbox.centerx = round(self.pos.x)

        elif abs(delta_y) > 0:
            direction_y = 1 if delta_y > 0 else -1  # 向下为正，向上为负
            self.dierction = pygame.math.Vector2(0, direction_y)  # 垂直移动
            self.status = "down" if direction_y > 0 else "up"
            move_distance = self.speed * dt

            if abs(delta_y) < move_distance:
                move_distance = abs(delta_y)
            self.rect.centery += direction_y * move_distance
            #self.hitbox.centery = round(self.pos.y)

        # 检查是否到达目标点
        if self.rect.center == target_point:
            #print(f"已到达目标位置 {target_point}")
            self.dierction = pygame.math.Vector2()  # 停止移动
            self.status = "down_idle"  # 回到待机状态
            self.actions.pop_next_task()  # 完成任务

    def sleep(self, duration):
        """Randomly select a sleeping animation and sleep for a given duration."""
        if not self.is_sleeping:
            self.is_sleeping = True
            self.status = random.choice(["sleep1", "sleep2"])
            self.sleep_timer = 0
            self.sleep_duration = duration


    def update_sleeping(self, dt):
        """Update sleep timer and play sleeping animation."""
        if self.is_sleeping:
            self.sleep_timer += dt

            if self.sleep_timer >= self.sleep_duration:
                self.is_sleeping = False
                self.status = "down_idle"
                self.actions.pop_next_task()    

    
    def rest(self, duration):
        """休息指定时间"""
        if not self.is_resting:
            self.is_resting = True
            self.rest_duration = duration  # 总休息时间
            self.rest_timer = 0  # 已休息时间
            self.status = "down_idle"  # 休息时保持待机动画

    def update_rest_status(self, dt):
        """更新休息状态"""
        if self.is_resting:
            self.rest_timer += dt  # 累计时间
            if self.rest_timer >= self.rest_duration:
                #print(f"休息了 {self.rest_duration} 秒，任务完成")
                self.is_resting = False  # 结束休息
                self.rest_timer = 0
                self.actions.pop_next_task()  # 完成休息任务    
    
    def random_walk(self):
        """随机移动"""
        pass

    def meow(self):
        """喵喵叫"""
        pass


    # 
    # 更新区
    #
    def update(self, dt):
        """更新动画和位置"""
        self.process_current_action(dt)
        self.ai.move_cat()  # 让 AI 决定下一步行动


        # 更新动画
        self._animation.update(dt)
        self.image = self._animation.get_current_frame()
