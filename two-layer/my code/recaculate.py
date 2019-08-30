import matplotlib.pyplot as plt
import numpy as np
import random
import math
import copy

# 找到对应分布类型的等价参数
def random_pr(pr, style):
    pf = 0
    if style == "Uniform":
        a = 0
        b = pr
        pf = random.uniform(a, b)
    elif style == "Beta":
        alpha = pr
        beta = 1 - pr
        pf = random.betavariate(alpha, beta)
    elif style == "Exponential":
        lambd = pr
        pf = random.expovariate(lambd)
        if pf > 1:
            pf = 1
    elif style == "Gamma":
        alpha = pr
        beta = 1
        pf = random.gammavariate(alpha, beta)
        if pf > 1:
            pf = 1
    elif style == "Normal":
        mu = pr
        sigma = 0.3
        pf = random.gauss(mu, sigma)
        if pf > 1:
            pf = 1
        if pf < 0:
            pf = 0
    return pf


# 找到对应分布类型的等价参数
def equal_pr(e, style):
    if style == "Uniform":
        return 2 / (math.exp(e) + 1)
    elif style == "Beta":
        return 1 / (math.exp(e) + 1)
    elif style == "Exponential":
        return math.exp(e) + 1
    elif style == "Gamma":
        return 1 / (math.exp(e) + 1)
    elif style == "Normal":
        return 1 / (math.exp(e) + 1)


# 执行函数比较不同加噪强度下的单双层MV、TD的错误率偏差
def execute_style():
    n = 1000000
    style_list = ['Normal']
    e_list = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.01, 0.001, 0.0]
    for style in style_list:
        print(style)
        for e in e_list:
            pf = 1 / (math.exp(e) + 1)
            left = -15.0
            right = 2.0
            mid = 0.0
            while right - left > 0.0000000000000001:
                mid = (left + right) / 2
                pr = equal_pr(mid, style)
                x = 0.0
                for i in range(n):
                    x += random_pr(pr, style)
                x = x / n
                print(left,"-",right,":",x)
                if x > pf:
                    left = mid
                else:
                    right = mid
            mid = (left + right) / 2
            print(mid)



execute_style()
