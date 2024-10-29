// Example cities with coordinates and names
const cities = [
  { name: "A", x: 0, y: 0 },
  { name: "B", x: 3, y: 4 },
  { name: "C", x: 6, y: 1 },
  { name: "D", x: 3, y: 7 }
];

/** Calculates the Euclidean distance between two city objects.
 * @param {Object} city1 - First city with coordinates {x, y}.
 * @param {Object} city2 - Second city with coordinates {x, y}.
 * @returns {number} The Euclidean distance.
 */
const calculateDistance = (city1, city2) =>
  Math.hypot(city1.x - city2.x, city1.y - city2.y);

/** Calculates the total distance for a given path of cities.
 * @param {Array} path - Ordered array of city objects representing the path.
 * @returns {number} Total distance for the path, returning to the start.
 */
const totalDistance = path =>
  path.reduce((acc, city, i, arr) => {
    const nextCity = arr[(i + 1) % arr.length];
    return acc + calculateDistance(city, nextCity);
  }, 0);

/** Recursively generates all permutations of cities.
 * @param {Array} cities - Array of city objects.
 * @returns {Array} An array of all city permutations.
 */
const permute = cities =>
  cities.length === 1
    ? [cities]
    : cities.flatMap((city, i) =>
        permute([...cities.slice(0, i), ...cities.slice(i + 1)]).map(
          path => [city, ...path]
        )
      );

/** Finds the shortest path from all permutations and returns it with its distance.
 * @param {Array} cities - Array of city objects.
 * @returns {Object} An object with shortestPath (city array) and minDistance.
 */
const findShortestPath = cities => {
  const allPaths = permute(cities).filter(path => path[0].name === "A"); // Ensure all paths start from 'A'
  
  // Map all paths to distances and sort by the minimum distance
  const sortedPaths = allPaths
    .map(path => ({ path, distance: totalDistance(path) }))
    .sort((a, b) => a.distance - b.distance);

  const { path: shortestPath, distance: minDistance } = sortedPaths[0];

  return { sortedPaths, shortestPath, minDistance };
};

// Run the algorithm and log each path tested, as well as the shortest path
const result = findShortestPath(cities);

// Console output
console.group("TSP Results with Starting Point 'A'");
result.sortedPaths.forEach(({ path, distance }, idx) => {
  console.log(`Path ${idx + 1}: ${path.map(city => city.name).join(" -> ")} | Distance: ${distance.toFixed(2)}`);
});
console.groupEnd();

console.group("Shortest Path Found");
console.log("%cShortest Path:", "color: green; font-weight: bold;", result.shortestPath.map(city => city.name).join(" -> "));
console.log("%cMinimum Distance:", "color: blue; font-weight: bold;", result.minDistance.toFixed(2));
console.groupEnd();
