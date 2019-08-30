import csv
import random
import os
import shutil
import pandas as pd

if __name__ == '__main__':
    truths = pd.read_csv("./data/d_jnproduct/truth.csv", header=0)
    answers = pd.read_csv("./data/d_jnproduct/answer.csv", header=0)

    worker = {'A2DDYH9F36MUYI','AK3GZE8MPQL4Y',
              'AN9SY5H7JVQH9','A2AU1R4ZU1ZJ1A','AGWQDYU798X33','A2E7MYHPTDRDRH',
              'A2K3372YQK1Y1R','A1K8LMHVN80G0X','AMVIV4WZNL9FP','ANKWF7RC5KIMN',
              'A2U2CZW77PNCI3','A25DNV1EXXI1WW','AB5YTMVVLIXSV','A9D14MQC5R919',
              'A2KMKK28DFCWI7','AZH91RXTSG1NZ','A3A00OWPY22PD1','A1XWYB204O7LQY',
              'A3B4ORT34G57U2','A17I83WP2RNN8G','A2U3GIFZQ60NZC','A2L4B4EDG5FKWE',
              'A167L0JU5N1097','A1ZE8RQYXP2EHZ','A3PT15XRN1X8VE','A3AMWXCXK3KHFD',
              'ACGDRU48WVNXO','A14ZS4XY2AXKXA','A11VPPEXEUNR0T','A3QJPLFO33NB8M',
              'A3A3ZWI3L3WKJB','A2T6O6MHE8PDB2','A1QV8F8IWF27G8','AXZVN7OO1KGGS',
              'A32YZRSTSLTMZM','A2OQ5SUV3W7HFY','ACDN1AKKXZJHD','A2W9NTI22HTWGF',
              'A2DOANWK20ADX8','AMBJ1VNH0RQLF','A8973OC7HM3Y6','A35F9JZCBMWW8P',
              'A16CUBQSMYOCD9','A2US865826Q0X9','A1RD3MY2LSYKIB','A356E3RU75EGT1',
              'A17AOG749U4H3K','A2SKWBR49HEXFY','A3SMKL9C485WLQ','A3EGTD5X91JG0H',
              'A348T531HDSG5S','A9P5940SILTN7','ATV4GJHYQ7KJ1','A17IODKSQ97YC5',
              'A26O4OGE3YI0UX','A9FFF0ZDBFB3B','A2YCMDV70RH926','AFSUIO2PSX2KW','A3GXLUKX0QLSJG'}
    lab = {0:'0',1:'1'}
    list = ['10', '15', '20', '25', '30', '35', '40']
    for di in list:
        print("divide " + di)
        day = int(di)
        Ntask = int(2000 / day)
        for time in range(0, 1):
            order = []
            for i in range(day):
                numT = Ntask
                if i == day - 1:
                    numT = 2000 - Ntask * (day - 1)
                for j in range(numT):
                    order.append(i)
            random.shuffle(order)
            if not os.path.exists("./data/d_jnproduct/%s/answers/%d" % (di, time)):
                os.mkdir("./data/d_jnproduct/%s/answers/%d" % (di, time))
            if not os.path.exists("./data/d_jnproduct/%s/truths/%d" % (di, time)):
                os.mkdir("./data/d_jnproduct/%s/truths/%d" % (di, time))
            for i in range(day):
                with open("./data/d_jnproduct/%s/truths/%d/ground_truth_%d.csv" % (di,time, i), "w",
                          newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["task", "truth"])
                with open("./data/d_jnproduct/%s/answers/%d/answer_%d.csv" % (di, time, i), "w",
                          newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["worker", "task", "answer"])

            trans = {}
            number = {}
            for i in range(2000): #len(truths)
                e = truths.iloc[i].loc['question']
                t = truths.iloc[i].loc['truth']
                doc = order[i]
                trans.update({e:doc})
                number.update({e:i})
                with open("./data/d_jnproduct/%s/truths/%d/ground_truth_%d.csv" % (di,time,doc), "a",
                          newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([number[e], lab[t]])

            for i in range(len(answers)):
                e = answers.iloc[i].loc['question']
                w = answers.iloc[i].loc['worker']
                l = answers.iloc[i].loc['answer']
                if e in trans.keys():
                    doc = trans[e]
                    with open("./data/d_jnproduct/%s/answers/%d/answer_%d.csv" % (di,time,doc), "a",
                              newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow([w, number[e], lab[l]])
            print("%d finish!" % time)


