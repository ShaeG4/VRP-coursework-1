import time
import tracemalloc
import matplotlib.pyplot as plt 

#Stages: 
# - need to create the routes with variables like routes, current_routes, current_load, capacity, customers and demand
# - if the condition fites add the route and update the load keeping in mind of our capicity
# - else add a depot to the current route then save route and start a new route with depot and customer
# - last adding depot to current route and save the route

customers = [1,2,3,4,5,6]
unvisited_customer = customers.copy()
current_location = 0
demand = [2,3,1,4,2,3]
routes = []
current_load = 0
current_route = [0] #starts at the depot 
capacity = 5 

def create_routes():
    
    global customers, routes, current_load, current_route

    for i in range(len(customers)):
        customer = customers[i]
        customer_demand = demand[i]
        if current_load + customer_demand <= capacity: #if condition is true, the customer fits in the current route
            current_route.append(customer)
            current_load = current_load + customer_demand 
        else:
            current_route.append(0) # finsishing the route 
            routes.append(current_route) # saving the route and then add onto it 
            current_route = [0, customer]
            current_load = customer_demand
    current_route.append(0)
    routes.append(current_route)
    return routes

#calculating the distance
def calculate_distance(route,distance_matrix):
    total = 0 
    for i in range(len(route)-1):
        start = route[i]
        end = route[i+1]
        total += distance_matrix[start][end]
    return total

"""
#Test case 
distance_matrix = [
    [0, 1, 2, 3, 4],
    [1, 0, 5, 6, 7],
    [2, 5, 0, 8, 9],
    [3, 6, 8, 0, 10],
    [4, 7, 9, 10, 0]
]
"""


"""
#----Bakery case --------
distance_matrix = [
    [0, 3, 5, 4, 6, 7, 8],
    [3, 0, 2, 6, 4, 5, 7],
    [5, 2, 0, 3, 5, 6, 4],
    [4, 6, 3, 0, 2, 5, 6],
    [6, 4, 5, 2, 0, 3, 4],
    [7, 5, 6, 5, 3, 0, 2],
    [8, 7, 4, 6, 4, 2, 0]
]

"""


#-- Test case 3: ---
customers = [1,2,3,4,5,6,7]
demand = [2,1,3,2,2,1,4]
capacity = 6

distance_matrix = [
    [0,3,4,5,6,7,8,9],
    [3,0,2,4,5,6,7,8],
    [4,2,0,3,4,5,6,7],
    [5,4,3,0,2,4,5,6],
    [6,5,4,2,0,3,4,5],
    [7,6,5,4,3,0,2,4],
    [8,7,6,5,4,2,0,3],
    [9,8,7,6,5,4,3,0]
]


#----Naive solution: -------
routes = []
current_route = [0]
current_load = 0

routes = create_routes()
total_distance = 0
for route in routes:
    dist = calculate_distance(route,distance_matrix)
    total_distance += dist
print("Naive Total Distance:", total_distance)
print("Naive Routes:", routes)


#-----greedy solution. -----
def greedy_solution():
    global current_location, current_load, current_route, routes, unvisited_customer
    
    while unvisited_customer:
        smallest_distance = float("inf")
        nearest_customer = None

        for customer in unvisited_customer:
            distance = distance_matrix[current_location][customer]
            if distance < smallest_distance:
                smallest_distance = distance
                nearest_customer = customer

        customer_demand = demand[nearest_customer - 1]

        if current_load + customer_demand <= capacity:
            current_route.append(nearest_customer)
            current_load += customer_demand
            current_location = nearest_customer
            unvisited_customer.remove(nearest_customer)
        else:
            current_route.append(0)
            routes.append(current_route)
            current_route = [0, nearest_customer]  # Start new route with the customer
            current_location = nearest_customer
            current_load = customer_demand
            unvisited_customer.remove(nearest_customer)  # Remove after adding to new route

    if len(current_route) > 1:
        current_route.append(0)
        routes.append(current_route)

    return routes

routes = []
current_route = [0]
current_load = 0
current_location = 0
unvisited_customer = customers.copy()

#stat records:
tracemalloc.start()
start_time = time.perf_counter()

routes = greedy_solution()

end_time = time.perf_counter()
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()

execution_time = end_time - start_time


print(routes)

total_distance = 0
for route in routes:
    dist = calculate_distance(route, distance_matrix)
    print(route, dist)
    total_distance += dist


print("Greedy Total Distance:", total_distance)
print("Vehicles used:", len(routes))
print(f"Execution time: {execution_time:.6f} seconds")
print(f"Memory used (current): {current} bytes")
print(f"Memory peak: {peak} bytes")