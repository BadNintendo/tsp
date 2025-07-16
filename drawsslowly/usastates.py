import time

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.colors as mcolors


# Draw cities and connecting lines
def draw_cities(ax, sorted_path, zoom_level=1, offset_x=0, offset_y=0):
    ax.clear()
    ax.set_facecolor('black')
    ax.set_xticks([])
    ax.set_yticks([])

    colors = list(mcolors.TABLEAU_COLORS.values())
    
    for index in range(1, len(sorted_path)):
        city = sorted_path[index]
        prev_city = sorted_path[index - 1]
        color = colors[index % len(colors)]
        x_coords = [prev_city.get('x', 0) + offset_x, city.get('x', 0) + offset_x]
        y_coords = [prev_city.get('y', 0) + offset_y, city.get('y', 0) + offset_y]
        if 'z' in city and 'z' in prev_city:
            z_coords = [prev_city.get('z', 0), city.get('z', 0)]
            ax.plot(x_coords, y_coords, zs=z_coords, color=color)
        else:
            ax.plot(x_coords, y_coords, color=color)

    if 'z' in sorted_path[0]:
        ax.scatter([city.get('x', 0) + offset_x for city in sorted_path], 
                   [city.get('y', 0) + offset_y for city in sorted_path], 
                   [city.get('z', 0) for city in sorted_path], 
                   c='white', s=5)
    else:
        ax.scatter([city.get('x', 0) + offset_x for city in sorted_path], 
                   [city.get('y', 0) + offset_y for city in sorted_path], 
                   c='white', s=5)

# Animation loop
def animate(frame, sorted_path, ax):
    ax.clear()
    draw_cities(ax, sorted_path[:frame + 1])

def zap(usa_states):
    """Sort and connect cities based on the least x and y values, 
    focusing only on name, x, y for speed. Includes size_x, size_y in output."""
    if not usa_states:
        print("No cities to process. Please check the input data.")
        return []
    
    # Sort cities by x, then y in ascending order
    cities_sorted = sorted(usa_states, key=lambda city: (city['x'], city['y']))
    sorted_path = []
    current_city = cities_sorted[0]
    sorted_path.append(current_city)

    remaining_cities = cities_sorted[1:]  # List of cities left to visit

    while remaining_cities:
        # Find the closest city by comparing x then y
        closest_city = min(remaining_cities, key=lambda city: (city['x'], city['y']))
        
        # Check if the closest city is in the remaining cities before trying to remove it
        if closest_city not in remaining_cities:
            # This shouldn't happen with correct data, skip this iteration
            continue

        index = remaining_cities.index(closest_city)
        sorted_path.append(closest_city)
        del remaining_cities[index]
        current_city = closest_city

        # If we've processed all remaining cities, break out of the loop
        if not remaining_cities:
            break
        
        # Placeholder for potential future code or logic checks
        pass

    # Rebuild the sorted path with all original city attributes
    full_sorted_path = []
    for city in sorted_path:
        # Check for presence of all required keys
        if 'name' in city and 'x' in city and 'y' in city:
            original_city = next((c for c in usa_states if c['name'] == city['name']), None)
            if original_city:
                full_sorted_path.append(original_city)

    # Ensure the first city is also placed at the end to form a loop
    if full_sorted_path:
        full_sorted_path.append(full_sorted_path[0])

    return full_sorted_path
