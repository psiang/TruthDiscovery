import csv
import random
import os
import shutil
import pandas as pd


def read_truth(day, time):
    data = pd.read_csv("./data/truths/%d/ground_truth_%d.csv" % (time, day), header=0)
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


def make_answer(day, truths, workers, time):
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
    data.to_csv("./data/answers/%d/answer_%d.csv" % (time, day), index=False)


def fliper(p):
    if random.uniform(0, 1) <= p:
        return True
    else:
        return False

if __name__ == '__main__':
    workers = worker_value()
    workers.to_csv("./data/workers.csv", index=False)
    for time in range(1, 100):
        if not os.path.exists("./data/answers/%d" % time):
            os.mkdir("./data/answers/%d" % time)
        shutil.copy("./data/answers/0/answer_0.csv", "./data/answers/%d" % time)
        for day in range(1, 20):
            truths = read_truth(day, time)
            make_answer(day, truths, workers, time)
            print("\tDay %d Finish!" % day)
        print("Time %d Finish!" % time)