import math
import csv
import random
import sys

class EM:
    def __init__(self,e2wl,w2el,label_set):
        self.e2wl = e2wl
        self.w2el = w2el
        self.workers = self.w2el.keys()
        self.label_set = label_set



    # E-step
    def Update_e2lpd(self):

        l2epd = {}
        for base_label in self.label_set:
            epd = {}
            for example, worker_label_set in self.e2wl.items():
                epd.update({example: 1})
                for w, label in worker_label_set:
                    if base_label == label:
                        epd[example] *= self.wm[w]
                    else:
                        epd[example] *= (1 - self.wm[w]) / (len(self.label_set) - 1)
            l2epd.update({base_label: epd})

        lpd = {}
        for base_label in self.label_set:
            lpd.update({base_label: 0})
            enum = 0
            for example in self.e2wl.keys():
                lpd[base_label] += self.e2lpd[example][base_label]
                enum += 1

        self.e2lpd = {}
        for example in self.e2wl.keys():
            pd = {}
            total = 0
            for label in self.label_set:
                pd.update({label: l2epd[label][example] * lpd[label]})
                total += l2epd[label][example] * lpd[label]
            for label in self.label_set:
                pd[label] /= total
            self.e2lpd.update({example: pd})


        #M-step
    def Update_wm(self):
        for w in self.workers:
            self.wm[w] = 0

        for w in self.w2el:
            sum_w2lpd = 0
            for example, label in self.w2el[w]:
                sum_w2lpd += self.e2lpd[example][label]
            self.wm[w] = (self.alph[w] + sum_w2lpd) / (self.alph[w] + self.beta[w] + len(self.w2el[w]))

        return self.wm







    #initialization
    def Init_ab(self):
        alph = {}
        beta = {}
        for worker in self.workers:
            if alph.get(worker, "None") == "None":
                alph.update({worker: 1})
                beta.update({worker: 1})

        return alph, beta

    def Init_e2lpd(self):
        e2lpd = {}
        for example, worker_label_set in self.e2wl.items():
            lpd = {}
            total = 0
            for label in self.label_set:
                lpd[label] = 0

            for (w, label) in worker_label_set:
                lpd[label] += 1
                total+= 1

            if not total:
                for label in self.label_set:
                    lpd[label] = 1.0 / len(self.label_set)
            else:
                for label in self.label_set:
                    lpd[label] = lpd[label] * 1.0 / total

            e2lpd[example] = lpd

        return e2lpd

    def Init_wm(self):
        wm = {}
        for worker in self.workers:
            if wm.get(worker, "None") == "None":
                wm.update({worker: 0})
        return wm

    def Run(self, iterr = 20):
        self.alph, self.beta = self.Init_ab()
        self.e2lpd = self.Init_e2lpd()
        self.wm = self.Init_wm()
        wm_old = self.wm

        while iterr > 0:

            # M-step
            self.Update_wm()

            # E-step
            self.Update_e2lpd()

            # compute the likelihood
            # print self.computelikelihood()

            # convergence
            if iterr > 0:
                count = 0
                for worker in self.workers:
                    count += (wm_old[worker] - self.wm[worker]) ** 2
                count /= len(self.workers)
                if count < 0.00000001:
                    wm_old = self.wm
                    break
            wm_old = self.wm

            iterr -= 1

        return self.e2lpd, self.wm


###################################
# The above is the EM method (a class)
# The following are several external functions
###################################

def getaccuracy(truthfile, e2lpd, label_set):
    e2truth = {}
    f = open(truthfile, 'r')
    reader = csv.reader(f)
    next(reader)

    for line in reader:
        example, truth = line
        e2truth[example] = truth

    tcount = 0
    count = 0

    for e in e2lpd:

        if e not in e2truth:
            continue

        temp = 0
        for label in e2lpd[e]:
            if temp < e2lpd[e][label]:
                temp = e2lpd[e][label]

        candidate = []

        for label in e2lpd[e]:
            if temp == e2lpd[e][label]:
                candidate.append(label)

        truth = random.choice(candidate)

        count += 1

        if truth == e2truth[e]:
            tcount += 1

    return tcount*1.0/count


def gete2wlandw2el(datafile):
    e2wl = {}
    w2el = {}
    label_set=[]

    f = open(datafile, 'r')
    reader = csv.reader(f)
    next(reader)

    for line in reader:
        worker, example, label = line
        if example not in e2wl:
            e2wl[example] = []
        e2wl[example].append([worker,label])

        if worker not in w2el:
            w2el[worker] = []
        w2el[worker].append([example,label])

        if label not in label_set:
            label_set.append(label)

    return e2wl,w2el,label_set



if __name__ == "__main__":

    datafile = sys.argv[1]
    e2wl,w2el,label_set = gete2wlandw2el(datafile) # generate structures to pass into EM
    iterations = 20 # EM iteration number
    e2lpd, wm= EM(e2wl,w2el,label_set).Run(iterations)

    print(wm)
    print(e2lpd)

