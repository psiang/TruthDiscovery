
import numpy as np

import MajorityVoting
import math
import copy


class emMultiClass:
    def __init__(self, graph, scale):

        self.G_SCALE=scale    # the rating scale
        self.priorAlpha = {}  # user reliability
        self.priorBeta = {}   # item difficulty level
        self.priorZk = 0.0
        self.probZj = []
        self.dQdAlpha = {}
        self.dQdBeta = {}
        self.graph = graph
        self.alpha = {}
        self.beta = {}


    def logProbL(self, lij, z, alpha_i, beta_j):
        if z == lij:
           return self.getLogSigma(alpha_i, beta_j)
        else:
           return -1 * math.log(len(self.G_SCALE)-1) + self.getLogOneMinusSigma(alpha_i, beta_j)


    def getSigma(self, alpha_i, beta_j):
        sigma = 1.0/(1.0 + math.exp(-1*math.exp(beta_j) * alpha_i))
        return sigma


    def getLogSigma(self, alpha_i, beta_j):
        logSigma = math.log(self.getSigma(alpha_i, beta_j))

        if math.isinf(logSigma) and logSigma < 0:  # Or could use x == float("-inf")
            logSigma = -1*math.exp(beta_j) * alpha_i

        return logSigma


    def getLogOneMinusSigma(self, alpha_i, beta_j):
        logOneMinusSigma = math.log(1-self.getSigma(alpha_i, beta_j))
        if logOneMinusSigma == float("-inf"):
            logOneMinusSigma = -1 * math.exp(beta_j) * alpha_i
        return logOneMinusSigma


    def gaussPDF(self, x):
        return 1.0/math.sqrt(2*math.pi)*math.exp(-math.pow(x,2)/2)


    def computeQ(self):
        # Calculate the Q function on page 3
        Q = 0.0
        # The expectation of the sum of priors over all tasks
        for lj in self.probZj:
            for lk in lj:
                Q += lk * math.log(self.priorZk)
        for it in self.graph.items:
            for u in it.users:
                for g in self.G_SCALE:
                    Q += self.probZj[it.id][g-1] * self.logProbL(u.grade[it], g, self.alpha[u], self.beta[it])

        # Set Gaussian prior for alpha and beta
        for u in self.graph.users:
            Q += math.log(self.gaussPDF(self.alpha[u] - self.priorAlpha[u]))

        for it in self.graph.items:
            Q += math.log(self.gaussPDF(self.beta[it] - self.priorBeta[it]))

        return Q


    def doGradientAscent(self, iterations, stepsize, tolerance):   # d(J_theda)
        iter = 0
        oldQ = self.computeQ()
        Q = oldQ
        alphaClone = {}
        betaClone = {}
        for u in self.graph.users:
            alphaClone[u] = self.alpha[u]
        for it in self.graph.items:
            betaClone[it] = self.beta[it]
        while True:
            oldQ = Q
            for u in self.graph.users:
                alphaClone[u] = self.alpha[u]
            for it in self.graph.items:
                betaClone[it] = self.beta[it]
            
            self.calcGradient()
            self.ascend(stepsize)
            Q = self.computeQ()
            iter += 1
            if not (iter < iterations and abs((Q-oldQ)/oldQ) > tolerance and Q > oldQ):
                break
        if Q < oldQ:
            for u in self.graph.users:
                self.alpha[u] = alphaClone[u]
            for it in self.graph.items:
                self.beta[it] = betaClone[it]


    def calcGradient(self):
        for u in self.graph.users:
            self.dQdAlpha[u] = -(self.alpha[u]-self.priorAlpha[u])

        for it in self.graph.items:
            self.dQdBeta[it] = -(self.beta[it]-self.priorBeta[it])

        for it in self.graph.items:
            for u in it.users:
                sigma = self.getSigma(self.alpha[u], self.beta[it])
                for g in self.G_SCALE:
                    delta = self.deltaFunc(g, u.grade[it])
                    self.dQdAlpha[u] += self.probZj[it.id][g-1] * ((delta-sigma) * math.exp(self.beta[it]) + (1-delta) * math.log(len(self.G_SCALE)-1))
                    self.dQdBeta[it] += self.probZj[it.id][g-1] * ((delta-sigma) * self.alpha[u] + (1-delta) * math.log(len(self.G_SCALE)-1))


    def deltaFunc(self, g, lij):
        if g == lij:
            return 1
        else:
            return 0


    def ascend(self, stepsize):
        for u in self.graph.users:
            self.alpha[u] += stepsize * self.dQdAlpha[u]

        for it in self.graph.items:
            self.beta[it] += stepsize * self.dQdBeta[it]


    def eStep(self):
        for it in self.graph.items:
            for g in self.G_SCALE:
                self.probZj[it.id][g-1] = math.log(self.priorZk)
                for u in it.users:
                    self.probZj[it.id][g-1] += self.logProbL(u.grade[it], g, self.alpha[u], self.beta[it])
                    

        # Exponentiate and renormalize
        for it in self.graph.items:
            sum_it = 0.0
            for g in self.G_SCALE:
                self.probZj[it.id][g-1] = math.exp(self.probZj[it.id][g-1])
                sum_it += self.probZj[it.id][g-1]
            tlist = [x/sum_it for x in self.probZj[it.id]]
            self.probZj[it.id] = tlist[:]


    def mStep(self):
        self.doGradientAscent(25, 0.01, 0.01)


    def EM(self, graph, max_iter, epsilon):
        self.eStep()
        lastQ = self.computeQ()
        self.mStep()
        Q = self.computeQ()
        change = (Q-lastQ)/lastQ
        while change > epsilon:
            lastQ = Q
            # E step, estimate P(Z|L, alpha, beta)
            self.eStep()
            # Mstep, estimate alpha and beta
            self.mStep()

            Q = self.computeQ()
            change = abs((Q-lastQ)/lastQ)
            print "After M-Step: Q = ", Q
            print "Change ratio: ", change
        self.eStep()



    # Convergence condition could be either max_iter or epsilon

    def expectation_maximization(self, max_iter=50, epsilon=0.001):
        em_value = {}
        for u in self.graph.users:
            self.priorAlpha[u] = 1.0
        for it in self.graph.items:
            self.probZj.append([])
        for it in self.graph.items:
            self.priorBeta[it] = 1.0
            self.probZj[it.id] = [0.0]*len(self.G_SCALE)  # Pr(z_j) for each item j on label c

        # Initialize alpha and beta with their priors
        for u in self.graph.users:
            self.alpha[u] =self.priorAlpha[u]
        for it in self.graph.items:
            self.beta[it] = self.priorBeta[it]
        self.priorZk = 1.0/len(self.G_SCALE)  # Pr(z_j=k)=1/k

        self.EM(self.graph, max_iter, epsilon)

        # get the results
        for it in self.graph.items:
            for g in self.G_SCALE:
                if self.probZj[it.id][g-1] == max(self.probZj[it.id]):
                    em_value[it] = g
        return self.alpha, em_value


        