import matplotlib.pyplot as plt
import numpy as np
import random
import math
import copy


# 画直方图
def draw_hist(my_list, title, x_label, y_label):
    plt.hist(my_list)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.show()


# 测试数据的分析，生成均值、方差和分布
def analysis_data(answer):
    nw = len(answer)
    nq = len(answer[0])
    worker_of_query = [0] * nq
    query_of_worker = [0] * nw
    print("Worker:" + str(nw) + "\tQuery:" + str(nq))

    # 统计工人回答问题数 和 问题被工人回答数
    for i in range(nw):
        for j in range(nq):
            if answer[i][j] != -1:
                worker_of_query[j] += 1
                query_of_worker[i] += 1

    # 画工人回答问题数的频率 和 问题被工人回答数的频率直方图
    draw_hist(worker_of_query,
              "Distribution - worker_of_querys", "worker_of_querys", "frequency")
    draw_hist(query_of_worker,
              "Distribution - query_of_workers", "query_of_workers", "frequency")
    print("mean worker_of_query:", np.mean(worker_of_query))
    print("mean query_of_worker:", np.mean(query_of_worker))
    print("var  worker_of_query:", np.var(worker_of_query))
    print("var  query_of_worker:", np.var(query_of_worker))


# 处理数据成工人和任务的表格
def pre_assign(votes, ground_truths):
    nw = 0
    nq = 0
    nc = 0
    query = {}
    worker = {}
    category = {}
    ground_truths_flag = {}
    truth = []

    # 统计任务数和工人数和选项数
    for g in ground_truths:
        ground_truths_flag.update({g[0]: 0})
        if category.get(g[1], "Null") == "Null":
            category.update({g[1]: nc})
            nc += 1
    for v in votes:
        if ground_truths_flag.get(v[0], "Null") != "Null":
            ground_truths_flag.update({v[0]: 1})
            if category.get(v[2], "Null") == "Null":
                category.update({v[2]: nc})
                nc += 1
    for g in ground_truths:
        if query.get(g[0], "Null") == "Null" and ground_truths_flag.get(g[0], "Null") == 1:
            query.update({g[0]: nq})
            truth.append(category[g[1]])
            nq += 1
    for v in votes:
        if worker.get(v[1], "Null") == "Null" and query.get(v[0], "Null") != "Null":
            worker.update({v[1]: nw})
            nw += 1

    answer = [([-1] * nq) for i in range(nw)]
    replay = [[([-1] * nc) for j in range(nq)] for i in range(nw)]
    for v in votes:
        if query.get(v[0], "Null") != "Null" and worker.get(v[1], "Null") != "Null":
            replay[worker[v[1]]][query[v[0]]][category[v[2]]] += 1

    for i in range(nw):
        for j in range(nq):
            max_k = max(replay[i][j])
            max_list = []
            if max_k != -1:
                for k in range(nc):
                    if max_k == replay[i][j][k]:
                        max_list.append(k)
                answer[i][j] = random.choice(max_list)
    # analysis_data(answer)
    return answer, truth, category


# 判断概率是否发生
def flip_or_not(prob):
    if random.random() <= prob:
        return 1
    else:
        return 0


# 计算正确率
def get_error(truth, ground_truth):
    count = 0.0
    for ti, gti in zip(truth, ground_truth):
        if ti != gti:
            count += 1
    count = count / len(ground_truth)
    return count


# onelayer加噪
def perturb_onelayer(answers, pf, nc):
    nw = len(answers)
    nq = len(answers[0])
    answers_perturbed = copy.deepcopy(answers)
    for i in range(nw):
        for j in range(nq):
            if answers_perturbed[i][j] != -1 and flip_or_not(pf):
                to_list = [k for k in range(nc) if k != answers_perturbed[i][j]]
                answers_perturbed[i][j] = random.choice(to_list)
    return answers_perturbed


# twolayer加噪
def perturb_twolayer(answers, pr, nc, style):
    nw = len(answers)
    nq = len(answers[0])
    answers_perturbed = copy.deepcopy(answers)
    for i in range(nw):
        pf = random_pr(pr, style)
        for j in range(nq):
            if answers_perturbed[i][j] != -1 and flip_or_not(pf):
                to_list = [k for k in range(nc) if k != answers_perturbed[i][j]]
                answers_perturbed[i][j] = random.choice(to_list)
    return answers_perturbed


# MV
def mv(answers, nc):
    nw = len(answers)
    nq = len(answers[0])
    truth = [0] * nq
    truth_vote = [([0] * nc) for i in range(nq)]

    for j in range(nq):
        for i in range(nw):
            if answers[i][j] != -1:
                truth_vote[j][answers[i][j]] += 1

    for i in range(nq):
        max_c = max(truth_vote[i])
        max_list = []
        for j in range(nc):
            if max_c == truth_vote[i][j]:
                max_list.append(j)
        truth[i] = random.choice(max_list)

    return truth


