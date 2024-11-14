import math
import time

def calculate_distance(city1, city2):
    return math.hypot(city1['x'] - city2['x'], city1['y'] - city2['y'])

def total_distance(path):
    return sum(calculate_distance(path[i], path[(i + 1) % len(path)]) for i in range(len(path)))

def morton_order(city):
    def interleave_bits(x, y):
        def spread_bits(v):
            v = (v | (v << 8)) & 0x00FF00FF
            v = (v | (v << 4)) & 0x0F0F0F0F
            v = (v | (v << 2)) & 0x33333333
            v = (v | (v << 1)) & 0x55555555
            return v
        return spread_bits(x) | (spread_bits(y) << 1)
    x = int(city['x'] * 10000)
    y = int(city['y'] * 10000)
    return interleave_bits(x, y)

def solve_tsp(cities):
    """Find and optimize a path using Morton order, nearest neighbor heuristic, and 2-opt algorithm."""
    
    # Sort cities based on Morton order
    cities_sorted = sorted(cities, key=morton_order)

    # Measure time for initial solution using nearest neighbor heuristic
    start_initial = time.time()
    
    # Nearest neighbor heuristic and path initialization
    unvisited = set(city['name'] for city in cities_sorted)
    path = [cities_sorted[0]]
    current_city = cities_sorted[0]

    while unvisited:
        unvisited.discard(current_city['name'])
        closest = min((city for city in cities_sorted if city['name'] in unvisited), 
                      key=lambda city: calculate_distance(current_city, city), 
                      default=None)
        if closest is None:
            break

        path.append(closest)
        current_city = closest

    # Ensure path returns to start to form a complete tour
    path.append(path[0])
    initial_distance = total_distance(path)
    end_initial = time.time()
    initial_time = round((end_initial - start_initial) * 1000, 2)  # Convert to milliseconds and round to 2 decimal places

    # Measure time for optimizing the path using 2-opt
    start_optimized = time.time()
    
    # 2-opt optimization
    improvement_threshold = 1e-6
    improved = True

    while improved:
        improved = False
        for i in range(1, len(path) - 2):
            for j in range(i + 1, len(path) - 1):
                if calculate_distance(path[i - 1], path[i]) + calculate_distance(path[j], path[(j + 1) % len(path)]) > \
                   calculate_distance(path[i - 1], path[j]) + calculate_distance(path[i], path[(j + 1) % len(path)]):
                    path[i:j + 1] = reversed(path[i:j + 1])
                    improved = True

    optimized_distance = total_distance(path)
    end_optimized = time.time()
    optimized_time = round((end_optimized - start_optimized) * 1000, 2)  # Convert to milliseconds and round to 2 decimal places

    # Validation checks
    unique_cities = {city['name'] for city in path}
    all_cities = {city['name'] for city in cities}
    is_valid_path = unique_cities == all_cities and path[0] == path[-1]

    optimized_array = [{'name': city['name'], 'x': city['x'], 'y': city['y']} for city in path]

    if is_valid_path:
        print("Path validation successful: Each city is visited once, and path returns to origin.")
    else:
        print("Path validation failed: Path does not include all cities or does not return to the origin.")

    return {
        'initial_path': [city['name'] for city in path],
        'optimized_path': [city['name'] for city in path],
        'initial_distance': initial_distance,
        'optimized_distance': optimized_distance,
        'initial_time': initial_time,
        'optimized_time': optimized_time,
        'optimized_array': optimized_array
    }

cities = [
    {'name': 'City0', 'x': 0, 'y': 0},
    {'name': 'City1', 'x': 10, 'y': 10},
    {'name': 'City2', 'x': 20, 'y': 20},
    {'name': 'City3', 'x': 30, 'y': 5},
    {'name': 'City4', 'x': 40, 'y': 15},
    {'name': 'City5', 'x': 50, 'y': 0},
    {'name': 'City6', 'x': 60, 'y': 10},
    {'name': 'City7', 'x': 70, 'y': 20},
    {'name': 'City8', 'x': 80, 'y': 5},
    {'name': 'City9', 'x': 90, 'y': 15},
    {'name': 'City10', 'x': 100, 'y': 0},
    {'name': 'City11', 'x': 110, 'y': 10},
    {'name': 'City12', 'x': 120, 'y': 20},
    {'name': 'City13', 'x': 130, 'y': 5},
    {'name': 'City14', 'x': 140, 'y': 15},
    {'name': 'City15', 'x': 150, 'y': 0},
    {'name': 'City16', 'x': 160, 'y': 10},
    {'name': 'City17', 'x': 170, 'y': 20},
    {'name': 'City18', 'x': 180, 'y': 5},
    {'name': 'City19', 'x': 190, 'y': 15},
    {'name': 'City20', 'x': 200, 'y': 0},
    {'name': 'City21', 'x': 210, 'y': 10},
    {'name': 'City22', 'x': 220, 'y': 20},
    {'name': 'City23', 'x': 230, 'y': 5},
    {'name': 'City24', 'x': 240, 'y': 15},
    {'name': 'City25', 'x': 250, 'y': 0},
    {'name': 'City26', 'x': 260, 'y': 10},
    {'name': 'City27', 'x': 270, 'y': 20},
    {'name': 'City28', 'x': 280, 'y': 5},
    {'name': 'City29', 'x': 290, 'y': 15},
    {'name': 'City30', 'x': 300, 'y': 0},
    {'name': 'City31', 'x': 310, 'y': 10},
    {'name': 'City32', 'x': 320, 'y': 20},
    {'name': 'City33', 'x': 330, 'y': 5},
    {'name': 'City34', 'x': 340, 'y': 15},
    {'name': 'City35', 'x': 350, 'y': 0},
    {'name': 'City36', 'x': 360, 'y': 10},
    {'name': 'City37', 'x': 370, 'y': 20},
    {'name': 'City38', 'x': 380, 'y': 5},
    {'name': 'City39', 'x': 390, 'y': 15},
    {'name': 'City40', 'x': 400, 'y': 0},
    {'name': 'City41', 'x': 410, 'y': 10},
    {'name': 'City42', 'x': 420, 'y': 20},
    {'name': 'City43', 'x': 430, 'y': 5},
    {'name': 'City44', 'x': 440, 'y': 15},
    {'name': 'City45', 'x': 450, 'y': 0},
    {'name': 'City46', 'x': 460, 'y': 10},
    {'name': 'City47', 'x': 470, 'y': 20},
    {'name': 'City48', 'x': 480, 'y': 5},
    {'name': 'City49', 'x': 490, 'y': 15}
]

# Run the function and print results
result = solve_tsp(cities)
print("Optimized Path:", result['optimized_path'])
print("Optimized Distance:", result['optimized_distance'])
print("Optimization Time (ms):", result['optimized_time'])
print("Optimized Array:", result['optimized_array'])
