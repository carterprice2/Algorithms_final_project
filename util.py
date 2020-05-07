import math
import time


def read_data(input_filename):
	f = open(input_filename, 'r')
	x_vals, y_vals = [], []
	for line in f:
		if line[0].isdigit():
			node_id, x_val, y_val = line.split()
			x_vals.append(float(x_val))
			y_vals.append(float(y_val))
	f.close()
	return x_vals, y_vals


def euclid_dist(x1, y1, x2, y2):
	return int(round(math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))))


def build_matrix(x_vals, y_vals):
	node_cnt = len(x_vals)
	distance_matrix = [[float('inf') for _ in range(node_cnt)] for _ in range(node_cnt)]
	for i in range(node_cnt):
		for j in range(node_cnt):
			if i == j:
				continue
			distance_matrix[i][j] = euclid_dist(x_vals[i], y_vals[i], x_vals[j], y_vals[j])
			distance_matrix[j][i] = distance_matrix[i][j]
	return distance_matrix


def get_output_filename(location="Cincinnati", alg="BnB", cut_time="600", seed=None):
	output_filename = "./output/" + '_'.join([location, alg, cut_time])
	if seed:
		output_filename = output_filename + '_' + str(seed)
	return output_filename


def write_trace(output_filename, start_time, upper_bound):
	f = open(output_filename + ".trace", 'a')
	time_elapsed = round(time.time() - start_time, 2)
	f.write(str(time_elapsed) + ", " + str(upper_bound) + '\n')
	f.close()
	return time_elapsed


def write_sol(output_filename, best_cost, best_tour):
	f = open(output_filename + ".sol", 'w')
	f.write(str(best_cost) + '\n')
	f.write(','.join(map(str, best_tour)))
	f.close()
