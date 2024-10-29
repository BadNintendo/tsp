
// Example cities with coordinates and names
const cities = [
    { name: "A", x: 0, y: 0 },
    { name: "B", x: 3, y: 4 },
    { name: "C", x: 6, y: 1 },
    { name: "D", x: 3, y: 7 },
    { name: "E", x: 0, y: 11 },
    { name: "F", x: 0, y: 4 },
    { name: "G", x: 1, y: 13 },
    { name: "H", x: 13, y: 1 }
];

// Memoization object for storing distances
const memoizedDistances = {};

/** Calculates the Euclidean distance between two city objects and memoizes it.
 * @param {Object} city1 - First city with coordinates {x, y}.
 * @param {Object} city2 - Second city with coordinates {x, y}.
 * @returns {number} The Euclidean distance.
 */
const calculateDistance = (city1, city2) => {
    const key = `${city1.name}-${city2.name}`;
    if (!memoizedDistances[key]) {
        memoizedDistances[key] = Math.hypot(city1.x - city2.x, city1.y - city2.y);
    }
    return memoizedDistances[key];
};

/** Calculates the total distance for a given path of cities with an early exit condition.
 * @param {Array} path - Ordered array of city objects representing the path.
 * @param {number} minDistance - The current known minimum distance to compare with.
 * @returns {number} Total distance for the path, or Infinity if it exceeds minDistance.
 */
const totalDistance = (path, minDistance = Infinity) =>
    path.reduce((acc, city, i, arr) => {
        if (acc >= minDistance) return Infinity; // Early exit
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

/** Finds the shortest paths from all permutations.
 * @param {Array} cities - Array of city objects.
 * @returns {Array} An array of the 5 shortest paths found.
 */
const findShortestPaths = cities => {
    const allPaths = permute(cities).filter(path => path[0].name === "A"); // Ensure all paths start from 'A'
    const pathDistances = [];

    allPaths.forEach(path => {
        const distance = totalDistance(path);
        // Store paths and their distances
        pathDistances.push({ path, distance });
    });

    // Sort paths by distance and return the top 5
    pathDistances.sort((a, b) => a.distance - b.distance);
    return pathDistances.slice(0, 5);
};

// Run the algorithm and get the shortest paths
const result = findShortestPaths(cities);

// Console output
console.group("TSP Results with Starting Point 'A'");
result.forEach(({ path, distance }, index) => {
    console.log(`Path ${index + 1}: ${path.map(city => city.name).join(" -> ")} | Distance: ${distance.toFixed(2)}`);
});
console.groupEnd();
