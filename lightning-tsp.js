/**
 * Solves the satisfiability problem with Traveling Salesman Problem algorithms.
 * @param {Array} clauses - Array of logical clauses for satisfiability.
 * @param {Array} cities - Array of city objects with properties {name, x, y}.
 * @returns {Promise<Object>} - Resolves to the best-found path and distance.
 */
const solveSatisfiabilityAndTSP = async (clauses, cities) => {
    const memo = {};
    const memoizedDistances = {};

    /**
     * Recursive DPLL algorithm for checking clause satisfiability.
     * @param {Array} clauses - Logical clauses.
     * @param {Object} assignment - Variable assignment for clauses.
     * @returns {Object|null} - Assignment if satisfiable; null otherwise.
     */
    const dpll = (clauses, assignment = {}) => {
        const key = JSON.stringify(assignment);
        if (memo[key] !== undefined) return memo[key];
        if (clauses.every(clause => clause.some(lit => assignment[Math.abs(lit)] === (lit > 0)))) {
            memo[key] = assignment;
            return assignment;
        }
        if (clauses.some(clause => clause.every(lit => assignment[Math.abs(lit)] === (lit < 0)))) {
            memo[key] = null;
            return null;
        }
        const unitClause = clauses.find(clause => clause.filter(lit => assignment[Math.abs(lit)] === undefined).length === 1);
        if (unitClause) {
            const unitLit = unitClause.find(lit => assignment[Math.abs(lit)] === undefined);
            return dpll(clauses, { ...assignment, [Math.abs(unitLit)]: unitLit > 0 });
        }
        const [variable] = clauses.flat().map(Math.abs).filter(v => assignment[v] === undefined);
        const result = dpll(clauses, { ...assignment, [variable]: true }) || dpll(clauses, { ...assignment, [variable]: false });
        memo[key] = result;
        return result;
    };

    /** Calculates Euclidean distance between two cities, with memoization.
     * @param {Object} city1 - First city with properties {name, x, y}.
     * @param {Object} city2 - Second city with properties {name, x, y}.
     * @returns {Promise<number>} - The calculated distance.
     */
    const calculateDistance = async (city1, city2) => {
        const key = `${city1.name}-${city2.name}`;
        if (!memoizedDistances[key]) memoizedDistances[key] = Math.hypot(city1.x - city2.x, city1.y - city2.y);
        return memoizedDistances[key];
    };

    /** Calculates the total distance of a path.
     * @param {Array} path - Array of cities in the path.
     * @returns {Promise<number>} - The total distance.
     */
    const totalDistance = async (path) => {
        return path.reduce(async (accPromise, city, i, arr) => {
            const acc = await accPromise;
            const nextCity = arr[(i + 1) % arr.length];
            const dist = await calculateDistance(city, nextCity);
            return acc + dist;
        }, Promise.resolve(0));
    };

    /** Solves TSP using a nearest-neighbor approach, starting from the first city.
     * @param {Array} cities - Array of cities.
     * @returns {Promise<Object>} - Contains the path and total distance.
     */
    const tspNearestNeighbor = async (cities) => {
        const unvisited = new Set(cities.map(city => city.name));
        const path = [cities[0]];
        let currentCity = cities[0];
        while (unvisited.size > 0) {
            unvisited.delete(currentCity.name);
            const nextCity = await cities.reduce(async (closestPromise, city) => {
                const closest = await closestPromise;
                if (unvisited.has(city.name)) {
                    const dist = await calculateDistance(currentCity, city);
                    if (!closest || dist < closest.distance) return { city, distance: dist };
                }
                return closest;
            }, Promise.resolve(null));
            if (!nextCity) break;
            path.push(nextCity.city);
            currentCity = nextCity.city;
        }
        const distance = await totalDistance(path);
        return { path, distance };
    };
    const satResult = dpll(clauses);
    const tspResult = await tspNearestNeighbor(cities);
    return {
        satisfiable: !!satResult,
        satAssignment: satResult,
        tspPath: tspResult.path.map(city => city.name),
        tspDistance: tspResult.distance,
    };
};

// Example usage
const clauses = [[1, -2], [2, 3], [-1, -3]];

