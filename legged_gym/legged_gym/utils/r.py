import numpy as np
import matplotlib.pyplot as plt
import random

# Parameters
x_max, y_max = 100, 100  # Size of the space
start = (10, 10)         # Starting point
goal = (90, 90)          # Goal point
step_size = 2            # Distance moved per step
goal_threshold = 5       # Distance at which the goal is considered reached
max_iterations = 100000    # Maximum number of iterations

# Obstacle definition
obstacles = [
    ((30, 30), 10),  # Circle obstacle with center and radius
    ((60, 60), 15),
]

# Check if a point is inside an obstacle
def is_in_obstacle(point):
    for obstacle in obstacles:
        center, radius = obstacle
        if np.linalg.norm(np.array(point) - np.array(center)) <= radius:
            return True
    return False

# Check if a line from p1 to p2 is clear of obstacles
def is_collision_free(p1, p2):
    num_points = 1  # Number of points between p1 and p2 to check
    points = np.linspace(np.array(p1), np.array(p2), num_points)
    for point in points:
        if is_in_obstacle(point):
            return False
    return True

# Get a random point in the space
def get_random_point():
    while True:
        point = (random.uniform(0, x_max), random.uniform(0, y_max))
        if not is_in_obstacle(point):
            return point

# Find the nearest node in the tree to a given point
def nearest_node(tree, point):
    return min(tree, key=lambda node: np.linalg.norm(np.array(node) - np.array(point)))

# Step from p1 towards p2 by step_size
def step_towards(p1, p2):
    direction = np.array(p2) - np.array(p1)
    distance = np.linalg.norm(direction)
    if distance < step_size:
        return p2
    direction = direction / distance
    new_point = np.array(p1) + direction * step_size
    return tuple(new_point)

# RRT algorithm
def rrt():
    tree = [start]
    parent = {start: None}  # Dictionary to keep track of the tree structure

    while(True):
        # Get a random point
        rand_point = get_random_point()
        
        # Find the nearest node in the tree
        nearest = nearest_node(tree, rand_point)
        
        # Step towards the random point
        new_point = step_towards(nearest, rand_point)
        
        # Check if the path to the new point is collision-free
        if is_collision_free(nearest, new_point):
            tree.append(new_point)
            parent[new_point] = nearest
            
            # Check if we have reached the goal
            if np.linalg.norm(np.array(new_point) - np.array(goal)) <= goal_threshold:
                print("Goal reached!")
                parent[goal] = new_point
                return tree, parent
    return tree, parent

# Plot the results
def plot_rrt(tree, parent):
    fig, ax = plt.subplots()

    # Plot the start and goal points
    ax.plot(*start, 'go', label='Start', markersize=8)
    ax.plot(*goal, 'ro', label='Goal', markersize=8)

    # Plot the obstacles
    for obstacle in obstacles:
        circle = plt.Circle(obstacle[0], obstacle[1], color='gray')
        ax.add_patch(circle)

    # Plot the tree
    for node in tree:
        if parent[node]:
            ax.plot([node[0], parent[node][0]], [node[1], parent[node][1]], 'b-')

    # If goal is reached, backtrack the path
    if goal in parent:
        node = goal
        path = []
        while node is not None:
            path.append(node)
            node = parent[node]
        path = path[::-1]
        path_x, path_y = zip(*path)
        ax.plot(path_x, path_y, 'r-', linewidth=2, label="Path")

    ax.set_xlim(0, x_max)
    ax.set_ylim(0, y_max)
    ax.set_aspect('equal')
    plt.legend()
    plt.show()

# Run the RRT algorithm
tree, parent = rrt()

# Plot the resulting RRT and the found path (if any)
plot_rrt(tree, parent)
