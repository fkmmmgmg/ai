import numpy as np

def distance_matrix(cities):
    num_cities = len(cities)
    dist_matrix = np.zeros((num_cities, num_cities))
    for i in range(num_cities):
        for j in range(num_cities):
            dist_matrix[i][j] = np.linalg.norm(cities[i] - cities[j])  # Euclidean distance
    return dist_matrix

def total_distance(path, dist_matrix):
    total_dist = 0
    num_cities = len(path)
    for i in range(num_cities - 1):
        total_dist += dist_matrix[path[i]][path[i+1]]
    total_dist += dist_matrix[path[-1]][path[0]]  # return to starting city
    return total_dist

def random_neighbor(path):
    new_path = path.copy()
    # Randomly swap two cities in the path
    idx1, idx2 = np.random.choice(len(path), 2, replace=False)
    new_path[idx1], new_path[idx2] = new_path[idx2], new_path[idx1]
    return new_path

def hillClimbing(state, evaluate_state, generate_neighbor, max_fail=10000):
    fail = 0
    
    while True:
        neighbor_state = generate_neighbor(state)
        if evaluate_state(neighbor_state) < evaluate_state(state):
            state = neighbor_state
            fail = 0
        else:
            fail += 1
            if fail > max_fail:
                return state, evaluate_state(state)
    
# Define the cities and the initial path
cities = np.array([[0, 0], [1, 2], [3, 1], [5, 3], [6, 0], [8, 2], [9, 1], [7, 5], [4, 4], [2, 6], [1, 8], [0, 7]])
print (cities)
start_path = np.arange(len(cities))  # Initial path: [0, 1, 2, ..., 11]

# Example usage:
best_path, best_distance = hillClimbing(start_path, lambda path: total_distance(path, distance_matrix(cities)), random_neighbor)
print("Best path:", best_path)
print("Total distance:", best_distance)
