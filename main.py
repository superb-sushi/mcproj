import numpy as np

building_types = {
    "B": "Barn",
    "A": "Apartment",
    "H": "Hospital",
    "F": "Field"
}

class Town:
    def __init__(self, size):
        self.size = size
        self.grid = [["O" for _ in range(size)] for _ in range(size)]
        for r in range(len(self.grid)):
            for c in range(len(self.grid[r])):
                self.grid[r][c] = Asset(row=r, col=c, is_empty=True)

    def print_town(self):
        temp = [["O" for _ in range(self.size)] for _ in range(self.size)]
        for r in range(len(self.grid)):
            for c in range(len(self.grid[r])):
                temp[r][c] = self.grid[r][c].display()
        for asset in assets:
            temp[asset.row][asset.col] = asset.display()
        for row in temp:
            print(" ".join(row))

    def is_destroyed(self):
        for asset in assets:
            if not asset.is_destroyed():
                return False
        return True

class Asset:
    def __init__(self, row=0, col=0, asset_type=0, damage_threshold=0, repair_time=0, is_empty=False):
        self.row = row
        self.col = col
        self.asset_type = asset_type
        self.damage_threshold = damage_threshold
        self.repair_time = repair_time
        self.damage_taken = 0
        self.repair_counter = 0
        self.is_empty = is_empty
    
    def take_damage(self, damage):
        if self.is_destroyed():
            self.repair_counter = 0
        else:
            self.damage_taken += damage
            print(f"  {building_types[self.asset_type]} at ({self.row}, {self.col}) took {damage} damage (HP: {self.damage_threshold - self.damage_taken}/{self.damage_threshold}).")
            if self.damage_taken >= self.damage_threshold:
                self.damage_taken = self.damage_threshold
                print(f"{building_types[self.asset_type]} at ({self.row}, {self.col}) has been destroyed.")
    
    def repair(self):
        self.repair_counter += 1
        if self.repair_counter >= self.repair_time:
            self.repair_counter = 0
            self.damage_taken = 0
            print(f"  {building_types[self.asset_type]} at ({self.row}, {self.col}) has been repaired.")
    
    def is_destroyed(self):
        return self.damage_taken >= self.damage_threshold

    def display(self):
        return "O" if self.is_empty else (self.asset_type if not self.is_destroyed() else "X")

template_assets = {"B":[2, 2], "A":[3, 3], "H":[5, 4], "F":[1, 1]} # Assets -> Building Type: [Damage Threshold, Repair Time]

assets = []
assets.append(Asset(4, 2, "B", template_assets["B"][0], template_assets["B"][1]))  # Barn
assets.append(Asset(0, 4, "A", template_assets["A"][0], template_assets["A"][1]))  # Apartment
assets.append(Asset(4, 1, "H", template_assets["H"][0], template_assets["H"][1]))  # Hospital
assets.append(Asset(4, 4, "F", template_assets["F"][0], template_assets["F"][1]))  # Field

assets.append(Asset(2, 3, "B", template_assets["B"][0], template_assets["B"][1]))  # Another Barn
assets.append(Asset(4, 0, "A", template_assets["A"][0], template_assets["A"][1]))  # Another Apartment
assets.append(Asset(3, 2, "H", template_assets["H"][0], template_assets["H"][1]))  # Another Hospital
assets.append(Asset(2, 1, "F", template_assets["F"][0], template_assets["F"][1]))  # Another Field


def generate_lightning_strikes(town_size):
    # Poisson distribution for number of strikes per day
    strikes = []
    num_strikes = np.random.poisson(20, 5) # Average 20 strikes per day for 5 days
    for n in num_strikes:
        n = int(n)
        print(f"Number of lightning strikes: {n}")
        # uniform distribution for x and y coordinates (assume town is level)
        r = np.random.uniform(0, town_size, n)
        c = np.random.uniform(0, town_size, n)
        strikes.append([r, c])
    return strikes

town = Town(5)

town.print_town()

strikes = generate_lightning_strikes(town.size)
for day, strikes_in_a_day in enumerate(strikes):
    print(f"\n--- Day {day + 1} ---")
    for asset in assets:
        if asset.is_destroyed():
            asset.repair()
    for i in range(len(strikes_in_a_day[0])):
        strike_row = int(strikes_in_a_day[0][i])
        strike_col = int(strikes_in_a_day[1][i])
        print(f"Day {day + 1}, Strike {i+1} at ({strike_row}, {strike_col})")
        for asset in assets:
            if asset.row == strike_row and asset.col == strike_col:
                asset.take_damage(np.random.randint(1, 5))  # Random damage between 1 and 4
    print(f"Town status at the end of Day {day + 1}:")
    town.print_town()
    if town.is_destroyed():
        print("All assets in the town have been destroyed!")
        break
        