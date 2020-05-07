"""
Implementation of Branch-and-Bound Algorithm.
3 kinds of lower bound functions are implemented.
"""
import time
import numpy as np
from heapq import heappush, heappop
from collections import defaultdict

from util import write_trace


def reduce_matrix(distance_matrix):
	new_distance_matrix = distance_matrix.copy()
	lower_bound = 0

	# Extract the min vals for each row, add the sum of min vals to lower_bound,
	# and substract min vals from each row to reduce the matrix.
	row_min = np.min(new_distance_matrix, axis=1)
	row_min[row_min == np.inf] = 0
	lower_bound += sum(row_min)
	new_distance_matrix = new_distance_matrix - row_min.reshape(-1, 1)

	# Extract the min vals for each column, add the sum of min vals to lower_bound,
	# and substract min vals from each column to reduce the matrix.
	col_min = np.min(new_distance_matrix, axis=0)
	col_min[col_min == np.inf] = 0
	lower_bound += sum(col_min)
	new_distance_matrix = new_distance_matrix - col_min

	return new_distance_matrix, lower_bound


def expand_next_node(distance_matrix, fr, to):
	# As node A connects to node B, B cannot connect back to A. 
	# A cannot connect to other nodes, and no other nodes can connect to B.
	new_distance_matrix = distance_matrix.copy()
	new_distance_matrix[to, fr] = np.inf
	new_distance_matrix[fr, :] = np.inf
	new_distance_matrix[:, to] = np.inf
	return reduce_matrix(new_distance_matrix)


def clean_min_heap(min_heap_lower_bound, upper_bound):
	# Examine the min heap and remove branches whose lower bound exceeds the upper bound.
	tmp_heap = []
	while min_heap_lower_bound:
		tmp = heappop(min_heap_lower_bound)
		if tmp[1] < upper_bound:
			heappush(tmp_heap, tmp)
	return tmp_heap


def bnb_reduce_matrix(distance_matrix, output_filename, start_time, cut_time):
	num_node = len(distance_matrix)
	# Convert 2-d list to numpy array for column wise operations and get the initial lower bound.
	distance_matrix = np.asarray(distance_matrix, dtype=np.float32)
	distance_matrix, lower_bound = reduce_matrix(distance_matrix)

	tour = [0]
	len_tour = -len(tour)
	# Deepest branch with the lowest lower bound on the top to expand the subproblem.
	min_heap_lower_bound = [[len_tour, lower_bound, tour, distance_matrix]]

	runtime = None
	upper_bound = float('inf')
	min_tour = None
	while min_heap_lower_bound:
		len_tour, lower_bound, tour, distance_matrix = heappop(min_heap_lower_bound)
		current_node = tour[-1]
		# Iterate over all the next nodes linked to the current node.
		for next_node, distance in enumerate(distance_matrix[current_node]):
			# Return the best solution so far if time-out.
			if time.time() - start_time > cut_time:
				print("Terminated due to time-out")
				if not runtime:
					runtime = round(time.time() - start_time, 2)
				return runtime, upper_bound, min_tour
			# Check if the next node is available. The next node could be unavailable because it is the current node itself or it is previously used.
			if distance != float('inf'):
				# Calculate the new lower bound and update the reduced matrix.
				new_distance_matrix, lower_bound_from_next = expand_next_node(distance_matrix, current_node, next_node)
				new_lower_bound = lower_bound + distance + lower_bound_from_next
				# Do not put back to the min heap or update the current best solution if the lower bound has already exceeded the upper bound.
				if new_lower_bound > upper_bound:  
					continue
				if -len_tour != num_node:  # If not all the nodes are visited in this branch, put back to the min heap to process later.
					heappush(min_heap_lower_bound, [len_tour - 1, new_lower_bound, tour + [next_node], new_distance_matrix])
				else:  # If all the nodes are visited in this branch, update the current best solution, upper bound, and clean up min heap.
					upper_bound = int(new_lower_bound)
					min_tour = tour
					runtime = write_trace(output_filename, start_time, upper_bound)
					min_heap_lower_bound = clean_min_heap(min_heap_lower_bound, upper_bound)
	
	return runtime, upper_bound, min_tour


