"""
COMP5066 VRP Coursework - Merged Naive + Greedy + 2-Opt + Benchmarking Version

This version includes:
- Naive sequential route builder
- Greedy nearest-neighbour route builder
- Greedy + 2-opt improvement
- Distance calculation
- Generated benchmark test cases
- Timing + memory benchmarking
- Comparison graphs
"""

import time
import tracemalloc
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# Import generated Python benchmark cases
# Make sure these files are in the same folder as this file
# ------------------------------------------------------------

from test_n010 import get_instance as get_n010
from test_n020 import get_instance as get_n020
from test_n030 import get_instance as get_n030
from test_n050 import get_instance as get_n050
from test_n075 import get_instance as get_n075


# ------------------------------------------------------------
# Core helper functions
# ------------------------------------------------------------

def calculate_distance(route, distance_matrix):
    """
    Calculate total distance for one route using the distance matrix.
    Example route: [0, 1, 2, 0]
    """
    total = 0

    for i in range(len(route) - 1):
        start = route[i]
        end = route[i + 1]
        total += distance_matrix[start][end]

    return total


def calculate_total_distance(routes, distance_matrix):
    """
    Calculate total distance across all vehicle routes.
    """
    total = 0

    for route in routes:
        total += calculate_distance(route, distance_matrix)

    return total


# ------------------------------------------------------------
# Naive solution
# ------------------------------------------------------------

def create_routes_naive(customers, demand, capacity):
    """
    Naive/sequential VRP solution.

    Customers are visited in the order they appear in the list.
    A new route is started when adding a customer would exceed capacity.
    """
    routes = []
    current_route = [0]
    current_load = 0

    for customer in customers:
        customer_demand = demand[customer - 1]

        if current_load + customer_demand <= capacity:
            current_route.append(customer)
            current_load += customer_demand
        else:
            current_route.append(0)
            routes.append(current_route)

            current_route = [0, customer]
            current_load = customer_demand

    current_route.append(0)
    routes.append(current_route)

    return routes


# ------------------------------------------------------------
# Greedy solution
# ------------------------------------------------------------

def create_routes_greedy(customers, demand, capacity, distance_matrix):
    """
    Greedy nearest-neighbour VRP solution.

    At each step, the algorithm chooses the nearest unvisited customer.
    If that customer does not fit in the current vehicle, the route is closed
    and a new route starts with that customer.
    """
    routes = []
    current_route = [0]
    current_load = 0
    current_location = 0

    unvisited_customers = customers.copy()

    while unvisited_customers:
        smallest_distance = float("inf")
        nearest_customer = None

        for customer in unvisited_customers:
            distance = distance_matrix[current_location][customer]

            if distance < smallest_distance:
                smallest_distance = distance
                nearest_customer = customer

        customer_demand = demand[nearest_customer - 1]

        if current_load + customer_demand <= capacity:
            current_route.append(nearest_customer)
            current_load += customer_demand
            current_location = nearest_customer
            unvisited_customers.remove(nearest_customer)
        else:
            current_route.append(0)
            routes.append(current_route)

            current_route = [0, nearest_customer]
            current_load = customer_demand
            current_location = nearest_customer
            unvisited_customers.remove(nearest_customer)

    if len(current_route) > 1:
        current_route.append(0)
        routes.append(current_route)

    return routes


# ------------------------------------------------------------
# 2-opt improvement
# ------------------------------------------------------------

def two_opt(route, distance_matrix):
    """
    Improve a single route using 2-opt local search.

    2-opt reverses sections of a route to check whether a shorter route
    can be found.
    """
    improved = True
    best_route = route.copy()
    best_distance = calculate_distance(best_route, distance_matrix)

    while improved:
        improved = False

        for i in range(1, len(best_route) - 2):
            for j in range(i + 1, len(best_route) - 1):
                new_route = (
                    best_route[:i]
                    + best_route[i:j + 1][::-1]
                    + best_route[j + 1:]
                )

                new_distance = calculate_distance(new_route, distance_matrix)

                if new_distance < best_distance:
                    best_route = new_route
                    best_distance = new_distance
                    improved = True

    return best_route, best_distance


