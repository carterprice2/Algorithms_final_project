#!/bin/bash

rm output/*.trace
for instance in DATA/*.tsp
do
	for seed in `seq 10`
	do
		echo $instance
		time python tsp_main.py -inst $instance -alg LS1 -time 5 -seed $seed
	done
done
