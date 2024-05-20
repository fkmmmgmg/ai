import numpy as np
import matplotlib.pyplot as plt

def distance_matrix(cities):
    num_cities = len(cities)
    dist_matrix = np.zeros((num_cities, num_cities))
    for i in range(num_cities):
        for j in range(num_cities):
            dist_matrix[i][j] = np.linalg.norm(cities[i] - cities[j])  # 歐氏距離
    return dist_matrix

def total_distance(path, dist_matrix):
    total_dist = 0
    num_cities = len(path)
    for i in range(num_cities - 1):
        total_dist += dist_matrix[path[i]][path[i+1]]
    total_dist += dist_matrix[path[-1]][path[0]]  # 返回出發城市
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
    
# 繪製城市
def plot_cities(cities):
    plt.figure(figsize=(8, 6))
    plt.scatter(cities[:, 0], cities[:, 1], color='blue', label='Cities')
    for i, city in enumerate(cities):
        plt.text(city[0], city[1], str(i), fontsize=12, ha='right')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Cities')
    plt.grid(True)
    plt.legend()
    plt.show()

# 繪製最佳路徑
def plot_best_path(cities, path):
    plt.figure(figsize=(8, 6))
    plt.scatter(cities[:, 0], cities[:, 1], color='blue', label='Cities')
    for i, city in enumerate(cities):
        plt.text(city[0], city[1], str(i), fontsize=12, ha='right')
    for i in range(len(path) - 1):
        plt.plot([cities[path[i], 0], cities[path[i + 1], 0]], [cities[path[i], 1], cities[path[i + 1], 1]], 'r--')
    plt.plot([cities[path[-1], 0], cities[path[0], 0]], [cities[path[-1], 1], cities[path[0], 1]], 'r--')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Best Path')
    plt.grid(True)
    plt.legend()
    plt.show()

# Define the cities and the initial path
cities = np.array([[0, 0], [1, 2], [3, 1], [5, 3], [6, 0], [8, 2], [9, 1], [7, 5], [4, 4], [2, 6], [1, 8], [0, 7]])
print (cities)
start_path = np.arange(len(cities))  # Initial path: [0, 1, 2, ..., 11]

# Example usage:
best_path, best_distance = hillClimbing(start_path, lambda path: total_distance(path, distance_matrix(cities)), random_neighbor)
print("Best path:", best_path)
print("Total distance:", best_distance)


plot_cities(cities)
best_path, best_distance = hillClimbing(start_path, lambda path: total_distance(path, distance_matrix(cities)), random_neighbor)
plot_best_path(cities, best_path)