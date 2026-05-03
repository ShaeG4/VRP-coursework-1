# VRP-coursework-1
# COMP5066 VRP Coursework

This project implements and benchmarks different heuristic approaches for solving a Vehicle Routing Problem (VRP). The aim is to create feasible delivery routes from a central depot to multiple customers while respecting vehicle capacity constraints and comparing algorithm performance.

## Project Overview

The Vehicle Routing Problem is based on a delivery scenario where a fleet of vehicles must serve a set of customers. Each customer has a demand, and each vehicle has a maximum capacity. The objective is to generate valid routes that start and end at the depot while minimising the total travel distance.

This coursework compares three approaches:

1. **Naive Sequential Algorithm**  
   Customers are visited in the order they appear in the input list. A new route is started whenever adding the next customer would exceed the vehicle capacity.

2. **Greedy Nearest-Neighbour Algorithm**  
   At each step, the nearest unvisited customer is selected, provided the customer can fit within the remaining vehicle capacity.

3. **Greedy + 2-Opt Improvement**  
   The greedy solution is improved using 2-opt local search, which attempts to reduce the route distance by reversing sections of each route.

## Files Included

- `new_DSA_CW.py`  
  Main Python file containing the algorithms, benchmarking code, and graph generation.

- `test_n010.py`  
  Synthetic VRP test instance with 10 customers.

- `test_n020.py`  
  Synthetic VRP test instance with 20 customers.

- `test_n030.py`  
  Synthetic VRP test instance with 30 customers.

- `test_n050.py`  
  Synthetic VRP test instance with 50 customers.

- `test_n075.py`  
  Synthetic VRP test instance with 75 customers.

## Test Cases

The benchmark uses six test cases in total:

| Test case | Number of customers |
|---|---:|
| Bakery Case | 6 |
| `test_n010.py` | 10 |
| `test_n020.py` | 20 |
| `test_n030.py` | 30 |
| `test_n050.py` | 50 |
| `test_n075.py` | 75 |

The synthetic test cases were generated using a fixed random seed so that the benchmark results are reproducible. Customers are placed randomly on a 100 × 100 grid, and customer demands are generated randomly within a fixed demand range. The number of vehicles is calculated automatically based on total demand and vehicle capacity to ensure each instance is feasible.

## Benchmarking

Each algorithm is tested on all six input cases. The program records:

- Total route distance
- Number of vehicles used
- Execution time
- Peak memory usage
- Percentage improvement between algorithms

The results are displayed in the terminal and visualised using Matplotlib graphs.

## Graphs Produced

The program generates the following comparison graphs:

- Total Distance vs Number of Customers
- Execution Time vs Number of Customers
- Peak Memory Usage vs Number of Customers
- Vehicles Used vs Number of Customers

These graphs help show how each algorithm scales as the number of customers increases.

## How to Run

Make sure all Python test case files are in the same folder as the main file.

Install Matplotlib if needed
