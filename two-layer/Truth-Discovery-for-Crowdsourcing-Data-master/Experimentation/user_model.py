
class User:
    def __init__(self, uid):
        self.items = []
        self.name = None
        self.id = uid
        self.grade = {}

    def add_item(self, it, lgrade):
        self.items.append(it)
        self.grade[it] = lgrade