# Example USA States data
usa_states = [
    {'x': -97.0, 'y': 35.0, 'name': 'Oklahoma', 'size_x': 69.0, 'size_y': 47.0},
    {'x': -98.0, 'y': 31.0,  'name': 'Texas', 'size_x': 268.0, 'size_y': 278.0},
    {'x': -88.0, 'y': 41.0,  'name': 'Illinois', 'size_x': 57.0, 'size_y': 55.0},
    {'x': -81.0, 'y': 27.0,  'name': 'Florida', 'size_x': 53.0, 'size_y': 58.0},
    {'x': -119.0, 'y': 36.0,  'name': 'California', 'size_x': 163.0, 'size_y': 156.0},
    {'x': -86.0, 'y': 40.0,  'name': 'Indiana', 'size_x': 36.0, 'size_y': 35.0},
    {'x': -93.0, 'y': 45.0,  'name': 'Minnesota', 'size_x': 87.0, 'size_y': 84.0},
    {'x': -105.0, 'y': 39.0,  'name': 'Colorado', 'size_x': 104.0, 'size_y': 103.0},
    {'x': -81.0, 'y': 38.0,  'name': 'West Virginia', 'size_x': 24.0, 'size_y': 31.0},
    {'x': -77.0, 'y': 39.0,  'name': 'Maryland', 'size_x': 12.0, 'size_y': 32.0},
    {'x': -92.0, 'y': 34.0,  'name': 'Arkansas', 'size_x': 53.0, 'size_y': 55.0},
    {'x': -81.0, 'y': 34.0,  'name': 'South Carolina', 'size_x': 32.0, 'size_y': 33.0},
    {'x': -83.0, 'y': 32.0,  'name': 'Georgia', 'size_x': 59.0, 'size_y': 60.0},
    {'x': -80.0, 'y': 35.0,  'name': 'North Carolina', 'size_x': 54.0, 'size_y': 55.0},
    {'x': -74.0, 'y': 40.0,  'name': 'New Jersey', 'size_x': 9.0, 'size_y': 21.0},
    {'x': -71.0, 'y': 42.0,  'name': 'Massachusetts', 'size_x': 10.0, 'size_y': 27.0},
    {'x': -122.0, 'y': 47.0,  'name': 'Washington', 'size_x': 71.0, 'size_y': 70.0},
    {'x': -70.0, 'y': 45.0,  'name': 'Maine', 'size_x': 35.0, 'size_y': 34.0},
    {'x': -149.0, 'y': 64.0,  'name': 'Alaska', 'size_x': 665.0, 'size_y': 663.0},
    {'x': -157.0, 'y': 21.0,  'name': 'Hawaii', 'size_x': 11.0, 'size_y': 10.0},
    {'x': -86.0, 'y': 39.0,  'name': 'Indiana', 'size_x': 36.0, 'size_y': 35.0},
    {'x': -95.0, 'y': 30.0,  'name': 'Louisiana', 'size_x': 52.0, 'size_y': 50.0},
    {'x': -92.0, 'y': 35.0,  'name': 'Mississippi', 'size_x': 48.0, 'size_y': 50.0},
    {'x': -117.0, 'y': 34.0,  'name': 'Nevada', 'size_x': 110.0, 'size_y': 107.0},
    {'x': -108.0, 'y': 33.0,  'name': 'New Mexico', 'size_x': 121.0, 'size_y': 122.0},
    {'x': -83.0, 'y': 42.0,  'name': 'Ohio', 'size_x': 45.0, 'size_y': 44.0},
    {'x': -96.0, 'y': 44.0,  'name': 'South Dakota', 'size_x': 77.0, 'size_y': 75.0},
    {'x': -85.0, 'y': 35.0,  'name': 'Tennessee', 'size_x': 42.0, 'size_y': 41.0},
    {'x': -120.0, 'y': 44.0,  'name': 'Oregon', 'size_x': 98.0, 'size_y': 96.0},
    {'x': -84.0, 'y': 43.0,  'name': 'Michigan', 'size_x': 97.0, 'size_y': 96.0},
    {'x': -73.0, 'y': 43.0,  'name': 'New York', 'size_x': 55.0, 'size_y': 54.0},
    {'x': -75.0, 'y': 41.0,  'name': 'Pennsylvania', 'size_x': 46.0, 'size_y': 47.0},
    {'x': -77.0, 'y': 38.0,  'name': 'Virginia', 'size_x': 43.0, 'size_y': 44.0},
    {'x': -86.0, 'y': 33.0,  'name': 'Alabama', 'size_x': 52.0, 'size_y': 53.0},
    {'x': -88.0, 'y': 33.0,  'name': 'Mississippi', 'size_x': 48.0, 'size_y': 49.0}
]

# Execute the 'zap' function to sort and connect cities based on their coordinates
# result = zap(usa_states)
# result = zap(cities)
# result = zap(usa_states)
result = zap(usa_states)

if result:
    # Extract key points from the sorted path:
    # - First city as the starting point
    # - Second-to-last city to understand the penultimate stop before loop closure
    # - Last city which should match the first to confirm the path forms a loop
    first_city = result[0]
    second_to_last_city = result[-2]
    last_city = result[-1]

    # Log the results for analysis:
    # - 'result' reflects the sorted and connected path of cities
    # - Length check ensures we're aware of how many stops are included in this path
    print(f"Array Sorted: {result} Length Of: {len(result)}")
    # Detail the starting point of the travel path
    print(f"First starting point: {first_city}")
    # The second-to-last city gives insight into the path's structure before returning to the start
    print(f"Second-to-last starting point: {second_to_last_city}")
    # Confirming the last city is the same as the first ensures the path forms a complete loop
    print(f"Last starting point: {last_city}")
    
    # Example command to measure execution time of this script in PowerShell:
    # - This command uses PowerShell's Measure-Command to time the execution
    # - Adjust the path to match your Python installation and script location
    # powershell -Command "Measure-Command { C:/Users/elite/AppData/Local/Programs/Python/Python313/python.exe TraveledPersonx2.py}"
    
# Note:
    # This test is run against a fixed set of cities for consistency in testing.
    # However, the 'zap' function is designed to handle any amount of cities depeding on
	# memory 999 cities is default, meaning the results can change if the input cities
	# change, although significant changes in outcomes are not expected with minor
	# adjustments to the city list due to the large sample size. This ensures the
	# algorithm's robustness across various city configurations with minimal impact on
	# the overall path structure.
    
	#Graph below (Can remove)
    fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d' if 'z' in usa_states[0] else 'rectilinear')
    ax = fig.add_subplot(111, projection='3d' if 'z' in usa_states[0] else 'rectilinear')

    # Initial draw to set up plot
    draw_cities(ax, result)

    ani = FuncAnimation(fig, animate, frames=len(result), fargs=(result, ax), interval=1, repeat=False)

    # Zoom functionality
    zoom_level = 1
    offset_x = 0
    offset_y = 0

    def on_scroll(event):
        global zoom_level, offset_x, offset_y
        zoom_factor = 1.1 if event.button == 'up' else 0.9
        zoom_level *= zoom_factor
        offset_x = event.xdata - (event.xdata - offset_x) * zoom_factor
        offset_y = event.ydata - (event.ydata - offset_y) * zoom_factor
        draw_cities(ax, result, zoom_level, offset_x, offset_y)
        plt.draw()

    fig.canvas.mpl_connect('scroll_event', on_scroll)

    # Initialize animation state
    animation_frame = [0]

    def on_click(event):
        if animation_frame[0] < len(result) - 1:
            animation_frame[0] += 1
            animate(animation_frame[0], result, ax)
            plt.draw()

    fig.canvas.mpl_connect('button_press_event', on_click)

    plt.show()
