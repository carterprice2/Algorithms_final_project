import sys
from util import read_data, compute_tour, write_solution
import itertools
import time

if len(sys.argv) < 3:
	print('Usage: python solve.py in.txt out.txt')
	sys.exit(1)

#read data into a graph G that specifies the distance between any two nodes from 1 to N
input_filename = sys.argv[1]
output_filename = sys.argv[2]
N, G = read_data(input_filename)
print('Read %d nodes from %s'%(N, input_filename))

#brute force solution: iterate through all possible permutations
#starting and end node can be assumed to be 0 without loss of generality
start_time = time.time()
best_tour = None
min_distance = None
for t in itertools.permutations(range(1,N)):
	current_tour = [0] + list(t) + [0]
	d = compute_tour(G, current_tour)
	if best_tour is None or d < min_distance:
		best_tour = current_tour
		min_distance = d
end_time = time.time()
print('Computed solution in %.2f seconds'%(end_time - start_time))

#write solution to output file
write_solution(output_filename, G, best_tour)
print('Wrote solution to %s (tour length=%d)'%(output_filename, min_distance))
