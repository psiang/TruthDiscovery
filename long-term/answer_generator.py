import csv
import random
import pandas as pd


def read_truth(day):
    data = pd.read_csv("./data/truths/ground_truth_%d.csv" % (day), header=0)
    return data


def worker_value():
    value = []
    wn = 200
    for i in range(wn):
        r = random.gauss(0.6, 0.1 / 3)
        if r < 0.5:
            r = 0.5
        if r > 1:
            r = 1
        value.append(r)
    '''for i in range(wn + 2):
        value.append(random.gauss(0, 1))
    maxv = max(value)
    minv = min(value)
    value.remove(maxv)
    value.remove(minv)
    for i in range(wn):
        value[i] = (value[i] - minv) / (maxv - minv)'''
    return pd.DataFrame({'worker': [x for x in range(wn)], 'value': value})


def make_answer(day, truths, workers):
    w = []
    t = []
    a = []
    for i in range(len(workers)):
        if fliper(0.25):
            for j in range(len(truths)):
                if fliper(0.2):
                    w.append(workers.iloc[i].loc['worker'])
                    t.append(truths.iloc[j].loc['task'])
                    if fliper(workers.iloc[i].loc['value']):
                        a.append(truths.iloc[j].loc['truth'])
                    else:
                        a.append(1 - truths.iloc[j].loc['truth'])
    data = pd.DataFrame({'worker': w, 'task': t, 'answer': a})
    data.to_csv("./data/answers/answer_%d.csv" % day, index=False)


def fliper(p):
    if random.uniform(0, 1) <= p:
        return True
    else:
        return False

if __name__ == '__main__':
    workers = worker_value()
    workers.to_csv("./data/workers.csv", index=False)
    for day in range(20):
        truths = read_truth(day)
        make_answer(day, truths, workers)
        print("Day %d Finish!" % day)