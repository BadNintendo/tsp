## **The visual lightning tsp is added to display origions of x and y with hover options.** 
![image](https://github.com/user-attachments/assets/8cfd21d6-bfc2-4c47-a8df-77df13ed0611)


# **Lightning TSP Module**

**Module Name**: `lightning-tsp.js`  
**Primary Purpose**: Solves both the Satisfiability Problem (SAT) and the Traveling Salesman Problem (TSP) in a single, efficient module using optimized asynchronous JavaScript techniques.

---

## **Module Overview**

The `lightning-tsp.js` module is designed to solve complex computational problems that involve both logical satisfiability and optimal pathfinding. It combines recursive logic with memoization and async handling to efficiently manage SAT checks and TSP path calculations. The code leverages async operations to calculate distances and build paths concurrently, maximizing speed without adding threading.

---

## **Module Components**

1. **DPLL Recursive Algorithm**  
   - **Purpose**: Checks for the satisfiability of logical clauses (SAT).
   - **Operation**: Uses memoization to store and quickly retrieve previous states, optimizing the recursive checks.
   
2. **Memoized Distance Calculation**  
   - **Purpose**: Calculates the Euclidean distance between cities using caching to avoid redundant calculations.
   - **Operation**: Uses city names as keys to store distances and retrieve them quickly.
   
3. **Asynchronous Total Distance Calculation**  
   - **Purpose**: Computes the total path distance for a series of cities asynchronously.
   - **Operation**: Allows non-blocking distance summation, reducing time spent on path calculations.
   
4. **Nearest-Neighbor TSP Solution**  
   - **Purpose**: Implements a nearest-neighbor approach for the TSP.
   - **Operation**: Selects the closest unvisited city to create an efficient path through all cities.

---

## **How to Use**

```javascript
// Import the module
const { solveSatisfiabilityAndTSP } = require('./lightning-tsp.js');

// Define clauses and cities data
const clauses = [[1, -2], [2, 3], [-1, -3]];
const cities = [
    { name: "City1", x: 8.69, y: 46.44 },
    { name: "City2", x: 55.30, y: 90.43 },
    // Add other cities as needed
];

// Run the function and log the result
solveSatisfiabilityAndTSP(clauses, cities).then(result => {
    console.log("Optimal Path:", result.path);
    console.log("Total Distance:", result.distance);
});
```

---

## **Feedback**

- **Efficiency**: The use of async functions and memoization ensures that the TSP calculation is handled smoothly without unnecessary recalculations.
- **Clarity**: The structure of this module makes it accessible and easy to maintain, with each function focused on a specific task.
- **Suggestions**:  
  - Consider adding error handling to manage invalid inputs or edge cases in the SAT logic.
  - If possible, optimize the `nearestNeighbor` function to explore alternative paths for a more optimal TSP solution.

---

## **Anything Else?**

This is everything you need to get started with `lightning-tsp.js`. Give it a try, explore its features, and enjoy solving complex problems at lightning speed!

---
