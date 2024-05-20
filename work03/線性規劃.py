import random

def total_value(x, y, z):
    return 3 * x + 2 * y + 5 * z

def random_neighbor(x, y, z):
    new_x = random.uniform(max(0, x - 0.1), min(10, x + 0.1))
    new_y = random.uniform(max(0, y - 0.1), min(10, y + 0.1))
    new_z = random.uniform(max(0, z - 0.1), min(5.5, z + 0.1))
    return new_x, new_y, new_z

def hill_climbing():
    x = random.uniform(0, 10)
    y = random.uniform(0, 10)
    z = random.uniform(0, 5.5)
    best_value = total_value(x, y, z)

    iterations = 10000
    for _ in range(iterations):
        new_x, new_y, new_z = random_neighbor(x, y, z)
        new_value = total_value(new_x, new_y, new_z)
        if new_value > best_value:
            x, y, z = new_x, new_y, new_z
            best_value = new_value

    return {"x": x, "y": y, "z": z}, best_value

solution, value = hill_climbing()
print("Best solution:", solution)
print("Optimal value:", value)