def create_routes_greedy_with_2opt(customers, demand, capacity, distance_matrix):
    """
    First creates routes using greedy nearest-neighbour.
    Then improves each route using 2-opt.
    """
    routes = create_routes_greedy(customers, demand, capacity, distance_matrix)

    improved_routes = []
    total_improvement = 0

    for route in routes:
        original_distance = calculate_distance(route, distance_matrix)
        improved_route, new_distance = two_opt(route, distance_matrix)

        improved_routes.append(improved_route)
        total_improvement += original_distance - new_distance

    return improved_routes, total_improvement


# ------------------------------------------------------------
# Benchmark helper functions
# ------------------------------------------------------------

def benchmark_algorithm(algorithm_function, *args):
    """
    Run an algorithm and record:
    - routes
    - execution time
    - current memory
    - peak memory
    """
    tracemalloc.start()
    start_time = time.perf_counter()

    routes = algorithm_function(*args)

    end_time = time.perf_counter()
    current_memory, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    execution_time = end_time - start_time

    return routes, execution_time, current_memory, peak_memory


def benchmark_algorithm_with_extra_return(algorithm_function, *args):
    """
    Run an algorithm that returns extra data.

    Greedy + 2-opt returns:
    routes, improvement_amount
    """
    tracemalloc.start()
    start_time = time.perf_counter()

    result = algorithm_function(*args)

    if isinstance(result, tuple):
        routes = result[0]
        extra = result[1]
    else:
        routes = result
        extra = None

    end_time = time.perf_counter()
    current_memory, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    execution_time = end_time - start_time

    return routes, execution_time, current_memory, peak_memory, extra


# ------------------------------------------------------------
# Convert test cases into the format the algorithms need
# ------------------------------------------------------------

def prepare_case(case):
    """
    Converts different test case formats into one standard format.

    The algorithms need:
    customers = [1, 2, 3, ...]
    demand = [2, 4, 1, ...]
    capacity = number
    distance_matrix = 2D list

    This function handles generated files that may use:
    - "demand" or "demands"
    - "capacity" or "vehicle_capacity"
    - customers as numbers or dictionaries
    """

    raw_customers = case["customers"]

    # If customers are stored as dictionaries, extract id and demand
    if isinstance(raw_customers[0], dict):
        customers = [customer["id"] for customer in raw_customers]
        demand = [customer["demand"] for customer in raw_customers]
    else:
        customers = raw_customers
        demand = case.get("demand", case.get("demands"))

    capacity = case.get("capacity", case.get("vehicle_capacity"))
    distance_matrix = case["distance_matrix"]

    return customers, demand, capacity, distance_matrix


# ------------------------------------------------------------
# Test cases
# ------------------------------------------------------------

bakery_case = {
    "name": "Bakery Case",
    "customers": [1, 2, 3, 4, 5, 6],
    "demand": [2, 3, 1, 4, 2, 3],
    "capacity": 5,
    "distance_matrix": [
        [0, 3, 5, 4, 6, 7, 8],
        [3, 0, 2, 6, 4, 5, 7],
        [5, 2, 0, 3, 5, 6, 4],
        [4, 6, 3, 0, 2, 5, 6],
        [6, 4, 5, 2, 0, 3, 4],
        [7, 5, 6, 5, 3, 0, 2],
        [8, 7, 4, 6, 4, 2, 0],
    ],
}

# Load generated synthetic benchmark cases
test_n010 = get_n010()
test_n020 = get_n020()
test_n030 = get_n030()
test_n050 = get_n050()
test_n075 = get_n075()

# Put all cases into one list
test_cases = [
    bakery_case,
    test_n010,
    test_n020,
    test_n030,
    test_n050,
    test_n075,
]


