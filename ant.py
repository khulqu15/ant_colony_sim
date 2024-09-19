import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib.animation import FuncAnimation

NUM_ANTS = 50
NUM_ITERATIONS = 100
ALPHA = 1.0
BETHA = 2.0
EVAPORATION_RATE = 0.5
Q = 100.0

def random_dots(num_dots, lower_bound=0, upper_bound=100):
    return np.random.randint(lower_bound, upper_bound, size=(num_dots, 2))

def calculate_distance(point1, point2):
    return np.linalg.norm(point1 - point2)

def initialize_pheromone(num_dots):
    return np.ones((num_dots, num_dots))

def transition_probabilites(pheromone, distance, current_dot, visited, alpha, betha):
    prob_numerator = np.power(pheromone[current_dot], alpha) * np.power(1 / (distance[current_dot] + 1e-10), betha)
    prob_numerator[visited] = 0
    prob_denominator = np.sum(prob_numerator)
    if prob_denominator == 0:
        return np.zeros(len(prob_numerator))
    return prob_numerator / prob_denominator

def update_pheromone(pheromone, all_routes, distance, evaporation_rate, Q):
    pheromone *= (1 - evaporation_rate)
    for route in all_routes:
        route_length = sum(distance[route[i], route[i + 1]] for i in range(len(route) - 1))
        pheromone_contribution = Q / route_length
        for i in range(len(route) - 1):
            pheromone[route[i], route[i + 1]] += pheromone_contribution
            pheromone[route[i + 1], route[i]] += pheromone_contribution
            
            
def ant_colony_optimization(dots, num_ants, num_iterations, alpha, beta, evaporation_rate, Q):
    num_dots = len(dots)
    distances = np.array([[calculate_distance(dots[i], dots[j]) for j in range(num_dots)] for i in range(num_dots)])
    pheromone = initialize_pheromone(num_dots)

    best_route = None
    best_route_length = float('inf')
    route_frequency = np.zeros((num_dots, num_dots))

    for iteration in range(num_iterations):
        all_routes = []
        for ant in range(num_ants):
            visited = [False] * num_dots
            current_dot = random.randint(0, num_dots - 1)
            route = [current_dot]
            visited[current_dot] = True

            for step in range(num_dots - 1):
                probabilities = transition_probabilites(pheromone, distances, current_dot, visited, alpha, beta)
                next_dot = np.random.choice(np.arange(num_dots), p=probabilities)
                route.append(next_dot)
                visited[next_dot] = True
                current_dot = next_dot

            route.append(route[0])  # Return to start
            all_routes.append(route)

            route_length = sum(distances[route[i], route[i + 1]] for i in range(len(route) - 1))
            if route_length < best_route_length:
                best_route_length = route_length
                best_route = route
                
            for i in range(len(route) - 1):
                route_frequency[route[i], route[i + 1]] += 1
                route_frequency[route[i + 1], route[i]] += 1

        update_pheromone(pheromone, all_routes, distances, evaporation_rate, Q)

    return best_route, best_route_length, route_frequency

def plot_all_possible_routes(dots):
    x, y = dots[:, 0], dots[:, 1]
    plt.scatter(x, y, color='blue')
    for i in range(len(dots)):
        for j in range(i + 1, len(dots)):
            plt.plot([dots[i][0], dots[j][0]], [dots[i][1], dots[j][1]], color='gray', linestyle='--', alpha=0.5)
            
    plt.title("All Possible Routes")
    plt.show()


def plot_frequent_routes(dots, route_frequency):
    max_frequency = np.max(route_frequency)
    threshold = 0.1 * max_frequency 
    x, y = dots[:, 0], dots[:, 1]
    plt.scatter(x, y, color='blue')

    for i in range(len(dots)):
        for j in range(i + 1, len(dots)):
            if route_frequency[i, j] > threshold:
                linewidth = (route_frequency[i, j] / max_frequency) * 5  # Line width proportional to frequency
                plt.plot([dots[i][0], dots[j][0]], [dots[i][1], dots[j][1]], color='purple', linewidth=linewidth)
    plt.title("Frequently Used Routes")
    plt.show()

def plot_path(dots, path):
    x, y = dots[:, 0], dots[:, 1]
    plt.scatter(x, y, color='blue')
    for i in range(len(path) - 1):
        plt.plot([dots[path[i]][0], dots[path[i + 1]][0]], [dots[path[i]][1], dots[path[i + 1]][1]], color='red')
    plt.plot([dots[path[-1]][0], dots[path[0]][0]], [dots[path[-1]][1], dots[path[0]][1]], color='red', linestyle='--')
    plt.title("Ant Colony Optimization Path")
    plt.show()
    
    
num_dots = 10
dots = random_dots(num_dots)
best_route, best_length, route_frequency = ant_colony_optimization(dots, NUM_ANTS, NUM_ITERATIONS, ALPHA, BETHA, EVAPORATION_RATE, Q)
print(f"Best Route: {best_route}, Best Length: {best_length}")

def animate_path(dots, path):
    fig, ax = plt.subplots()
    x, y = dots[:, 0], dots[:, 1]
    scat = ax.scatter(x, y, color='blue')

    line, = ax.plot([], [], color='red', linewidth=2)

    def init():
        line.set_data([], [])
        return line,

    def update(frame):
        current_path_x = [dots[path[i]][0] for i in range(frame + 1)]
        current_path_y = [dots[path[i]][1] for i in range(frame + 1)]
        line.set_data(current_path_x, current_path_y)
        return line,

    ani = FuncAnimation(fig, update, frames=len(path), init_func=init, blit=True, repeat=False)
    plt.title("Ant Colony Optimization - Route Animation")
    plt.show()

plot_all_possible_routes(dots)
plot_frequent_routes(dots, route_frequency)

animate_path(dots, best_route)
plot_path(dots, best_route)