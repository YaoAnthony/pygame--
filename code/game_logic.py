

class GameLogic:
    def __init__(self, settings):
        self.settings = settings
        self.inventory = {"咖啡": 10, "猫爬架": 5}
        self.customers = []

    def restock(self, item, amount):
        if item in self.inventory:
            self.inventory[item] += amount

    def add_customer(self, name, preference):
        customer = {"name": name, "preference": preference, "favorability": 0}
        self.customers.append(customer)

    def interact_with_customer(self, customer, action):
        if action == "夸奖":
            customer["favorability"] += 1
        elif action == "忽视":
            customer["favorability"] -= 1