# ------------------------------------------------------------
# Run benchmarks
# ------------------------------------------------------------

results = []

bakery_greedy_routes = None
bakery_greedy_2opt_routes = None

for case in test_cases:
    print("\n" + "=" * 50)
    print(f"Dataset: {case['name']}")
    print("=" * 50)

    customers, demand, capacity, distance_matrix = prepare_case(case)

    print("Customers:", customers)
    print("Number of customers:", len(customers))
    print("Demand:", demand)
    print("Capacity:", capacity)

    # ---------------- Naive benchmark ----------------

    naive_routes, naive_time, naive_current_mem, naive_peak_mem = benchmark_algorithm(
        create_routes_naive,
        customers,
        demand,
        capacity
    )

    naive_distance = calculate_total_distance(naive_routes, distance_matrix)

    # ---------------- Greedy benchmark ----------------

    greedy_routes, greedy_time, greedy_current_mem, greedy_peak_mem = benchmark_algorithm(
        create_routes_greedy,
        customers,
        demand,
        capacity,
        distance_matrix
    )

    greedy_distance = calculate_total_distance(greedy_routes, distance_matrix)

    # ---------------- Greedy + 2-opt benchmark ----------------

    (
        greedy_2opt_routes,
        greedy_2opt_time,
        greedy_2opt_current_mem,
        greedy_2opt_peak_mem,
        improvement_gain
    ) = benchmark_algorithm_with_extra_return(
        create_routes_greedy_with_2opt,
        customers,
        demand,
        capacity,
        distance_matrix
    )

    greedy_2opt_distance = calculate_total_distance(greedy_2opt_routes, distance_matrix)

    # Save bakery routes in case you want route visualisation later
    if case["name"] == "Bakery Case":
        bakery_greedy_routes = greedy_routes
        bakery_greedy_2opt_routes = greedy_2opt_routes

    # ---------------- Improvement calculations ----------------

    improvement_greedy_vs_naive = 0

    if naive_distance > 0:
        improvement_greedy_vs_naive = (
            (naive_distance - greedy_distance) / naive_distance
        ) * 100

    improvement_2opt_vs_greedy = 0

    if greedy_distance > 0:
        improvement_2opt_vs_greedy = (
            (greedy_distance - greedy_2opt_distance) / greedy_distance
        ) * 100

    # ---------------- Print results ----------------

    print("\n--- Naive Solution ---")
    print("Routes:", naive_routes)
    print("Total distance:", naive_distance)
    print("Vehicles used:", len(naive_routes))
    print(f"Execution time: {naive_time:.6f} seconds")
    print("Peak memory:", naive_peak_mem, "bytes")

    print("\n--- Greedy Solution ---")
    print("Routes:", greedy_routes)
    print("Total distance:", greedy_distance)
    print("Vehicles used:", len(greedy_routes))
    print(f"Execution time: {greedy_time:.6f} seconds")
    print("Peak memory:", greedy_peak_mem, "bytes")
    print(f"Improvement over naive: {improvement_greedy_vs_naive:.2f}%")

    print("\n--- Greedy + 2-Opt Solution ---")
    print("Routes:", greedy_2opt_routes)
    print("Total distance:", greedy_2opt_distance)
    print("Vehicles used:", len(greedy_2opt_routes))
    print(f"Execution time: {greedy_2opt_time:.6f} seconds")
    print("Peak memory:", greedy_2opt_peak_mem, "bytes")
    print(f"Improvement over greedy: {improvement_2opt_vs_greedy:.2f}%")
    print(f"Total 2-opt gain: {improvement_gain:.2f} distance units")

    # Save results for graphs
    results.append({
        "dataset": case["name"],
        "num_customers": len(customers),

        "naive_distance": naive_distance,
        "greedy_distance": greedy_distance,
        "greedy_2opt_distance": greedy_2opt_distance,

        "naive_vehicles_used": len(naive_routes),
        "greedy_vehicles_used": len(greedy_routes),
        "greedy_2opt_vehicles_used": len(greedy_2opt_routes),

        "naive_time": naive_time,
        "greedy_time": greedy_time,
        "greedy_2opt_time": greedy_2opt_time,

        "naive_peak_memory": naive_peak_mem,
        "greedy_peak_memory": greedy_peak_mem,
        "greedy_2opt_peak_memory": greedy_2opt_peak_mem,

        "improvement_greedy_vs_naive": improvement_greedy_vs_naive,
        "improvement_2opt_vs_greedy": improvement_2opt_vs_greedy,
    })


