from matplotlib import pyplot as plt
import pandas as pd
import csv

data1 = pd.read_csv("./result.csv", header=0)
data2 = pd.read_csv("./result_pure.csv", header=0)


plt.plot([str(i) for i in range(len(data1))], data1['Accuracy'].tolist(),label='long-term')
plt.plot([str(i) for i in range(len(data1))], data2['Accuracy'].tolist(), label='pure')

plt.legend()
plt.show()