"""
Time: 2022-11-21
Author:   Chen jiangxi
Describe: Terminal appointment system design by non-stationary M(t)Ekc(t) queueing model and genetic algorithm https://www.sciencedirect.com/science/article/pii/S0925527313003824
"""

import math

def bisection(l_last, lam, mu, c):
    left, right = 0, 1
    rho = (left + right) / 2
    l = max(l_last + lam - c * mu * rho, 0)
    l_est = esitimate_len(rho, c)
    
    while (abs(l - l_est) > 0.0001):
        if l_est > l:
            right = rho
        elif l_est < l:
            left = rho
        else:
            break
        rho = (left + right) / 2
        l = max(l_last + lam - c * mu * rho, 0)
        l_est = esitimate_len(rho, c)

    return l


def esitimate_len(rho, c):
    s = 0
    for h in range(c):
        s += pow(rho * c, h) / math.factorial(h)
    P0 = 1 / (s + (pow(rho*c, c)/ (math.factorial(c)*(1-rho))))
    l_est = pow(rho, c+1) * pow(c,c) * P0/ (math.factorial(c)* pow(1-rho,2)) + rho * c
    return l_est