# TD
def td(answers, nc):
    nw = len(answers)
    nq = len(answers[0])
    former_truth = [0] * nq
    weight = [1] * nw
    truth = [0] * nq

    for time in range(100):
        truth.clear()
        truth = [0] * nq
        truth_vote = [([-2147483647] * nc) for i in range(nq)]
        for j in range(nq):
            for i in range(nw):
                if answers[i][j] != -1:
                    if truth_vote[j][answers[i][j]] == -2147483647:
                        truth_vote[j][answers[i][j]] = 0
                    truth_vote[j][answers[i][j]] += weight[i] + 10

        for i in range(nq):
            max_c = max(truth_vote[i])
            max_list = []
            for j in range(nc):
                if max_c == truth_vote[i][j]:
                    max_list.append(j)
            truth[i] = random.choice(max_list)

        difference = 0
        for i in range(nq):
            if truth[i] != former_truth[i] and time != 0:
                difference += 1
            former_truth[i] = truth[i]
        if difference <= 0 and time != 0:
            break

        for i in range(nw):
            ac = 0.0
            su = 0.0
            for j in range(nq):
                if answers[i][j] != -1:
                    su += 1
                    if answers[i][j] == truth[j]:
                        ac += 1
            ac = ac / su
            if ac == 1:
                ac -= 0.0001
            if ac == 0:
                ac += 0.0001
            weight[i] = math.log(ac/(1-ac))

    return truth


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
    return pf


# 执行函数比较不同加噪强度下的单双层MV、TD的错误率偏差
def execute_style(votes, ground_list):
    n = 100
    answers, ground_truth, category = pre_assign(votes, ground_list)
    nc = len(category)

    style_list = ['Uniform', 'Beta', 'Exponential', 'Gamma']
    e_list_origin = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.01, 0.001, 0.0]
    for style in style_list:
        print(style)
        ac_list = []
        if style == 'Exponential':
            e_list = [0.9648513868451118, 0.8475331654689704, 0.730388397937257,
                      0.6097469478991127, 0.48101835901641726, 0.34337225181842174,
                      0.19847853464215953, 0.043426372091174004, -0.12310288754782026,
                      -0.3106643476053096, -0.4978324695829641, -0.5176191828087624,
                      -0.522867381837526]
        elif style == "Gamma":
            e_list = [0.6369664713130023, 0.5117903314858268, 0.382904052734375,
                      0.24208450247533614, 0.10788107617986577, -0.040507247958678286,
                      -0.1987433713366052, -0.3617469326063796, -0.5386977658320813,
                      -0.7367098941658703, -0.9384765625, -0.9521432715541753,
                      -0.9541385503868145]
        else:
            e_list = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.01, 0.001, 0.0]
        for e in e_list:
            print(" ", e)
            pr = equal_pr(e, style)
            # TD with two-layer
            td_error_twolayer = 0.0
            for i in range(n):
                answers_perturbed = perturb_twolayer(answers, pr, nc, style)
                td_error_twolayer += get_error(td(answers_perturbed, nc), ground_truth)
                del answers_perturbed
            td_error_twolayer /= n
            ac_list.append(1 - td_error_twolayer)
        plt.plot(e_list_origin, ac_list, label=style)
    plt.xlabel('ε')
    plt.ylabel('accuracy')
    plt.title('Accuracy of distribution')
    plt.legend()
    plt.show()


def execute(votes, ground_list):
    n = 100
    answers, ground_truth, category = pre_assign(votes, ground_list)
    nc = len(category)

    mv_error = 0.0
    for i in range(n):
        mv_error += get_error(mv(answers, nc), ground_truth)
    mv_error /= n

    td_error = 0.0
    for i in range(n):
        td_error += get_error(td(answers, nc), ground_truth)
    td_error /= n

    print("MVerror:", round(mv_error, 8), "TDerror:", round(td_error, 8))
    print("ε\tMV_onelayer\tMV_twolayer\tTD_onelayer\tTD_twolayer")

    e_list = [2.0, 1.7, 1.5, 1.3, 1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.01, 0.001, 0.0]
    for e in e_list:
        print(e, end='\t')
        pf = (nc - 1) / (math.exp(e) + nc - 1)
        b = 2 * (nc - 1) / (math.exp(e) + nc - 1)

        # MV with one-layer
        mv_error_onelayer = 0.0
        for i in range(n):
            answers_perturbed = perturb_onelayer(answers, pf, nc)
            mv_error_onelayer += get_error(mv(answers_perturbed, nc), ground_truth)
            del answers_perturbed
        mv_error_onelayer /= n
        print(round(mv_error_onelayer - mv_error, 8), end='\t')

        # MV with two-layer
        mv_error_twolayer = 0.0
        for i in range(n):
            answers_perturbed = perturb_twolayer(answers, b, nc)
            mv_error_twolayer += get_error(mv(answers_perturbed, nc), ground_truth)
            del answers_perturbed
        mv_error_twolayer /= n
        print(round(mv_error_twolayer - mv_error, 8), end='\t')

        # TD with one-layer
        td_error_onelayer = 0.0
        for i in range(n):
            answers_perturbed = perturb_onelayer(answers, pf, nc)
            td_error_onelayer += get_error(td(answers_perturbed, nc), ground_truth)
            del answers_perturbed
        td_error_onelayer /= n
        print(round(td_error_onelayer - td_error, 8), end='\t')

        # TD with two-layer
        td_error_twolayer = 0.0
        for i in range(n):
            answers_perturbed = perturb_twolayer(answers, b, nc)
            td_error_twolayer += get_error(td(answers_perturbed, nc), ground_truth)
            del answers_perturbed
        td_error_twolayer /= n
        print(round(td_error_twolayer - td_error, 8), end='\n')