def bnb_min_edge(distance_matrix, output_filename, start_time, cut_time):
	num_node = len(distance_matrix)
	# Retrieve the minimum edge for each node and sum all of them to be the initial lower bound.
	min_distance_from_node = [min(distances_from_node) for distances_from_node in distance_matrix]
	lower_bound = sum(min_distance_from_node)

	tour = [0]
	len_tour = -len(tour)
	visited = {0}
	# Deepest branch with the lowest lower bound on the top to expand the subproblem.
	min_heap_lower_bound = [[len_tour, lower_bound, tour, visited]]

	runtime = None
	upper_bound = float('inf')
	min_tour = None
	while min_heap_lower_bound:
		len_tour, lower_bound, tour, visited = heappop(min_heap_lower_bound)
		current_node = tour[-1]
		# Iterate over all the next nodes linked to the current node.
		for next_node, distance in enumerate(distance_matrix[current_node]):
			# Return the best solution so far if time-out.
			if time.time() - start_time > cut_time:
				print("Terminated due to time-out")
				if not runtime:
					runtime = round(time.time() - start_time, 2)
				return runtime, upper_bound, min_tour
			if next_node in visited:  # Check if the next node is visited before.
				continue
			# Calculate the new lower bound by replace the minimum edge cost with the true distance.
			new_lower_bound = lower_bound - min_distance_from_node[next_node] + distance
			# Do not put back to the min heap or update the current best solution if the lower bound has already exceeded the upper bound.
			if new_lower_bound > upper_bound:
				continue
			new_len_tour = len_tour - 1
			if -new_len_tour != num_node:  # If not all the nodes are visited in this branch, put back to the min heap to process later.
				new_visited = visited.copy()
				new_visited.add(next_node)
				heappush(min_heap_lower_bound, [new_len_tour, new_lower_bound, tour + [next_node], new_visited])
			else:
			# If all the nodes are visited in this branch, calculate the new lower bound by adding the distance back to node 0.
			# Update the current best solution, upper bound, and clean up min heap.
				new_lower_bound = new_lower_bound - min_distance_from_node[0] + distance_matrix[next_node][0]
				if new_lower_bound < upper_bound:  # Check again due to update of new lower bound.
					upper_bound = int(new_lower_bound)
					min_tour = tour + [next_node]
					runtime = write_trace(output_filename, start_time, upper_bound)
					min_heap_lower_bound = clean_min_heap(min_heap_lower_bound, upper_bound)

	return runtime, upper_bound, min_tour


def bnb_min_two_edges(distance_matrix, output_filename, start_time, cut_time):
	num_node = len(distance_matrix)
	# Retrieve 2 adjacent shortest edges for each node and sum all of them and divided 2 to be the initial lower bound.
	lower_bound = 0
	min_two_distances_from_node = defaultdict(list)
	for node, distances_from_node in enumerate(distance_matrix):
		smallest = second_smallest = float('inf')
		for distance in distances_from_node:
			if distance < smallest:
				smallest, second_smallest = distance, smallest
			elif distance < second_smallest:
				second_smallest = distance
		min_two_distances_from_node[node].append(smallest)
		min_two_distances_from_node[node].append(second_smallest)
		lower_bound += smallest + second_smallest
	lower_bound /= 2

	tour = [0]
	len_tour = -len(tour)
	visited = {0}
	# Deepest branch with the lowest lower bound on the top to expand the subproblem.
	min_heap_lower_bound = [[len_tour, lower_bound, tour, visited]]

	runtime = None
	upper_bound = float('inf')
	min_tour = None
	while min_heap_lower_bound:
		len_tour, lower_bound, tour, visited = heappop(min_heap_lower_bound)
		current_node = tour[-1]
		# Iterate over all the next nodes linked to the current node.
		for next_node, distance in enumerate(distance_matrix[current_node]):
			# Return the best solution so far if time-out.
			if time.time() - start_time > cut_time:
				print("Terminated due to time-out")
				if not runtime:
					runtime = round(time.time() - start_time, 2)
				return runtime, upper_bound, min_tour
			if next_node in visited:  # Check if the next node is visited before.
				continue
			# Calculate the new lower bound by replace the half of 2 adjacent shortest edges with the true distance.
			new_lower_bound = lower_bound - 0.5 * min_two_distances_from_node[current_node][1] - 0.5 * min_two_distances_from_node[next_node][0] + distance
			# Do not put back to the min heap or update the current best solution if the lower bound has already exceeded the upper bound.
			if new_lower_bound > upper_bound:
				continue
			new_len_tour = len_tour - 1
			if -new_len_tour != num_node:  # If not all the nodes are visited in this branch, put back to the min heap to process later.
				new_visited = visited.copy()
				new_visited.add(next_node)
				heappush(min_heap_lower_bound, [new_len_tour, new_lower_bound, tour + [next_node], new_visited])
			else:
			# If all the nodes are visited in this branch, calculate the new lower bound by adding the distance back to node 0.
			# Update the current best solution, upper bound, and clean up min heap.
				new_lower_bound = new_lower_bound - 0.5 * min_two_distances_from_node[next_node][1] - 0.5 * min_two_distances_from_node[0][0] + distance_matrix[next_node][0]
				if new_lower_bound < upper_bound:
					upper_bound = int(new_lower_bound)
					min_tour = tour + [next_node]
					runtime = write_trace(output_filename, start_time, upper_bound)
					min_heap_lower_bound = clean_min_heap(min_heap_lower_bound, upper_bound)

	return runtime, upper_bound, min_tour
