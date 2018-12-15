import numpy as np

class Item:
    def __init__(self, quality, url):
        self.users = []
        self.id = None
        self.q = quality
        self.url = url

    def add_user(self, user):
        self.users.append(user)