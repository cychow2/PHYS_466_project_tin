import numpy as np


def autocorr_coeff(data, t):
    n = len(data)
    mean = np.mean(data)
    r = 0
    for i in range(n-t):
        r += (data[i] - mean)*(data[i+t] - mean)
    r *= (n-1)/(n-t-1) * 1/(np.sum((data - mean)**2)) if np.sum((data - mean)**2) > 1e-5 else 0
    return r


def autocorr_time(data):
    kappa = 1
    t = 1
    r = autocorr_coeff(data, t)
    while r > 0:
        kappa += 2 * r
        t += 1
        r = autocorr_coeff(data, t)
        assert t < len(data)-1
    return kappa


def stand_error(data):
    kappa = autocorr_time(data)
    n = len(data)
    return np.std(data)/np.sqrt(n/kappa)