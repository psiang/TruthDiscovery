

import numpy as np
import math
from random import randint

import MajorityVoting
import average_voting

N_ITERATIONS = 20



# weighted voting for categorical data, with 0-1 loss
def weighted_voting_cat(graph, G_SCALE):
    # initialize the truths
    # Assume the initialization is first based on MV, in which each worker's weight is same at the beginning
    chi = MajorityVoting.majority_voting(graph)  # truths of items
    
    weights = {}
    for i in range(N_ITERATIONS):
        # Update the users' weights while fixing the truths of the items
        sum_distance_all = 0.0  # d(truth, observation) for all users on all the items
        for u in graph.users:
            sum_distance_k = 0.0
            for it in u.items:
                if u.grade[it] <> chi[it]:
                    sum_distance_k += 1.0
                    sum_distance_all += 1.0
            if sum_distance_k == 0 or sum_distance_all == 0:
                weights[u] = -1  # indicates that the weights of the user should be infinity, which is a perfect user
            else:
                weights[u] = -1 * math.log(sum_distance_k/sum_distance_all)

        # update the true labels of the items while fixing the user weights and all the other items' truth labels
        for it in graph.items:
            weighted_scale = {}
            for g in G_SCALE:
                f_sum = 0
                for u in it.users:
                    if g == u.grade[it]:
                        if weights[u] == -1:
                            f_sum = -1
                        else:
                            if f_sum <> -1:
                                f_sum += weights[u]
                weighted_scale[g] = f_sum
            # the true value of the item should minimize the f(W, chi)
            truth = 1
            for key in weighted_scale:
                if weighted_scale[key] == -1:
                    truth = key
                    break
                elif weighted_scale[key] > weighted_scale[truth]:
                    truth = key
            chi[it] = truth
    return chi


# weighted voting for numerical data, with normalized squared loss (variance)
def weighted_voting_num(graph):
    # Initialize the truth of the items, Averaging approach are used here
    chi = average_voting.average(graph)
    weights = {}
    for i in range(N_ITERATIONS):
        # Update the user's weights while fixing the truths of the items
        sum_distance_all = 0
        for u in graph.users:
            sum_distance_k = 0
            observed_grade_k = []
            for it in u.items:
                squared_d = (chi[it]-u.grade[it])**2
                for u_prime in it.users:
                    observed_grade_k.append(u_prime.grade[it])
                stdev = np.std(np.array(observed_grade_k))
                sum_distance_k += squared_d/stdev  # normalized squared loss
                sum_distance_all += squared_d/stdev
            weights[u] = -1*math.log(sum_distance_k/sum_distance_all)

        # Update the true labels of the items while fixing the users' weights and other items' truths
        for it in graph.items:
            sum_weights = 0
            sum_weighted_grades = 0
            for u in it.users:
                sum_weights += weights[u]
                sum_weighted_grades += weights[u]*u.grade[it]
            chi[it] = sum_weighted_grades/sum_weights
    return chi
