// solvedtsp.js

const solveSatisfiabilityAndTSP = async (cities) => {
    const memoizedDistances = {};

    /** Calculates Euclidean distance between two cities with memoization.
     * @param {Object} city1 - First city with properties {name, x, y}.
     * @param {Object} city2 - Second city with properties {name, x, y}.
     * @returns {number} - The calculated distance.
     */
    const calculateDistance = (city1, city2) => {
        const key = `${city1.name}-${city2.name}`;
        if (!memoizedDistances[key]) {
            memoizedDistances[key] = Math.hypot(city1.x - city2.x, city1.y - city2.y);
        }
        return memoizedDistances[key];
    };

    /** Calculates total path distance.
     * @param {Array} path - Array of cities in the path.
     * @returns {number} - The total calculated distance.
     */
    const totalDistance = (path) => {
        return path.reduce((acc, city, i, arr) => {
            const nextCity = arr[(i + 1) % arr.length];
            const dist = calculateDistance(city, nextCity);
            return acc + dist;
        }, 0);
    };

    /** Implements the Nearest-Neighbor approach to approximate TSP.
     * @param {Array} cities - Array of cities.
     * @returns {Object} - Object containing the path and total distance.
     */
    const tspNearestNeighbor = (cities) => {
        const unvisited = new Set(cities.map(city => city.name));
        const path = [cities[0]];
        let currentCity = cities[0];
        while (unvisited.size > 0) {
            unvisited.delete(currentCity.name);
            let closest = null;
            let closestDistance = Infinity;
            for (const city of cities) {
                if (unvisited.has(city.name)) {
                    const dist = calculateDistance(currentCity, city);
                    if (dist < closestDistance) {
                        closestDistance = dist;
                        closest = city;
                    }
                }
            }
            if (!closest) break;
            path.push(closest);
            currentCity = closest;
        }
        const distance = totalDistance(path);
        return { path, distance };
    };

    /** Helper function to calculate the distance between two nodes in a path.
     * @param {Array} path - The path array of cities.
     * @param {number} index1 - First index in path.
     * @param {number} index2 - Second index in path.
     * @returns {number} - Distance between two points in the path.
     */
    const segmentDistance = (path, index1, index2) => {
        // Ensure indexes wrap around correctly if they go out of bounds
        const i1 = (index1 + path.length) % path.length;
        const i2 = (index2 + path.length) % path.length;
        // Retrieve the two cities based on wrapped indexes
        const city1 = path[i1];
        const city2 = path[i2];
        // Calculate and return the memoized distance between the two cities
        return calculateDistance(city1, city2);
    };

    /**
     * Optimizes path with 2-opt swap technique.
     * @param {Array} path - Initial path of cities from TSP solution.
     * @returns {Array} - The optimized path.
     */
    const twoOpt = (path) => {
        let improved = true;
        const improvementThreshold = 1e-6; // Small threshold for improvement
        while (improved) {
            improved = false;
            for (let i = 1; i < path.length - 1; i++) {
                for (let j = i + 1; j < path.length; j++) {
                    // Calculate only the segments affected by the swap
                    const beforeSwapDistance = 
                        segmentDistance(path, i - 1, i) +
                        segmentDistance(path, j, j + 1);
                    // Reverse the segment between i and j
                    const newPath = [
                        ...path.slice(0, i),
                        ...path.slice(i, j + 1).reverse(),
                        ...path.slice(j + 1)
                    ];
                    const afterSwapDistance = 
                        segmentDistance(newPath, i - 1, i) +
                        segmentDistance(newPath, j, j + 1);
                    // If the new path is better, update it
                    if (afterSwapDistance < beforeSwapDistance - improvementThreshold) {
                        path = newPath;
                        improved = true;
                    }
                }
            }
        }
        return path;
    };

    // Solve TSP
    const nearestNeighborResult = tspNearestNeighbor(cities);
    const optimizedPath = twoOpt(nearestNeighborResult.path);
    return {
        path: optimizedPath,
        distance: totalDistance(optimizedPath),
    };
};

module.exports = solveSatisfiabilityAndTSP;
