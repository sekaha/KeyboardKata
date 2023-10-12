import math
import random

# Define the objective function to be minimized
def objective_function(x):
    return math.sin(x) + abs(x - 10)


# Simulated Annealing function
def simulated_annealing(
    obj_func, initial_solution, temperature, cooling_rate, num_iterations
):
    current_solution = initial_solution
    current_energy = obj_func(current_solution)

    for _ in range(num_iterations):
        # Generate a neighbor solution
        neighbor_solution = current_solution + random.uniform(-1, 1)
        neighbor_energy = obj_func(neighbor_solution)

        # Calculate the energy difference between the current and neighbor solutions
        energy_difference = neighbor_energy - current_energy

        # If the neighbor solution is better or with a certain probability, accept it
        if energy_difference < 0 or random.random() < math.exp(
            -energy_difference / temperature
        ):
            current_solution = neighbor_solution
            current_energy = neighbor_energy

        # Reduce the temperature
        temperature *= cooling_rate

    return current_solution, current_energy


# Parameters
initial_solution = 2.0
initial_temperature = 1.0
cooling_rate = 0.95
iterations = 1000000

# Run the simulated annealing algorithm
final_solution, min_energy = simulated_annealing(
    objective_function, initial_solution, initial_temperature, cooling_rate, iterations
)

print(f"Minimum solution found: {final_solution}")
print(f"Minimum energy: {min_energy}")
