import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib.animation import FuncAnimation

NUM_PARTICLES = 50
NUM_ITERATIONS = 100
W = 0.5
C1 = 1.0
C2 = 2.0

def random_dots(num_dots, lower_bound=0, upper_bound=100):
    return np.random.randint(lower_bound, upper_bound, size=(num_dots, 2))

def calculate_distance(point1, point2):
    return np.linalg.norm(point1 - point2)

def initialize_particles(num_particles, num_dots):
    particles = [random.sample(range(num_dots), num_dots) for _ in range(num_particles)]
    return particles

def calculate_route_length(dots, route):
    distance = 0
    for i in range(len(route) - 1):
        distance += calculate_distance(dots[route[i]], dots[route[i+1]])
    distance += calculate_distance(dots[route[-1]], dots[route[0]])  # Return to start to form a loop
    return distance

def update_velocity(velocity, current_route, personal_best_route, global_best_route, W, C1, C2):
    new_velocity = W * np.array(velocity)
    
    cognitive_component = C1 * random.random() * np.array([personal_best_route[i] - current_route[i] for i in range(len(current_route))])
    social_component = C2 * random.random() * np.array([global_best_route[i] - current_route[i] for i in range(len(current_route))])
    
    new_velocity = new_velocity + cognitive_component + social_component
    return new_velocity

def update_position(current_route, velocity):
    new_route = current_route[:]
    num_swaps = int(np.abs(velocity.sum()) % len(current_route))  # Number of swaps based on velocity
    for _ in range(num_swaps):
        i, j = random.sample(range(len(current_route)), 2)  # Select two random indices to swap
        new_route[i], new_route[j] = new_route[j], new_route[i]
    return new_route

def pso_optimization(dots, num_particles, num_iterations, W, C1, C2):
    num_dots = len(dots)
    particles = initialize_particles(num_particles, num_dots)
    
    velocities = [np.zeros(num_dots) for _ in range(num_particles)]
    
    personal_best_routes = particles.copy()
    personal_best_lengths = [calculate_route_length(dots, route) for route in personal_best_routes]
    
    global_best_route = personal_best_routes[np.argmin(personal_best_lengths)]
    global_best_length = min(personal_best_lengths)
    
    for iteration in range(num_iterations):
        for i in range(num_particles):
            current_length = calculate_route_length(dots, particles[i])
            
            if current_length < personal_best_lengths[i]:
                personal_best_routes[i] = particles[i]
                personal_best_lengths[i] = current_length
            
            if current_length < global_best_length:
                global_best_route = particles[i]
                global_best_length = current_length
                
            velocities[i] = update_velocity(velocities[i], particles[i], personal_best_routes[i], global_best_route, W, C1, C2)
            particles[i] = update_position(particles[i], velocities[i])
    
    return global_best_route, global_best_length

def plot_all_possible_routes(dots):
    x, y = dots[:, 0], dots[:, 1]
    plt.scatter(x, y, color='blue')
    for i in range(len(dots)):
        for j in range(i + 1, len(dots)):
            plt.plot([dots[i][0], dots[j][0]], [dots[i][1], dots[j][1]], color='gray', linestyle='--', alpha=0.5)
            
    plt.title("All Possible Routes")
    plt.show()

def plot_frequent_routes(dots, particles):
    x, y = dots[:, 0], dots[:, 1]
    plt.scatter(x, y, color='blue')
    
    route_counts = np.zeros((len(dots), len(dots)))
    for route in particles:
        for i in range(len(route) - 1):
            route_counts[route[i], route[i + 1]] += 1
            route_counts[route[i + 1], route[i]] += 1

    max_frequency = np.max(route_counts)
    threshold = 0.1 * max_frequency 
    
    for i in range(len(dots)):
        for j in range(i + 1, len(dots)):
            if route_counts[i, j] > threshold:
                linewidth = (route_counts[i, j] / max_frequency) * 5 
                plt.plot([dots[i][0], dots[j][0]], [dots[i][1], dots[j][1]], color='purple', linewidth=linewidth)
    plt.title("Frequently Used Routes (PSO)")
    plt.show()

def plot_path(dots, path):
    x, y = dots[:, 0], dots[:, 1]
    plt.scatter(x, y, color='blue')
    for i in range(len(path) - 1):
        plt.plot([dots[path[i]][0], dots[path[i + 1]][0]], [dots[path[i + 1]][1], dots[path[i + 1]][1]], color='red')
    plt.plot([dots[path[-1]][0], dots[path[0]][0]], [dots[path[-1]][1], dots[path[0]][1]], color='red', linestyle='--')
    plt.title("Particle Swarm Optimization Path")
    plt.show()

num_dots = 10
dots = random_dots(num_dots)
best_route, best_length = pso_optimization(dots, NUM_PARTICLES, NUM_ITERATIONS, W, C1, C2)
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
    plt.title("Particle Swarm Optimization - Route Animation")
    plt.show()

plot_all_possible_routes(dots)

animate_path(dots, best_route)
