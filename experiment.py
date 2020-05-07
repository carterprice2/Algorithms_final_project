import os
import time

from util import get_output_filename, read_data, build_matrix, write_sol
from branch_and_bound import bnb_reduce_matrix, bnb_min_edge, bnb_min_two_edges
from nearest_neighbor import nearest_neighbor


locations = ["Cincinnati", "UKansasState", "Atlanta", "Philadelphia", "Boston", "Berlin",\
			 "Champaign", "NYC", "Denver", "SanFrancisco", "UMissouri", "Toronto", "Roanoke"]
optimal_solutions = [277952, 62962, 2003763, 1395981, 893536, 7542,\
					 52643, 1555060, 100431, 810196, 132709, 1176151, 655454]

def test(func):
	alg, cut_time, seed = "Approx" if func==nearest_neighbor else "BnB", 600, None
	best_costs = {}
	approx_ratio = {}

	for location in locations:
		print(location)
		output_filename = get_output_filename(location, alg, str(cut_time), seed)

		start_time = time.time()

		input_filename = "./DATA/" + location + ".tsp"
		x_vals, y_vals = read_data(input_filename)
		distance_matrix = build_matrix(x_vals, y_vals)
		max_edge = max([max([d for d in e if d != float('inf')]) for e in distance_matrix])
		min_edge = min([min([d for d in e if d != 0]) for e in distance_matrix])
		approx_ratio[location] = (1.0 * max_edge / min_edge + 1) / 2

		runtime, best_cost, best_tour = func(distance_matrix, output_filename, start_time, cut_time)
		try:
			write_sol(output_filename, best_cost, best_tour)
		except:
			pass
		best_costs[location] = (runtime, best_cost)

	print(alg)
	print("Time (s)      Sol. Qual.      RelErr")
	for idx, location in enumerate(locations):
		runtime, sol_qual = best_costs[location]
		opt = optimal_solutions[idx]
		try:
			rel_err = round((sol_qual - opt) / opt, 4)
		except:
			pass
		try:
			print("%5.2f        %7d        %.4f" % (runtime, sol_qual, rel_err))
		except:
			print("%5.2f          ---          ---" % runtime)

	for i, loc in enumerate(locations):
		t, q = best_costs[loc]
		a = approx_ratio[loc]
		relErr = 1.0 * (q - optimal_solutions[i]) / optimal_solutions[i]
		if alg=='Approx':
			print('%s&%.2f&%.0f&%.4f&%.2f\\\\ \\hline'%(loc,t,q,relErr,a))
		else:
			print('%s&%.2f&%.0f&%.4f\\\\ \\hline'%(loc,t,q,relErr))

#test(bnb_reduce_matrix)
#test(bnb_min_edge)
test(bnb_min_two_edges)
#test(nearest_neighbor)
