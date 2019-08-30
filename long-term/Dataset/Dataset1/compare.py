from matplotlib import pyplot as plt
import pandas as pd
import csv

acc = [0] * 20
acc_pure = [0] * 20
Ntime = 500


for time in range(Ntime):
    data1 = pd.read_csv("./result/result_%s.csv" % time, header=0)
    for i in range(len(data1)):
        acc[i] += abs(data1.iloc[i].loc['MSE_mu'])#MSE_mu	Accuracy
    data2 = pd.read_csv("./result_pure/result_pure_%s.csv" % time, header=0)
    for i in range(len(data2)):
        acc_pure[i] += abs(data2.iloc[i].loc['MSE_mu'])
for i in range(20):
    acc[i] = (acc[i] / Ntime)
    acc_pure[i] = (acc_pure[i] / Ntime)
    '''acc[i] = (acc[i] / Ntime)
    acc_pure[i] = (acc_pure[i] / Ntime)'''


plt.plot([str(i) for i in range(20)], acc, 's-', label='long-term')
plt.plot([str(i) for i in range(20)], acc_pure, 'o-', label='pure')
#plt.ylim(0.0, 1.0)

plt.legend()
plt.show()