import os
import json
from code.Cat import Cat

class CatFactory:
    def __init__(self, base_path="assets/cats/"):
        self.base_path = base_path

    def create_cat(self, cat_name, pos, group):
        """根据名字创建猫咪对象"""
        cat_dir = os.path.join(self.base_path, cat_name)
        if not os.path.exists(cat_dir):
            raise ValueError(f"未找到名为 {cat_name} 的猫咪资源目录：{cat_dir}")

        # 读取 index.json
        index_path = os.path.join(cat_dir, "index.json")
        if not os.path.exists(index_path):
            raise FileNotFoundError(f"{cat_name} 缺少 index.json 文件")

        with open(index_path, "r", encoding="utf-8") as f:
            cat_info = json.load(f)

        # 加载 images 文件夹路径
        image_base_path = os.path.join(cat_dir, "images")
        return Cat(pos, group, cat_info, image_base_path)
