import numpy as np
import random

class CatAI:
    def __init__(self, cat, grid_size=(10, 10), area_bounds=((100, 100), (640, 640)), alpha=0.1, gamma=0.9, epsilon=0.1):
        """
        基于 Q-learning 的 AI，负责猫咪的策略移动，并限制活动范围。
        :param cat: Cat 实例
        :param grid_size: 网格化环境尺寸 (x, y)
        :param area_bounds: 限制范围 ((左上角x, 左上角y), (右下角x, 右下角y))
        :param alpha: 学习率
        :param gamma: 折扣因子
        :param epsilon: 探索率
        """
        self.cat = cat
        self.grid_size = grid_size
        self.area_bounds = area_bounds  # 活动范围
        self.alpha = alpha  # 学习率
        self.gamma = gamma  # 折扣因子
        self.epsilon = epsilon  # 探索率
        self.actions = ["up", "down", "left", "right"]  # 四个可能的移动方向
        self.q_table = np.zeros((*grid_size, len(self.actions)))  # Q 值表
        self.previous_state = None
        self.previous_action = None

    def get_state(self):
        """获取当前猫咪所在的离散网格位置"""
        x, y = self.cat.rect.center
        left, top = self.area_bounds[0]
        right, bottom = self.area_bounds[1]

        # 将猫咪的位置映射到限定区域内的网格
        grid_x = min(self.grid_size[0] - 1, max(0, int((x - left) / ((right - left) / self.grid_size[0]))))
        grid_y = min(self.grid_size[1] - 1, max(0, int((y - top) / ((bottom - top) / self.grid_size[1]))))
        return grid_x, grid_y

    def choose_action(self):
        """ε-greedy 策略选择下一步移动方向"""
        state = self.get_state()
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(self.actions)  # 以 ε 概率随机探索
        else:
            return self.actions[np.argmax(self.q_table[state])]  # 选择当前最佳 Q 值的动作

    def update_q_table(self, reward):
        """更新 Q-learning 表"""
        if self.previous_state is not None:
            prev_x, prev_y = self.previous_state
            prev_action_idx = self.actions.index(self.previous_action)
            current_x, current_y = self.get_state()

            # Bellman 方程更新 Q 值
            best_next_q = np.max(self.q_table[current_x, current_y])
            self.q_table[prev_x, prev_y, prev_action_idx] += self.alpha * (
                reward + self.gamma * best_next_q - self.q_table[prev_x, prev_y, prev_action_idx]
            )

    def move_cat(self):
        """执行移动"""
        action = self.choose_action()
        move_dist = 64  # 一次移动一个网格

        # 限制移动目标在范围内
        target_x, target_y = self.cat.rect.center
        if action == "up":
            target_x, target_y = target_x, target_y - move_dist
        elif action == "down":
            target_x, target_y = target_x, target_y + move_dist
        elif action == "left":
            target_x, target_y = target_x - move_dist, target_y
        elif action == "right":
            target_x, target_y = target_x + move_dist, target_y

        # 确保目标在活动范围内
        left, top = self.area_bounds[0]
        right, bottom = self.area_bounds[1]
        target_x = max(left, min(target_x, right))
        target_y = max(top, min(target_y, bottom))

        self.cat.add_action("move", (target_x, target_y))  # 添加移动任务

        # 记录上一次状态与行动
        self.previous_state = self.get_state()
        self.previous_action = action

    def reward(self, amount):
        """给予 AI 奖励（正奖励鼓励某行为，负奖励惩罚某行为）"""
        self.update_q_table(amount)
