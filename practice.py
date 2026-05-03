route = [0,3,1,0]

distance_matrix = [ 
    [0,10,20,30],
    [10,0,15,25],
    [20,15,0,35],
    [30,25,35,0],
]

def calculate_distance(route,distance_matrix):
    total = 0 #store the final result
    for i in range (len(route)-1):
        start = route[i] # current node
        end = route[i+1] #next node
        total += distance_matrix[start][end]
    return total

print(calculate_distance(route,distance_matrix))    

route = [0,3,2,0]

distance_matrix = [
    [0,10,20,30],
    [10,0,15,25],
    [20,15,0,35],
    [30,25,35,0],
]


print(calculate_distance(route,distance_matrix))

route = [0,1,3,2,0]

distance_matrix = [
    [0,10,20,30],
    [10,0,15,25],
    [20,15,0,35],
    [30,25,35,0],
]
print(calculate_distance(route,distance_matrix))