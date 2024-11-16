# QPRx2025 found in [Instant Folder](./instant/) [QPRx2025.py](./instant/QPRx2025.py)

## Quantum Processing Relay: Instantly Query a Result!

This project implements various algorithms and methods to handle data efficiently. Below are the key components and their corresponding mathematical calculations.

## Initialization

```python
import time

class QPRx2025:
    """Quantum Processing Relay: Instantly query a result!"""
    def __init__(self, seed=None):
        self.CHARACTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
        self.LCG_PARAMS = {
            'a': 1664525,
            'c': 1013904223,
            'm': 4294967296
        }
        self.seed = None
        self.entropy = None
        if seed is not None:
            self.seed = seed % 1000000
            self.entropy = self.mix_entropy(int(time.time() * 1000))
```

## Mathematical Calculations

### Entropy Mixing

The entropy is mixed using bitwise operations:

mixed_entropy = value XOR (value >> 32) XOR (value >> 16) XOR (value >> 8) XOR value

```python
    def mix_entropy(self, value):
        return value ^ (value >> 32) ^ (value >> 16) ^ (value >> 8) ^ value
```

### Linear Congruential Generator (LCG)

The LCG updates the seed using the parameters \( a \), \( c \), and \( m \):

new_seed = (a * seed + c + entropy) % m

new_entropy = mix_entropy(new_seed + current_time)

```python
    def lcg(self, a=None, c=None, m=None):
        if self.seed is None or self.entropy is None:
            raise ValueError('Seed and entropy must be initialized to use LCG')
        if a is None: a = self.LCG_PARAMS['a']
        if c is None: c = self.LCG_PARAMS['c']
        if m is None: m = self.LCG_PARAMS['m']
        self.seed = (a * self.seed + c + self.entropy) % m
        self.entropy = self.mix_entropy(self.seed + int(time.time() * 1000))
        return self.seed
```

### Mersenne Twister

The Mersenne Twister is initialized and generates random numbers:

```python
    def mersenne_twister(self):
        if self.seed is None:
            raise ValueError('Seed must be initialized to use Mersenne Twister')
        MT = [0] * 624
        index = 0

        def initialize(seed):
            MT[0] = seed
            for i in range(1, 624):
                MT[i] = (0x6c078965 * (MT[i - 1] ^ (MT[i - 1] >> 30)) + i) & 0xffffffff

        def generate_numbers():
            for i in range(624):
                y = (MT[i] & 0x80000000) + (MT[(i + 1) % 624] & 0x7fffffff)
                MT[i] = MT[(i + 397) % 624] ^ (y >> 1)
                if y % 2 != 0:
                    MT[i] ^= 0x9908b0df

        def extract_number():
            nonlocal index
            if index == 0:
                generate_numbers()
            y = MT[index]
            y ^= y >> 11
            y ^= (y << 7) & 0x9d2c5680
            y ^= (y << 15) & 0xefc60000
            y ^= y >> 18
            index = (index + 1) % 624
            return y

        initialize(self.seed)
        return extract_number()
```

### Quantum Polls Relay

Combines LCG and Mersenne Twister values:

quantum_value = ((lcg_value + mt_value) % 1000000) % max_val

```python
    def quantum_polls_relay(self, max_val):
        if not isinstance(max_val, int) or max_val <= 0:
            raise ValueError('Invalid max value for QuantumPollsRelay')
        lcg_value = self.lcg()
        mt_value = self.mersenne_twister()
        return ((lcg_value + mt_value) % 1000000) % max_val
```

## Example Usage

The example demonstrates sorting a list of cities:

```python
    def morton_order(self, city):
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

    def dont_matter(self, cities):
        if not cities:
            print("No cities to process. Please check the input data.")
            return []
        start_sort_time = time.time()
        cities_sorted = sorted(cities, key=self.morton_order)
        sorted_path = [cities_sorted.pop(0)]
        cities_sorted.sort(key=lambda city: (city['x'], city['y']))
        sorted_path.extend(cities_sorted)
        sorted_path.append(sorted_path[0])
        end_sort_time = time.time()
        sort_time = round((end_sort_time - start_sort_time) * 1000, 2)
        print(f"Sort Time (ms): {sort_time}")
        return sorted_path

# Create an instance of QPRx2025
qprx = QPRx2025() # QPRx2025(seed=12345)

# Define the cities data
cities = [
    {'name': 'City0', 'x': 710, 'y': 168},
    {'name': 'City1', 'x': 737, 'y': 137},
    {'name': 'City2', 'x': 761, 'y': 101},
    {'name': 'City3', 'x': 661, 'y': 125},
    {'name': 'City4', 'x': 707, 'y': 185},
    {'name': 'City5', 'x': 612, 'y': 126},
    {'name': 'City6', 'x': 682, 'y': 198},
    {'name': 'City7', 'x': 829, 'y': 137},
]

# Trigger sorting
sorted_cities = qprx.dont_matter(cities)

# Fetch the first, second-to-last starting points, and last
if sorted_cities:
    first_city = sorted_cities[0]
    second_to_last_city = sorted_cities[-2]
    last_city = sorted_cities[-1]

    # Log the results
    print(f"First starting point: {first_city}")
    print(f"Second-to-last starting point: {second_to_last_city}")
    print(f"Last starting point: {last_city}")
```

## License

This project is licensed under the terms of the [File](LICENSE).

© [BadNintendo] 2024. All rights reserved.
