import sys
import os
import time

from util import get_output_filename, read_data, build_matrix, write_sol
from branch_and_bound import bnb_min_two_edges
from nearest_neighbor import nearest_neighbor
from LS1 import LS1
from LS2 import LS2


if __name__ == "__main__":
	args = sys.argv
	if len(args) < 4:
		sys.exit("Usage: {} -inst <filename> -alg <BnB | Approx | LS1 | LS2> -time <cutoff_in_seconds> -seed <random_seed>".format(args[0]))
	seed = None
	for i in range(len(args)-1):
		if args[i]=='-inst':
			input_filename = args[i+1]
		elif args[i]=='-alg':
			alg = args[i+1]
		elif args[i]=='-time':
			cut_time = args[i+1]
		elif args[i]=='-seed':
			seed = int(args[i+1])

	if alg not in ("BnB", "Approx", "LS1", "LS2"):
		sys.exit("No such algorithm")

	if alg in ("LS1", "LS2") and seed is None:
		sys.exit("Input a random seed for Local Search algorithms")

	if not os.path.isdir("./output"):
		os.makedirs("output")
	location = input_filename.split('/')[-1].split('.')[0]
	output_filename = get_output_filename(location, alg, cut_time, seed)

	cut_time = float(cut_time)
	start_time = time.time()

	x_vals, y_vals = read_data(input_filename)
	distance_matrix = build_matrix(x_vals, y_vals)

	optimal_solutions = {
		'Cincinnati':277952,
		'UKansasState':62962,
		'Atlanta':2003763,
		'Philadelphia':1395981,
		'Boston':893536,
		'Berlin':7542,
		'Champaign':52643,
		'NYC':1555060,
		'Denver':100431,
		'SanFrancisco':810196,
		'UMissouri':132709,
		'Toronto':1176151,
		'Roanoke':655454
	}

	if alg == "BnB":
		runtime, best_cost, best_tour = bnb_min_two_edges(distance_matrix, output_filename, start_time, cut_time)
	elif alg == "Approx":
		runtime, best_cost, best_tour = nearest_neighbor(distance_matrix, output_filename, start_time, cut_time)
	elif alg == "LS1":
		best_cost, best_tour = LS1(distance_matrix, output_filename, start_time, cut_time, seed)
	elif alg == "LS2":
		best_cost, best_tour = LS2(distance_matrix, output_filename, start_time, int(cut_time), int(seed))
	rel_err = round(1.0 * (best_cost - optimal_solutions[location]) / optimal_solutions[location], 4)
	print(location,alg,best_cost,rel_err)

	write_sol(output_filename, best_cost, best_tour)