const cities = [
    {
        "name": "City1",
        "x": 8.69137830994713,
        "y": 46.44025316199729
    },
    {
        "name": "City2",
        "x": 55.30259522197798,
        "y": 90.43313399637462
    },
    {
        "name": "City3",
        "x": 16.578891890873358,
        "y": 21.941089157246285
    },
    {
        "name": "City4",
        "x": 21.889295164734857,
        "y": 90.76024184372531
    },
    {
        "name": "City5",
        "x": 88.19071285347344,
        "y": 48.020594727638596
    },
    {
        "name": "City6",
        "x": 58.43743154322216,
        "y": 29.432209030993416
    },
    {
        "name": "City7",
        "x": 68.0602007070311,
        "y": 56.711846045347045
    },
    {
        "name": "City8",
        "x": 36.701385811059154,
        "y": 71.19188879624163
    },
    {
        "name": "City9",
        "x": 0.01873875607718567,
        "y": 11.009963340473883
    },
    {
        "name": "City10",
        "x": 52.849121177865484,
        "y": 6.996053948555581
    },
    {
        "name": "City11",
        "x": 68.87471857229117,
        "y": 32.79663260556893
    },
    {
        "name": "City12",
        "x": 1.8677580833082352,
        "y": 7.147315398048604
    },
    {
        "name": "City13",
        "x": 1.5993246161458252,
        "y": 88.35835402837688
    },
    {
        "name": "City14",
        "x": 80.95162106158304,
        "y": 29.56421853192648
    },
    {
        "name": "City15",
        "x": 57.1730028284754,
        "y": 50.84701012104242
    },
    {
        "name": "City16",
        "x": 75.62937521934225,
        "y": 40.15212233595569
    },
    {
        "name": "City17",
        "x": 71.07542840053786,
        "y": 48.00426558897224
    },
    {
        "name": "City18",
        "x": 51.48724675403036,
        "y": 15.61233843048253
    },
    {
        "name": "City19",
        "x": 44.1889027670048,
        "y": 4.163829807832364
    },
    {
        "name": "City20",
        "x": 13.301293259873482,
        "y": 77.2725096650387
    },
    {
        "name": "City21",
        "x": 39.15614503807894,
        "y": 8.26083071471071
    },
    {
        "name": "City22",
        "x": 53.536069024598774,
        "y": 25.890730248514913
    },
    {
        "name": "City23",
        "x": 91.16993109630565,
        "y": 64.88857330981139
    },
    {
        "name": "City24",
        "x": 14.00802641367922,
        "y": 61.91699631754239
    },
    {
        "name": "City25",
        "x": 9.437485293356328,
        "y": 89.16591866484033
    },
    {
        "name": "City26",
        "x": 76.17762384044224,
        "y": 3.079928487278072
    },
    {
        "name": "City27",
        "x": 11.309276152034876,
        "y": 88.7217041195026
    },
    {
        "name": "City28",
        "x": 33.75588253715929,
        "y": 45.84382474832407
    },
    {
        "name": "City29",
        "x": 86.78820119746906,
        "y": 35.96192558213864
    },
    {
        "name": "City30",
        "x": 91.50162227511187,
        "y": 23.868459984934276
    },
    {
        "name": "City31",
        "x": 1.0500530517091544,
        "y": 45.286742424156
    },
    {
        "name": "City32",
        "x": 26.27891535397131,
        "y": 12.457873639735961
    },
    {
        "name": "City33",
        "x": 48.59970652086212,
        "y": 55.97853729870883
    },
    {
        "name": "City34",
        "x": 4.669618271949982,
        "y": 2.0054758337797463
    },
    {
        "name": "City35",
        "x": 50.559384362820836,
        "y": 28.540072467252386
    },
    {
        "name": "City36",
        "x": 34.38351827124786,
        "y": 51.75418357394437
    },
    {
        "name": "City37",
        "x": 52.36468736363564,
        "y": 90.72482484358298
    },
    {
        "name": "City38",
        "x": 53.12962412424702,
        "y": 10.471468910106484
    },
    {
        "name": "City39",
        "x": 39.53355513393695,
        "y": 15.237526268184553
    },
    {
        "name": "City40",
        "x": 1.5078813730161622,
        "y": 73.11111241364144
    },
    {
        "name": "City41",
        "x": 19.03814712034586,
        "y": 75.71393597271016
    },
    {
        "name": "City42",
        "x": 88.52309081434208,
        "y": 85.48824757237898
    },
    {
        "name": "City43",
        "x": 16.473186873952184,
        "y": 81.7288772108241
    },
    {
        "name": "City44",
        "x": 20.317397223198164,
        "y": 45.4903074216577
    },
    {
        "name": "City45",
        "x": 15.45326001812577,
        "y": 26.095975246720272
    },
    {
        "name": "City46",
        "x": 92.16901728411901,
        "y": 53.744222254344606
    },
    {
        "name": "City47",
        "x": 65.49405780609573,
        "y": 23.62228717082846
    },
    {
        "name": "City48",
        "x": 64.43265970482214,
        "y": 31.98511346309063
    },
    {
        "name": "City49",
        "x": 57.07000973821559,
        "y": 39.18306416449566
    },
    {
        "name": "City50",
        "x": 80.44488707787619,
        "y": 59.48553318002872
    }
];

solveSatisfiabilityAndTSP(clauses, cities).then(result => {
    console.log("Satisfiability Result:", result.satisfiable ? "Satisfiable" : "Unsatisfiable");
    console.log("SAT Assignment:", result.satAssignment);
    console.log("TSP Path:", result.tspPath);
    console.log("TSP Distance:", result.tspDistance);
});

/* Proven P vs NP can be done but at what cost?!?
Satisfiability Result: Satisfiable
SAT Assignment: {1: false, 2: false, 3: true}
TSP Path: (50) ['City1', 'City31', 'City44', 'City28', 'City36', 'City33', 'City15', 'City49', 'City6', 'City22', 'City35', 'City18', 'City38', 'City10', 'City19', 'City21', 'City39', 'City32', 'City3', 'City45', 'City9', 'City12', 'City34', 'City24', 'City41', 'City20', 'City43', 'City27', 'City25', 'City13', 'City40', 'City4', 'City8', 'City37', 'City2', 'City42', 'City23', 'City46', 'City5', 'City29', 'City14', 'City16', 'City17', 'City7', 'City50', 'City11', 'City48', 'City47', 'City26', 'City30']
TSP Distance: 723.2810647523485
*/
