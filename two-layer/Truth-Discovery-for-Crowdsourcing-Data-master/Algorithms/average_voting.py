def evaluate_items(graph):
    item_value = {}
    for it in graph.items:
        n = 0
        tot = 0.0
        for u in it.users:
            n += 1
            tot += u.grade[it]
        item_value[it] = tot / n
    return item_value