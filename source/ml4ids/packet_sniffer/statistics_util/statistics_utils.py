import math

def update_mean_std(curr_mean, curr_std, num_el, x):
    newM = curr_mean + (x - curr_mean) * 1. / num_el
    newS = math.sqrt(curr_std + ((x - curr_mean) * (x - newM) - curr_std) * 1. / num_el)
    return newM, newS


def update_avg(curr_avg, num_el, x):
    return curr_avg + (x - curr_avg) / num_el
