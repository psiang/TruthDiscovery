import csv
import random
import os
import shutil
import pandas as pd

now_work = "participant"

def read_truth(day, time, rate):
    data = pd.read_csv("./data/" + now_work + "/%s/truths/%d/ground_truth_%d.csv" % (rate, time, day), header=0)
    return data


def worker_value():
    value = []
    wn = 150
    for i in range(wn):
        r = random.gauss(0.6, 0.2 / 2)
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


def make_answer(day, truths, workers, time, rate):
    w = []
    t = []
    a = []
    for i in range(len(workers)):
        if fliper(0.3333333333333333):
            for j in range(len(truths)):
                if fliper(float(rate)):
                    w.append(workers.iloc[i].loc['worker'])
                    t.append(truths.iloc[j].loc['task'])
                    if fliper(workers.iloc[i].loc['value']):
                        a.append(truths.iloc[j].loc['truth'])
                    else:
                        a.append(1 - truths.iloc[j].loc['truth'])
    data = pd.DataFrame({'worker': w, 'task': t, 'answer': a})
    data.to_csv("./data/" + now_work + "/%s/answers/%d/answer_%d.csv" % (rate, time, day), index=False)


def fliper(p):
    if random.uniform(0, 1) <= p:
        return True
    else:
        return False

if __name__ == '__main__':
    rates = ['0.7', '0.8', '0.9', '1.0']
    for rate in rates:
        print(str(float(rate)) + " is starting!")
        if not os.path.exists("./data/" + now_work + "/%s/answers" % rate):
            os.mkdir("./data/" + now_work + "/%s/answers" % rate)
        if not os.path.exists("./data/" + now_work + "/%s/workers" % rate):
            os.mkdir("./data/" + now_work + "/%s/workers" % rate)
        for time in range(0, 100):
            if not os.path.exists("./data/" + now_work + "/%s/answers/%d" % (rate, time)):
                os.mkdir("./data/" + now_work + "/%s/answers/%d" % (rate, time))
            if not os.path.exists("./data/" + now_work + "/%s/workers/%d" % (rate, time)):
                os.mkdir("./data/" + now_work + "/%s/workers/%d" % (rate, time))
            workers = worker_value()
            workers.to_csv("./data/" + now_work + "/%s/workers/%d/workers.csv" % (rate, time), index=False)
            #shutil.copy("./data/answers/0/answer_0.csv", "./data/answers/%d" % time)
            for day in range(0, 20):
                truths = read_truth(day, time, rate)
                make_answer(day, truths, workers, time, rate)
                print("\tDay %d Finish!" % day)
            print("Time %d Finish!" % time)
        print(rate + " is finished!")