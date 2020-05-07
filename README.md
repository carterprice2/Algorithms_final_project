# CSE 6140 Final Project

Compute the solution to the Travelling Salesman Problem using 4 different algorithms

1. Branch-and-Bound
2. Nearest Neighbor
3. 2-opt
4. Simulated Annealing

## Usage

Main file to compute the TSP solution for the given problem instance.

```
python tsp_main.py -inst <filename> -alg <BnB | Approx | LS1 | LS2> -time <cutoff_in_seconds> -seed <random_seed>
```

## Scripts

```
#Computes solution for every problem instance with 10 different random seeds using the 2-opt algorithm
./scripts/run_ls1.sh
#Computes solution for every problem instance with 10 different random seeds using the Simulated Annealing algorithm
./scripts/run_ls2.sh
```
