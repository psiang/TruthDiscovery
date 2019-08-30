from matplotlib import pyplot as plt
import pandas as pd
import csv


now_work = "d_jnproduct"
work = "Accuracy"#"RMSTE", "RMSRE", "Accuracy"

pic_name = {"Accuracy":"AR", "RMSTE":"MARE"}
sig = {'HisEM':'d-', 'LFCC':'p--', 'CATD':'s--', 'MV':'*--', 'PM':'+--', 'BCC':'x--'}
algorithm = ['HisEM', 'LFCC', 'MV', 'CATD', 'PM']
label_al = ['Our', 'LFCC', 'MV', 'CATD', 'PM', 'BCC']
color_al = ['#E83015', 'royalblue', 'm', 'forestgreen', 'darkcyan', 'goldenrod', 'chocolate']
names = {"s4_Dogdata", "barzanMozafari_binary", "d_Duck", "AdultContent2_multi", "d_jnproduct"}

if now_work == "round":
    Ntime = 100
    acc = [([0] * 20) for i in range(len(algorithm))]
    for time in range(Ntime):
        for algo_i in range(len(algorithm)):
            data = pd.read_csv("./result/" + now_work + "/%s/result_%s.csv" % (algorithm[algo_i], time), header=0)
            for i in range(len(data)):
                acc[algo_i][i] += abs(data.iloc[i].loc[work])

    for i in range(20):
        for algo_i in range(len(algorithm)):
            acc[algo_i][i] = (acc[algo_i][i] / Ntime)

    for algo_i in range(len(algorithm)):
        plt.plot([str(i) for i in range(1,21)], acc[algo_i], sig[algorithm[algo_i]], lw=2.2, label=label_al[algo_i], color=color_al[algo_i])
    #plt.ylim(0.0, 1.0)

    ax = plt.gca()
    ax.set_xticks([1,3,5,7,9,11,13,15,17,19])
    plt.rcParams['figure.dpi'] = 300 #分辨率
    plt.tick_params(labelsize=17)
    plt.ylabel(pic_name[work], fontsize=17)
    plt.xlabel("Rounds", fontsize=17)
    plt.legend(loc='best',ncol=3)
    plt.tight_layout()
    plt.savefig("./picture/%s_rounds.pdf" % pic_name[work])
    plt.show()

elif now_work in names:
    '''Ntime = 100
    Nday = 20
    acc = [([0] * Nday) for i in range(len(algorithm))]
    for time in range(0,Ntime):
        for algo_i in range(len(algorithm)):
            data = pd.read_csv("./result/" + now_work + "/1/%s/result_%s.csv" % (algorithm[algo_i], time), header=0)
            for i in range(len(data)):
                acc[algo_i][i] += abs(data.iloc[i].loc[work])

    for i in range(Nday):
        for algo_i in range(len(algorithm)):
            acc[algo_i][i] = (acc[algo_i][i] / Ntime)

    for algo_i in range(len(algorithm)):
        plt.plot([str(i) for i in range(1,Nday + 1)], acc[algo_i], sig[algorithm[algo_i]], lw=2.2, label=label_al[algo_i], color=color_al[algo_i])
    #plt.ylim(0.0, 1.0)

    ax = plt.gca()
    ax.set_xticks([1,3,5,7,9,11,13,15,17,19])
    plt.rcParams['figure.dpi'] = 300 #分辨率
    plt.tick_params(labelsize=17)
    plt.ylabel(pic_name[work], fontsize=17)
    plt.xlabel("No. of current round", fontsize=17)
    plt.legend(loc='best',ncol=3)
    plt.tight_layout()
    plt.savefig("./picture/%s_%s.pdf" % (pic_name[work], now_work))
    plt.show()'''

    rates = ['10', '15', '20', '25', '30', '35', '40']
    Ntime = 1
    acc = [([0] * len(rates)) for i in range(len(algorithm))]
    for x in range(len(rates)):
        for time in range(0, Ntime):
            for algo_i in range(len(algorithm)):
                data = pd.read_csv("./result/" + now_work + "/%s/%s/result_%s.csv" % (rates[x], algorithm[algo_i], time), header=0)
                for i in range(len(data)):
                    acc[algo_i][x] += abs(data.iloc[i].loc[work])

    for x in range(len(rates)):
        for algo_i in range(len(algorithm)):
            acc[algo_i][x] = (acc[algo_i][x] / int(rates[x]))

    for algo_i in range(len(algorithm)):
        plt.plot([str(i) for i in range(1,len(rates) + 1)], acc[algo_i], sig[algorithm[algo_i]], lw=2.2, label=label_al[algo_i], color=color_al[algo_i])
    #plt.ylim(0.0, 1.0)

    ax = plt.gca()
    #ax.set_xticks(rates)
    plt.rcParams['figure.dpi'] = 300 #分辨率
    plt.tick_params(labelsize=17)
    plt.ylabel(pic_name[work], fontsize=17)
    plt.xlabel("the number of divided rounds", fontsize=17)
    plt.legend(loc='best',ncol=3)
    plt.tight_layout()
    plt.savefig("./picture/%s_%s.pdf" % (pic_name[work], now_work))
    plt.show()

else:
    Ntime = 100
    #rates = ['0.04', '0.06', '0.08', '0.10', '0.12', '0.14']   #sigma
    #rates = ['0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9']
    rates = ['0.5','0.55','0.6','0.65','0.7','0.75','0.8'] #mu
    #rates = ['0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1.0']
    #rates = ['1', '2', '3', '4', '5', '6']
    acc = [([0] * len(rates)) for i in range(len(algorithm))]
    for r in range(len(rates)):
        for time in range(Ntime):
            for algo_i in range(len(algorithm)):
                data = pd.read_csv("./result/" + now_work + "/%s/%s/result_%s.csv" % (rates[r], algorithm[algo_i], time), header=0)
                acc[algo_i][r] += abs(data.iloc[len(data) - 1].loc[work])

    for r in range(len(rates)):
        for algo_i in range(len(algorithm)):
            acc[algo_i][r] = (acc[algo_i][r] / Ntime)

    for algo_i in range(len(algorithm)):
        plt.plot([rates[i-1] for i in range(1,len(rates)+1)], acc[algo_i], sig[algorithm[algo_i]], lw=2.2, label=label_al[algo_i], color=color_al[algo_i])
    #plt.ylim(0.0, 1.0)

    ax = plt.gca()
    #ax.set_xticks([r"$\frac{%s}{6}$"%r for r in rates])
    plt.rcParams['figure.dpi'] = 300 #分辨率
    plt.tick_params(labelsize=17)
    plt.ylabel(pic_name[work], fontsize=17)
    plt.xlabel(r"$parameter\ \sigma$", fontsize=17)
    plt.legend(loc='best',ncol=3)
    plt.tight_layout()
    plt.savefig("./picture/%s_%s.pdf" % (pic_name[work], now_work))
    plt.show()
