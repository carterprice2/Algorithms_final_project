"""
Implementation of Nearest Neighbor Algorithm.
"""
import time
import numpy as np
import random

from util import write_trace


def update_distance_matrix(distance_matrix, fr, to):
	# As node A connects to node B, B cannot connect back to A. 
	# A cannot connect to other nodes, and no other nodes can connect to B.
	distance_matrix[to, fr] = np.inf
	distance_matrix[fr, :] = np.inf
	distance_matrix[:, to] = np.inf


def nearest_neighbor(distance_matrix, output_filename, start_time, cut_time):
	num_node = len(distance_matrix)
	# Convert 2-d list to numpy array for column wise operations and get the initial lower bound.
	distance_matrix = np.asarray(distance_matrix, dtype=np.float32)

	start_node = random.randint(0, num_node - 1)  # can be changed to any node
	distance_to_start_node = distance_matrix[:, start_node].copy()
	distance_matrix[:, start_node] = np.inf

	tour = [start_node]
	len_tour = 1
	total_distance = 0
	runtime = None

	while len_tour < num_node:
		if time.time() - start_time > cut_time:
			print("Terminated due to time-out")
			if not runtime:
				runtime = round(time.time() - start_time, 2)
			return runtime, total_distance, tour

		current_node = tour[-1]
		next_node = np.argmin(distance_matrix[current_node, :])
		tour.append(next_node)
		len_tour += 1
		total_distance += distance_matrix[current_node, next_node]
		update_distance_matrix(distance_matrix, current_node, next_node)

	total_distance += distance_to_start_node[tour[-1]]
	runtime = write_trace(output_filename, start_time, total_distance)
	return runtime, total_distance, tour
