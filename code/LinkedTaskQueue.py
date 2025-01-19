from collections import OrderedDict

class TaskNode:
    def __init__(self, task_name, value):
        self.task_name = task_name  # 任务名称
        self.value = value  # value

    def __repr__(self):
        return f"{self.task_name} ({self.value})"

class LinkedTaskQueue:
    def __init__(self):
        self.task_map = OrderedDict()  # 任务链表
        self.task_counter = 0  # 任务ID计数器

    def _generate_task_id(self):
        """生成唯一任务ID"""
        self.task_counter += 1
        return f"task{self.task_counter}"

    def add_task(self, task_name, value):
        """向末尾添加新任务"""
        task_id = self._generate_task_id()
        task_node = TaskNode(task_name, value)
        self.task_map[task_id] = task_node
        #print(f"任务 {task_id} 已添加: {task_node}")

    def add_high_priority_task(self, task_name, value):
        """在开头插入高优先级任务"""
        task_id = self._generate_task_id()
        task_node = TaskNode(task_name, value)
        self.task_map = OrderedDict([(task_id, task_node)] + list(self.task_map.items()))
        print(f"高优先级任务 {task_id} 已插入: {task_node}")

    def pop_next_task(self):
        """弹出第一个任务"""
        if self.task_map:
            task_id, task_node = self.task_map.popitem(last=False)
            print(f"弹出任务 {task_id}: {task_node}")
            return task_id, task_node
        print("无任务可执行1")
        return None, None
    
    def get_current_task(self):
        """获取当前任务,不删除任务"""
        if self.task_map:
            task_id, task_node = next(iter(self.task_map.items()))
            return task_id, task_node
        #print("无任务可执行2")
        return None, None
    
    def len(self):
        """获取任务数量"""
        return len(self.task_map)
    
    def move_to_front(self, task_id):
        """将某个任务移动到队列开头"""
        task_node = self.task_map.pop(task_id)
        self.task_map = OrderedDict([(task_id, task_node)] + list(self.task_map.items()))
        print(f"任务 {task_id} 已被移动到队列开头")

    def __repr__(self):
        """方便调试，打印任务列表"""
        return f"任务队列: {list(self.task_map.values())}"