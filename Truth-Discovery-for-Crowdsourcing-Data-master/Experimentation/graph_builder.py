class Graph:
    def __init__(self, users, items):
        self.users = users
        self.items = items
        self.n_items = len(items)
        self.n_users = len(users)

        self.user_index_hm = {}
        for u in self.users:
            self.user_index_hm[u.id] = u

        self.item_index_hm = {}
        for it in self.items:
            self.item_index_hm[it.url] = it

    def pick_user(self, it, uid):
        it.add_user(self.user_index_hm[uid])

    def pick_item(self, user, iturl, label):
        user.add_item(self.item_index_hm[iturl], label)