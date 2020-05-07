import numpy as np
import time
from util import write_trace

#helper function that performs pairwise exchange
def two_opt(pairwise_dist, path,i,j):
	if pairwise_dist[path[i-1]][path[j]] + pairwise_dist[path[i]][path[j+1]] < \
		pairwise_dist[path[i-1]][path[i]] + pairwise_dist[path[j]][path[j+1]]:
		return path[:i] + path[i:j+1][::-1] + path[j+1:]
	else:
		return None

#helper function that computer
def compute_tour(pairwise_dist, path):
	cost = 0
	for i in range(len(path)-1):
		cost += pairwise_dist[path[i]][path[i+1]]
	return cost

#main function for Local Search 1
def LS1(pairwise_dist, output_filename, start_time, cut_time, seed):
	#initialize the random seed
	np.random.seed(seed)
	N = len(pairwise_dist)
	#keep track of the best tour found so far and its cost
	min_cost = float('inf')
	best_path = None

	#continuously run as long as there is enough time
	while True:
		#randomly choose a starting tour
		path = np.arange(1, N)
		np.random.shuffle(path)
		path = [0] + list(path) + [0]
		updated = True

		while updated:
			updated = False
			#loop through all pairs until a valid pairwise exchange is found
			for i in range(1,len(path)-2):
				for j in range(i+1,len(path)-1):
					new_path = two_opt(pairwise_dist, path, i, j)
					if new_path is not None:
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

