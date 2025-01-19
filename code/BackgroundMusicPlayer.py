import pygame
import os
import random
from queue import Queue

class BackgroundMusicPlayer:
    def __init__(self, music_folder="audio/sounds/background", initial_volume=3):
        """
        初始化背景音乐播放器。
        :param music_folder: 存放背景音乐的文件夹路径
        :param initial_volume: 初始音量，范围从0到10
        """
        self.music_folder = music_folder
        self.music_queue = Queue()
        self.volume = initial_volume  # 初始音量
        self.load_music()
        pygame.mixer.init()
        self.set_volume(self.volume)

    def load_music(self):
        """
        加载音乐文件并创建随机播放队列。
        """
        if not os.path.exists(self.music_folder):
            print(f"错误: 文件夹 {self.music_folder} 不存在！")
            return

        # 获取文件夹中所有音乐文件
        music_files = [f for f in os.listdir(self.music_folder) if f.endswith(('.mp3', '.ogg', '.wav'))]
        if not music_files:
            print(f"错误: 文件夹 {self.music_folder} 中没有音乐文件！")
            return

        # 打乱音乐文件并添加到队列
        random.shuffle(music_files)
        for music_file in music_files:
            self.music_queue.put(os.path.join(self.music_folder, music_file))

    def play_next(self):
        """
        播放队列中的下一首音乐。
        如果队列为空，重新加载并随机排序。
        """
        if self.music_queue.empty():
            self.load_music()

        if not self.music_queue.empty():
            next_song = self.music_queue.get()
            pygame.mixer.music.load(next_song)
            pygame.mixer.music.play()
            print(f"正在播放: {next_song}")

    def start(self):
        """
        开始播放背景音乐。
        """
        pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)  # 自定义事件监听音乐结束
        self.play_next()

    def handle_event(self, event):
        """
        处理音乐结束事件。
        :param event: Pygame 事件
        """
        if event.type == pygame.USEREVENT + 1:  # 音乐播放结束
            self.play_next()

    def pause(self):
        """
        暂停当前播放的音乐。
        """
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            print("音乐已暂停。")

    def unpause(self):
        """
        恢复播放暂停的音乐。
        """
        pygame.mixer.music.unpause()
        print("音乐已继续播放。")

    def set_volume(self, volume):
        """
        设置音乐音量。
        :param volume: 音量值，范围从0到10
        """
        if 0 <= volume <= 10:
            self.volume = volume
            pygame.mixer.music.set_volume(self.volume / 10)
            print(f"音量已设置为: {self.volume}/10")
        else:
            print("错误: 音量值必须在0到10之间。")
