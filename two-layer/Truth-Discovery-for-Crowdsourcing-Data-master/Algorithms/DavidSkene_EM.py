import numpy as np
import math
import sys
import csv
import os
import random

class ds_em:
    def __init__(self, graph, iterations = 20, epsilon = 0.001, scale):
        self.graph = graph
        self.pi_k = []   # probability of of an item has label k (prior)
        self.theta = {}  # distribution of user's given label, confusion matrix of the workers
        self.zi = {}     # true label of items, Pr(Zi = k|D)
        self.G_SCALE = scale
        self.max_iter = iterations
        self.epsilon = epsilon


    def em(self):
        iteration = 0
        old_posterior = float("inf")
        for it in self.graph.items:
            self.zi[it] = [0.0] * len(self.G_SCALE)
            for g in self.G_SCALE:
                self.zi[it][g-1] = 1.0/len(self.G_SCALE)

        while iteration < self.max_iter:
            self.eStep()

            log_posterior = self.mStep()
            if iteration == 0:
                print "After iteration: ", iteration, ", log_posterior is: ", log_posterior
            else:
                change = abs((log_posterior - old_posterior)/old_posterior)
                print "After iteration: ", iteration, ", log_posterior is: ", log_posterior
                if change < self.epsilon:
                    break
            old_posterior = log_posterior
            iteration += 1

        self.eStep()



    def eStep(self):
        for it in self.graph.items:
            self.zi[it] = self.pi_k[:]
            for u in it.users:
                for g in self.G_SCALE:
                    self.zi[it][g-1] = self.zi[it][g-1] * self.theta[u][g-1][u.grade[it]-1]

        # Renormalize
        for it in self.graph.items:
            sum_zi = sum(self.zi[it])
            self.zi[it] = [x/sum_zi for x in self.zi[it]]


    def mStep(self):
        # add beta smoothing to pi_k
        beta = 0.01
        self.pi_k = [beta] * len(self.G_SCALE)

        for g in self.G_SCALE:
            for it in self.graph.items:
                self.pi_k[g-1] += self.zi[it][g-1]
        sum_pi = sum(self.pi_k)
        self.pi_k = [x/sum_pi for x in self.pi_k]

        # add alpha smoothing to theta
        alpha = 0.01
        count = {}
        for u in self.graph.users:
            count[u] = []
            for g1 in self.G_SCALE:
                count[u].append([])
                count[u][g1-1] = [alpha] * len(self.G_SCALE)
                for it in u.items:
                    count[u][g1-1][u.grade[it]-1] += self.zi[it][g1-1]
        for u in self.graph.users:
            for g in self.G_SCALE:
                sum_count = np.sum(count[u][g-1])
                self.theta[u][g-1] = [c/sum_count for c in count[u][g-1]]

        P = {}
        for it in self.graph.items:
            P[it] = self.pi_k[:]
            for u in it.users:
                for g in self.G_SCALE:
                    P[it][g-1] = P[it][g-1] * self.theta[u][g-1][u.grade[it]-1]

        log_posterior = 0.0
        for it in self.graph.items:
            log_posterior = log_posterior + math.log(sum(P[it]))

        return log_posterior


    def delta(self, g1, g2):
        if g1 == g2:
            return 0.7    # original is 0.7
        else:
            return 0.3/len(self.G_SCALE)   # original is 0.3


    def DS(self):
        '''MAP - maximize a posterior'''
        ds_value = {}
        # Initialization
        # Random Initialization
        for u in self.graph.users:
            self.theta[u] = [0.0] *len(self.G_SCALE)
            for g1 in self.G_SCALE:
                self.theta[u][g1-1] = [0.0] * len(self.G_SCALE)
                for g2 in self.G_SCALE:
                    self.theta[u][g1-1][g2-1] = self.delta(g1, g2)

        

        self.pi_k = [1.0/len(self.G_SCALE)]*len(self.G_SCALE)

        # EM iterations
        self.em()

        theta_value = {}
        for u in self.graph.users:
            theta_value[u] = []
            for g1 in self.G_SCALE:
                for g2 in self.G_SCALE:
                    theta_value[u].append(u.name)
                    theta_value[u].append(g1)
                    theta_value[u].append(g2)
                    theta_value[u].append(self.theta[u][g1-1][g2-1])
        direct = os.path.dirname(__file__)
        filename = os.path.join(direct, '/Pycharm Workspace/Data/DS_EM_output.csv')
        with open(filename, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['worker', 'true label', 'observation', 'prob'])
            for u in self.graph.users:
                writer.writerow(theta_value[u])

        # Get the output as results
        for it in self.graph.items:
            for g in self.G_SCALE:
                if self.zi[it][g-1] == max(self.zi[it]):
                    ds_value[it] = g

        return ds_value