# ------------------------------------------------------------
# Prepare graph data
# ------------------------------------------------------------

datasets = [result["dataset"] for result in results]
num_customers = [result["num_customers"] for result in results]

naive_distances = [result["naive_distance"] for result in results]
greedy_distances = [result["greedy_distance"] for result in results]
greedy_2opt_distances = [result["greedy_2opt_distance"] for result in results]

naive_times = [result["naive_time"] for result in results]
greedy_times = [result["greedy_time"] for result in results]
greedy_2opt_times = [result["greedy_2opt_time"] for result in results]

naive_memory_peak = [result["naive_peak_memory"] for result in results]
greedy_memory_peak = [result["greedy_peak_memory"] for result in results]
greedy_2opt_memory_peak = [result["greedy_2opt_peak_memory"] for result in results]

naive_vehicles_used = [result["naive_vehicles_used"] for result in results]
greedy_vehicles_used = [result["greedy_vehicles_used"] for result in results]
greedy_2opt_vehicles_used = [result["greedy_2opt_vehicles_used"] for result in results]


# ------------------------------------------------------------
# Graph 1: Total Distance vs Number of Customers
# ------------------------------------------------------------

plt.figure(figsize=(10, 5))

plt.plot(num_customers, naive_distances, marker="o", label="Naive")
plt.plot(num_customers, greedy_distances, marker="s", label="Greedy")
plt.plot(num_customers, greedy_2opt_distances, marker="^", label="Greedy + 2-Opt")

plt.title("Total Distance vs Number of Customers")
plt.xlabel("Number of Customers")
plt.ylabel("Total Distance")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# Graph 2: Execution Time vs Number of Customers
# ------------------------------------------------------------

plt.figure(figsize=(10, 5))

plt.plot(num_customers, naive_times, marker="o", label="Naive")
plt.plot(num_customers, greedy_times, marker="s", label="Greedy")
plt.plot(num_customers, greedy_2opt_times, marker="^", label="Greedy + 2-Opt")

plt.title("Execution Time vs Number of Customers")
plt.xlabel("Number of Customers")
plt.ylabel("Execution Time (seconds)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# Graph 3: Peak Memory Usage vs Number of Customers
# ------------------------------------------------------------

plt.figure(figsize=(10, 5))

plt.plot(num_customers, naive_memory_peak, marker="o", label="Naive")
plt.plot(num_customers, greedy_memory_peak, marker="s", label="Greedy")
plt.plot(num_customers, greedy_2opt_memory_peak, marker="^", label="Greedy + 2-Opt")

plt.title("Peak Memory Usage vs Number of Customers")
plt.xlabel("Number of Customers")
plt.ylabel("Peak Memory Usage (bytes)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# Graph 4: Vehicles Used vs Number of Customers
# ------------------------------------------------------------

plt.figure(figsize=(10, 5))

plt.plot(num_customers, naive_vehicles_used, marker="o", label="Naive")
plt.plot(num_customers, greedy_vehicles_used, marker="s", label="Greedy")
plt.plot(num_customers, greedy_2opt_vehicles_used, marker="^", label="Greedy + 2-Opt")

plt.title("Vehicles Used vs Number of Customers")
plt.xlabel("Number of Customers")
plt.ylabel("Vehicles Used")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()