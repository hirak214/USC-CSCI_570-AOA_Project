#!/bin/bash

g++ basic.cpp -o basic -std=c++17
for input in datapoints/in*.txt; do
    
    num=$(basename "$input" | sed 's/in\([0-9]*\)\.txt/\1/')
    
    output="datapoints/out${num}.txt"

    echo "Running on $input -> $output"
    ./basic "$input" "$output"
done
