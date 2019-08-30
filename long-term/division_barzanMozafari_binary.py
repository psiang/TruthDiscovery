import csv
import random
import os
import shutil
import pandas as pd

if __name__ == '__main__':
    truths = pd.read_csv("./data/barzanMozafari_binary/evaluation.csv", header=0)
    answers = pd.read_csv("./data/barzanMozafari_binary/labels.csv", header=0)

    worker = {'A2H3M1JVY991Q3','AADB14P6ZCSOC','A39LJRF4LGAIX5',
              'A2AM9D21A7KEZF','A17RJ1RVSJ6Z9Y','A36N8WJKIGNKT0',
              'A2IGRNX80F2BRD','A3KUOOJQ1Y4QC0','A39PPFQ1L7N6OQ',
              'A8JXHGJIXG2NQ','A3QJWBEC5A5OEG','A29PMRCRJ7Q9ZD',
              'A39BQD05T7ALEG','A17G2QHR8AH5VV','AROJE6P94TZ9Q',
              'AB5C1BRQTC19Q','A52AHJEUWFSA2','A3U5GS55UEF5C8',
              'A37NNI7YFHQU0E','A2D2UXKO4AWBO8','A1N914XTP4CJ7X',
              'A1E3MS4AD1WM8V','AQ3M9XJK8WOII','AE4OWTLXURMKP',
              'A1BENJCLTWP1NH','A23RB1Y4ANXQLS','A2U3EWDHMY526T'}
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
        for i in range(10):
            for j in range(100):
                order.append(i)
        random.shuffle(order)
        if not os.path.exists("./data/barzanMozafari_binary/1/answers/%d" % time):
            os.mkdir("./data/barzanMozafari_binary/1/answers/%d" % time)
        if not os.path.exists("./data/barzanMozafari_binary/1/truths/%d" % time):
            os.mkdir("./data/barzanMozafari_binary/1/truths/%d" % time)
        for i in range(10):
            with open("./data/barzanMozafari_binary/1/truths/%d/ground_truth_%d.csv" % (time, i), "w",
                      newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["task", "truth"])
            with open("./data/barzanMozafari_binary/1/answers/%d/answer_%d.csv" % (time, i), "w",
                      newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["worker", "task", "answer"])

        trans = {}
        number = {}
        for i in range(1000): #len(truths)
            e = truths.iloc[i].loc['example']
            t = truths.iloc[i].loc['truth']
            doc = order[i]
            trans.update({e:doc})
            number.update({e:i})
            with open("./data/barzanMozafari_binary/1/truths/%d/ground_truth_%d.csv" % (time,doc), "a",
                      newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([number[e], lab[t]])

        for i in range(len(answers)):
            e = answers.iloc[i].loc['example']
            w = answers.iloc[i].loc['worker']
            l = answers.iloc[i].loc['label']
            if e in trans.keys() and w in worker:
                doc = trans[e]
                with open("./data/barzanMozafari_binary/1/answers/%d/answer_%d.csv" % (time,doc), "a",
                          newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([w, number[e], lab[l]])
        print("%d finish!" % time)


