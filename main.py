import numpy as np

town = [["O" for _ in range(10)] for _ in range(10)]

def print_town(town):
    for row in town:
        print(" ".join(row))

assets = [["B", 2, 2], ["A", 3, 3], ["H", 5, 4], ["F", 1, 1]]  
# Lists of assets in categories: Building Type, Damage Threshold, Repair Time

town[4][2] = "B"  # Barn
town[0][8] = "A"  # Apartment
town[7][1] = "H"  # Hospital
town[5][5] = "F"  # Field
town[2][3] = "B"  # Another Barn
town[9][0] = "A"  # Another Apartment
town[3][7] = "H"  # Another Hospital
town[6][6] = "F"  # Another Field

print_town(town)

def generate_lightning_strikes(town_size):
    # Poisson distribution for number of strikes per day
    strikes = []
    num_strikes = np.random.poisson(10, 5) # Average 10 strikes per day for 5 days
    for n in num_strikes:
        n = int(n)
        print(f"Number of lightning strikes: {n}")
        # uniform distribution for x and y coordinates (assume town is level)
        x = np.random.uniform(0, town_size, n)
        y = np.random.uniform(0, town_size, n)
        strikes.append([x, y])
    return strikes

strikes = generate_lightning_strikes(10)
for day, strike in enumerate(strikes):
    print(strike)
    new_town = town.copy()
    for i in range(len(strike[0])):
        new_town[int(strike[1][i])][int(strike[0][i])] = "X"  # Mark lightning strikes
        print("\nTown after lightning strike", i + 1, "on day", day + 1,":")
        print_town(new_town)