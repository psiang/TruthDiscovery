from matplotlib import pyplot as plt
import pandas as pd
import csv

# 参数依次为list,抬头,X轴标签,Y轴标签,XY轴的范围
def draw_hist(myList,Title,Xlabel,Ylabel):
    plt.hist(myList,100)
    plt.xlabel(Xlabel)
    plt.ylabel(Ylabel)
    plt.title(Title)
    plt.show()


data = pd.read_csv("./workers.csv", header=0)
value = []
for x in range(len(data)):
    w = data.iloc[x].loc['worker']
    v = data.iloc[x].loc['value']
    value.append(v)

draw_hist(value,'AreasList','Area','number')   # 直方图展示