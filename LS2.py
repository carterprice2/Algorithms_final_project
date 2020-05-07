# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 14:38:56 2019

@author: Carter
"""

#simulated Annealing

import numpy as np
import time
from util import write_trace


def swap(pairwise_dist, path,i,j):
    #swaps the position of two local neighbors
    return path[:i] + path[i:j+1][::-1] + path[j+1:]

def compute_tour(pairwise_dist, path):
	cost = 0
	for i in range(len(path)-1):
		cost += pairwise_dist[path[i]][path[i+1]]
	return cost

def schedule(t_start,time_limit):
    #linear schedule
    t = time.time() - t_start
    temp = (time_limit - t)/time_limit
    if temp < 0:
        temp = 0
    return temp

def schedule_exponential(t_start,time_limit):
    #exponential cooling schedule 
    t = time.time() - t_start
    alpha = 0.01
    temp = time_limit*alpha**t
    if temp < 0:
        temp = 0
    return temp

def LS2(pairwise_dist, output_filename, start_time, cut_time, seed):
    """
    simulated annealing
    """
    np.random.seed(seed) 
    N = len(pairwise_dist)
    min_cost = float('inf')
    best_path = None

    while True:
    	path = np.arange(1, N)
    	np.random.shuffle(path)
    	path = [0] + list(path) + [0]
    	updated = True

    	while updated:
    		updated = False
    		for i in range(1,len(path)-2):
    			for j in range(i+1,len(path)-1):
                    #calculte the temperature based on the cooling schedule
    			    T = schedule_exponential(start_time,cut_time)
    			    cost_current = compute_tour(pairwise_dist,path)
    			    if T == 0:
    			        return cost_current, path
    			    new_path = swap(pairwise_dist, path, i, j)
    			    if new_path is not None:
    			        cost_new = compute_tour(pairwise_dist,new_path)
    			        #find the normalized change in cost to get the change in energy
    			        delta_E = (cost_new - cost_current)/cost_current
    			        #if energy change is less than 0 accept the new path
    			        if delta_E < 0:
    			            path = new_path			         
    			        else:
                            #if the energy is positive randomly accept based on T - temperature
    			            a = np.random.rand()    			            
    			            if a < np.exp(-delta_E/T):
    			                path = new_path    			                
    			        updated = True
    			        cost = compute_tour(pairwise_dist, path)
    			        if cost < min_cost:
    			        	min_cost = cost
    			        	best_path = path
    			        	write_trace(output_filename, start_time, min_cost)
    			        if time.time() - start_time > cut_time:
                                    return min_cost, best_path[:-1]
    
    return min_cost, best_path[:-1]
