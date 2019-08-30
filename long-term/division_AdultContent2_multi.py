import csv
import random
import os
import shutil
import pandas as pd

if __name__ == '__main__':
    truths = pd.read_csv("./data/AdultContent2_multi/gold.csv", header=0)
    answers = pd.read_csv("./data/AdultContent2_multi/labels.csv", header=0)

    lab = {'G':'0','P':'1','R':'2','X':'3','B':'4'}

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
        for i in range(20):
            for j in range(20):
                order.append(i)
        random.shuffle(order)
        if not os.path.exists("./data/AdultContent2_multi/1/answers/%d" % time):
            os.mkdir("./data/AdultContent2_multi/1/answers/%d" % time)
        if not os.path.exists("./data/AdultContent2_multi/1/truths/%d" % time):
            os.mkdir("./data/AdultContent2_multi/1/truths/%d" % time)
        for i in range(20):
            with open("./data/AdultContent2_multi/1/truths/%d/ground_truth_%d.csv" % (time, i), "w",
                      newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["task", "truth"])
            with open("./data/AdultContent2_multi/1/answers/%d/answer_%d.csv" % (time, i), "w",
                      newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["worker", "task", "answer"])

        trans = {}
        number = {}
        for i in range(400): #len(truths)
            e = truths.iloc[i].loc['example']
            t = truths.iloc[i].loc['truth']
            doc = order[i]
            trans.update({e:doc})
            number.update({e:i})
            with open("./data/AdultContent2_multi/1/truths/%d/ground_truth_%d.csv" % (time,doc), "a",
                      newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([number[e], lab[t]])

        for i in range(len(answers)):
            e = answers.iloc[i].loc['example']
            w = answers.iloc[i].loc['worker']
            l = answers.iloc[i].loc['label']
            if e in trans.keys():
                doc = trans[e]
                with open("./data/AdultContent2_multi/1/answers/%d/answer_%d.csv" % (time,doc), "a",
                          newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([w, number[e], lab[l]])
        print("%d finish!" % time)

