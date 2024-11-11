import math
import time

def solve_satisfiability_and_tsp(cities):
    memoized_distances = {}

    def calculate_distance(city1, city2):
        key = f"{city1['name']}-{city2['name']}"
        if key not in memoized_distances:
            memoized_distances[key] = math.hypot(city1['x'] - city2['x'], city1['y'] - city2['y'])
        return memoized_distances[key]

    def total_distance(path):
        return sum(
            calculate_distance(path[i], path[(i + 1) % len(path)]) for i in range(len(path))
        )

    def tsp_nearest_neighbor(cities):
        unvisited = set(city['name'] for city in cities)
        path = [cities[0]]
        current_city = cities[0]

        while unvisited:
            unvisited.discard(current_city['name'])
            closest = None
            closest_distance = float('inf')

            for city in cities:
                if city['name'] in unvisited:
                    dist = calculate_distance(current_city, city)
                    if dist < closest_distance:
                        closest_distance = dist
                        closest = city

            if closest is None:
                break

            path.append(closest)
            current_city = closest

        distance = total_distance(path)
        return {'path': path, 'distance': distance}

    def segment_distance(path, index1, index2):
        i1 = (index1 + len(path)) % len(path)
        i2 = (index2 + len(path)) % len(path)
        return calculate_distance(path[i1], path[i2])

    def two_opt(path):
        improved = True
        improvement_threshold = 1e-6

        while improved:
            improved = False
            for i in range(1, len(path) - 1):
                for j in range(i + 1, len(path)):
                    before_swap_distance = (
                        segment_distance(path, i - 1, i) +
                        segment_distance(path, j, (j + 1) % len(path))
                    )

                    new_path = path[:i] + path[i:j + 1][::-1] + path[j + 1:]
                    after_swap_distance = (
                        segment_distance(new_path, i - 1, i) +
                        segment_distance(new_path, j, (j + 1) % len(path))
                    )

                    if after_swap_distance < before_swap_distance - improvement_threshold:
                        path = new_path
                        improved = True
        return path

    tsp_result = tsp_nearest_neighbor(cities)
    tsp_result['path'] = two_opt(tsp_result['path'])
    tsp_result['distance'] = total_distance(tsp_result['path'])
    return tsp_result

# Test with a sample list of 10 cities
# Test with a sample list of 10 cities
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

# Measure start time
start_time = time.time()

# Run the TSP solution
result = solve_satisfiability_and_tsp(cities)

# Measure end time
end_time = time.time()

# Calculate the elapsed time
elapsed_time = end_time - start_time

# Print the results and time taken
print("Optimal Path:", [city['name'] for city in result['path']])
print("Total Distance:", result['distance'])
print(f"Elapsed Time: {elapsed_time:.6f} seconds")
