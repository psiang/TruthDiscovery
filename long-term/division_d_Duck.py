import csv
import random
import os
import shutil
import pandas as pd

if __name__ == '__main__':
    truths = pd.read_csv("./data/d_Duck/truth.csv", header=0)
    answers = pd.read_csv("./data/d_Duck/answer.csv", header=0)

    worker = {885,1725,896,335,175,866,1737,1761,
              1721,1723,1722,97,1740,1005,1750,1724,
              1727,1734,1738,1730,1742,1755,1757,1758,1764,1743}
    lab = {0:'0',1:'1'}

    '''ww = {}
    for i in range(len(answers)):
        e = answers.iloc[i].loc['example']
        w = answers.iloc[i].loc['worker']
        l = answers.iloc[i].loc['label']
        if w not in ww:
            ww.update({w:0})
        else:
            ww.update({w:ww[w] + 1})
    print(len(ww.keys()))
    print(ww)'''


    for time in range(0, 1):
        order = []
        for i in range(5):
            for j in range(20):
                order.append(i)
        random.shuffle(order)
        if not os.path.exists("./data/d_Duck/1/answers/%d" % time):
            os.mkdir("./data/d_Duck/1/answers/%d" % time)
        if not os.path.exists("./data/d_Duck/1/truths/%d" % time):
            os.mkdir("./data/d_Duck/1/truths/%d" % time)
        for i in range(5):
            with open("./data/d_Duck/1/truths/%d/ground_truth_%d.csv" % (time, i), "w",
                      newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["task", "truth"])
            with open("./data/d_Duck/1/answers/%d/answer_%d.csv" % (time, i), "w",
                      newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["worker", "task", "answer"])

        trans = {}
        number = {}
        for i in range(100): #len(truths)
            e = truths.iloc[i].loc['question']
            t = truths.iloc[i].loc['truth']
            doc = order[i]
            trans.update({e:doc})
            number.update({e:i})
            with open("./data/d_Duck/1/truths/%d/ground_truth_%d.csv" % (time,doc), "a",
                      newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([number[e], lab[t]])

        for i in range(len(answers)):
            e = answers.iloc[i].loc['question']
            w = answers.iloc[i].loc['worker']
            l = answers.iloc[i].loc['answer']
            if e in trans.keys() and w in worker:
                doc = trans[e]
                with open("./data/d_Duck/1/answers/%d/answer_%d.csv" % (time,doc), "a",
                          newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([w, number[e], lab[l]])
        print("%d finish!" % time)


