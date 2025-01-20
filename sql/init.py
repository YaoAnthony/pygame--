import sqlite3
import os

DB_PATH = os.path.join("sql", "game_save.db")

# 初始化数据库
def init_database():
    conn = sqlite3.connect("game_save.db")
    cursor = conn.cursor()
    # 创建表
    cursor.executescript('''
    CREATE TABLE IF NOT EXISTS saves (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        days_played INTEGER NOT NULL,
        current_time TEXT NOT NULL,
        current_weather TEXT NOT NULL,
        player_money INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        save_id INTEGER NOT NULL,
        item_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        FOREIGN KEY (save_id) REFERENCES saves(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS store (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        save_id INTEGER NOT NULL,
        item_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        price INTEGER NOT NULL,
        FOREIGN KEY (save_id) REFERENCES saves(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS cats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        save_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        energy INTEGER NOT NULL,
        hunger INTEGER NOT NULL,
        FOREIGN KEY (save_id) REFERENCES saves(id) ON DELETE CASCADE
    );

    CREATE TRIGGER IF NOT EXISTS limit_saves
    AFTER INSERT ON saves
    WHEN (SELECT COUNT(*) FROM saves) > 3
    BEGIN
        DELETE FROM saves WHERE id = (SELECT MIN(id) FROM saves);
    END;
    ''')
    conn.commit()
    conn.close()

def save_game(days_played, current_time, current_weather, player_money, inventory, store, cats):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 插入存档信息
        cursor.execute('''
            INSERT INTO saves (days_played, current_time, current_weather, player_money)
            VALUES (?, ?, ?, ?)
            ''', (days_played, current_time, current_weather, player_money))
        save_id = cursor.lastrowid  # 获取刚插入的存档 ID

        # 插入背包信息
        for item_id, quantity in inventory.items():
            cursor.execute('''
            INSERT INTO inventory (save_id, item_id, quantity) VALUES (?, ?, ?)
            ''', (save_id, item_id, quantity))

        # 插入商店信息
        for item_id, (quantity, price) in store.items():
            cursor.execute('''
            INSERT INTO store (save_id, item_id, quantity, price) VALUES (?, ?, ?, ?)
            ''', (save_id, quantity, price))

        # 插入猫咪信息
        for cat in cats:
            cursor.execute('''
            INSERT INTO cats (save_id, name, age, energy, hunger) VALUES (?, ?, ?, ?, ?)
            ''', (save_id, cat['name'], cat['age'], cat['energy'], cat['hunger']))

        conn.commit()
        conn.close()
        print("存档成功！")
    except sqlite3.Error as e:
        print(f"存档失败: {e}")
    finally:
        conn.close()

def delete_save(save_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM saves WHERE id = ?', (save_id,))
        conn.commit()
        print(f"存档 {save_id} 已删除！")
    except sqlite3.Error as e:
        print(f"删除存档失败: {e}")
    finally:
        conn.close()


def load_game(save_id):
    conn = sqlite3.connect("game_save.db")
    cursor = conn.cursor()

    # 查询存档基本信息
    cursor.execute('SELECT * FROM saves WHERE id = ?', (save_id,))
    save = cursor.fetchone()

    if not save:
        print("存档不存在！")
        return None

    # 查询背包信息
    cursor.execute('SELECT item_id, quantity FROM inventory WHERE save_id = ?', (save_id,))
    inventory = {row[0]: row[1] for row in cursor.fetchall()}

    # 查询商店信息
    cursor.execute('SELECT item_id, quantity, price FROM store WHERE save_id = ?', (save_id,))
    store = {row[0]: (row[1], row[2]) for row in cursor.fetchall()}

    # 查询猫咪信息
    cursor.execute('SELECT name, age, energy, hunger FROM cats WHERE save_id = ?', (save_id,))
    cats = [{'name': row[0], 'age': row[1], 'energy': row[2], 'hunger': row[3]} for row in cursor.fetchall()]

    conn.close()

    # 返回游戏状态
    return {
        'days_played': save[1],
        'current_time': save[2],
        'current_weather': save[3],
        'player_money': save[4],
        'inventory': inventory,
        'store': store,
        'cats': cats
    }

def list_saves():
    conn = sqlite3.connect("game_save.db")
    cursor = conn.cursor()
    cursor.execute('SELECT id, days_played, current_time, current_weather FROM saves')
    saves = cursor.fetchall()
    conn.close()
    return saves

