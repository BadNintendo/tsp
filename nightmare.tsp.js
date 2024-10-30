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

// Memoization object for storing distances between cities
const memoizedDistances = {};

/**
 * Calculates the Euclidean distance between two city objects and memoizes it.
 * @param {Object} city1 - First city with coordinates {x, y}.
 * @param {Object} city2 - Second city with coordinates {x, y}.
 * @returns {number} The Euclidean distance between the two cities.
 */
const calculateDistance = (city1, city2) => {
    const key = `${city1.name}-${city2.name}`; // Create a unique key for memoization
    if (!memoizedDistances[key]) {
        // Calculate the distance only if it's not already memoized
        memoizedDistances[key] = Math.hypot(city1.x - city2.x, city1.y - city2.y);
    }
    return memoizedDistances[key];
};

/**
 * Generates all permutations of cities.
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

/**
 * Calculates the total distance for a given path of cities.
 * @param {Array} path - Ordered array of city objects representing the path.
 * @returns {number} Total distance for the path.
 */
const totalDistance = path =>
    path.reduce((acc, city, i, arr) => {
        const nextCity = arr[(i + 1) % arr.length]; // Wrap around to the start
        return acc + calculateDistance(city, nextCity);
    }, 0);

/**
 * Finds the shortest path using dynamic programming and memoization.
 * @param {Array} cities - Array of city objects.
 * @returns {number} The minimum distance to complete the TSP.
 */
const tspDynamicProgramming = (cities) => {
    const n = cities.length;
    const dp = Array(1 << n).fill(null).map(() => Array(n).fill(Infinity)); // DP table
    dp[1][0] = 0; // Starting from city A

    // Loop through all subsets of cities (represented by masks)
    for (let mask = 1; mask < (1 << n); mask += 1) {
        for (let u = 0; u < n; u += 1) {
            // If city 'u' is visited in this mask
            if (mask & (1 << u)) {
                for (let v = 0; v < n; v += 1) {
                    // Skip if 'v' is already visited or same as 'u'
                    if (mask & (1 << v) || u === v) continue; 
                    const newMask = mask | (1 << v); // New mask including city 'v'
                    // Update the DP table with the minimum distance
                    dp[newMask][v] = Math.min(dp[newMask][v], dp[mask][u] + calculateDistance(cities[u], cities[v]));
                }
            }
        }
    }

    // Calculate the minimum cost to return to the starting city
    let minPathCost = Infinity;
    for (let i = 1; i < n; i += 1) {
        minPathCost = Math.min(minPathCost, dp[(1 << n) - 1][i] + calculateDistance(cities[i], cities[0]));
    }
    return minPathCost;
};

// Run the dynamic programming TSP algorithm and output the result
const minDistance = tspDynamicProgramming(cities);
console.log(`Minimum distance for TSP: ${minDistance.toFixed(2)}`);

// Permutations to find paths (if needed)
const allPaths = permute(cities).filter(path => path[0].name === "A");
const pathDistances = allPaths.map(path => ({ path, distance: totalDistance(path) }));
pathDistances.sort((a, b) => a.distance - b.distance);
console.log("Top 5 shortest paths:");
pathDistances.slice(0, 5).forEach(({ path, distance }, index) => {
   console.log(`Path ${index + 1}: ${path.map(city => city.name).join(" -> ")} | Distance: ${distance.toFixed(2)}`);
});
