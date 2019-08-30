import csv
import random
import os
import shutil
import pandas as pd

if __name__ == '__main__':
    truths = pd.read_csv("./data/s4_Dogdata/truth.csv", header=0)
    answers = pd.read_csv("./data/s4_Dogdata/answer.csv", header=0)

    lab = {0:'0',1:'1',2:'2',3:'3'}


    for time in range(0, 1):
        order = []
        for i in range(20):
            for j in range(40):
                order.append(i)
        random.shuffle(order)
        if not os.path.exists("./data/s4_Dogdata/1/answers/%d" % time):
            os.mkdir("./data/s4_Dogdata/1/answers/%d" % time)
        if not os.path.exists("./data/s4_Dogdata/1/truths/%d" % time):
            os.mkdir("./data/s4_Dogdata/1/truths/%d" % time)
        for i in range(20):
            with open("./data/s4_Dogdata/1/truths/%d/ground_truth_%d.csv" % (time, i), "w",
                      newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["task", "truth"])
            with open("./data/s4_Dogdata/1/answers/%d/answer_%d.csv" % (time, i), "w",
                      newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["worker", "task", "answer"])

        trans = {}
        number = {}
        for i in range(800): #len(truths)
            e = truths.iloc[i].loc['question']
            t = truths.iloc[i].loc['truth']
            doc = order[i]
            trans.update({e:doc})
            number.update({e:i})
            with open("./data/s4_Dogdata/1/truths/%d/ground_truth_%d.csv" % (time,doc), "a",
                      newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([number[e], lab[t]])

        for i in range(len(answers)):
            e = answers.iloc[i].loc['question']
            w = answers.iloc[i].loc['worker']
            l = answers.iloc[i].loc['answer']
            if e in trans.keys():
                doc = trans[e]
                with open("./data/s4_Dogdata/1/answers/%d/answer_%d.csv" % (time,doc), "a",
                          newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([w, number[e], lab[l]])
        print("%d finish!" % time)


