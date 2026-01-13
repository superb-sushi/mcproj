import numpy as np
from db import add_sample, add_asset, add_lightning_strike, reset_db, add_experiment_params_if_not_exist

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
    def __init__(self, row=0, col=0, asset_type=0, damage_threshold=0, repair_time=0, importance=0, is_empty=False, ):
        self.row = row
        self.col = col
        self.asset_type = asset_type
        self.damage_threshold = damage_threshold
        self.repair_time = repair_time
        self.damage_taken = 0
        self.repair_counter = 0
        self.is_empty = is_empty
        self.importance = importance
    
    def take_damage(self, damage):
        if self.is_destroyed():
            self.repair_counter = 0
        else:
            self.damage_taken += damage
            #print(f"  {building_types[self.asset_type]} at ({self.row}, {self.col}) took {damage} damage (HP: {self.damage_threshold - self.damage_taken}/{self.damage_threshold}).")
            if self.damage_taken >= self.damage_threshold:
                self.damage_taken = self.damage_threshold
                #print(f"{building_types[self.asset_type]} at ({self.row}, {self.col}) has been destroyed.")
    
    def repair(self):
        self.repair_counter += 1
        if self.repair_counter >= self.repair_time:
            self.repair_counter = 0
            self.damage_taken = 0
            #print(f"  {building_types[self.asset_type]} at ({self.row}, {self.col}) has been repaired.")
    
    def is_destroyed(self):
        return self.damage_taken >= self.damage_threshold

    def display(self):
        return "O" if self.is_empty else (self.asset_type if not self.is_destroyed() else "X")

template_assets = {"B":[2, 2, 3], "A":[3, 3, 7], "H":[5, 4, 10], "F":[1, 1, 1]} # Assets -> Building Type: [Damage Threshold, Repair Time, Importance]

assets = []
assets.append(Asset(4, 2, "B", template_assets["B"][0], template_assets["B"][1], template_assets["B"][2]))  # Barn
assets.append(Asset(0, 4, "A", template_assets["A"][0], template_assets["A"][1], template_assets["A"][2]))  # Apartment
assets.append(Asset(4, 1, "H", template_assets["H"][0], template_assets["H"][1], template_assets["H"][2]))  # Hospital
assets.append(Asset(4, 4, "F", template_assets["F"][0], template_assets["F"][1], template_assets["F"][2]))  # Field

assets.append(Asset(2, 3, "B", template_assets["B"][0], template_assets["B"][1], template_assets["B"][2]))  # Another Barn
assets.append(Asset(4, 0, "A", template_assets["A"][0], template_assets["A"][1], template_assets["A"][2]))  # Another Apartment
assets.append(Asset(3, 2, "H", template_assets["H"][0], template_assets["H"][1], template_assets["H"][2]))  # Another Hospital
assets.append(Asset(2, 1, "F", template_assets["F"][0], template_assets["F"][1], template_assets["F"][2]))  # Another Field


def generate_lightning_strikes(town_size, expected_daily_lightning_stikes, no_of_days): # Generates [[[x_coords], [y_coords]], [x1_coords], [y1_coords]], ...] for each day x_i
    # Poisson distribution for number of strikes per day
    strikes = []
    num_strikes = np.random.poisson(expected_daily_lightning_stikes, no_of_days) # Average 'expected_daily_lightning_strikes' strikes per day for X days
    for n in num_strikes:
        n = int(n)
        #print(f"Number of lightning strikes: {n}")
        # uniform distribution for x and y coordinates (assume town is level)
        r = np.random.uniform(0, town_size, n)
        c = np.random.uniform(0, town_size, n)
        strikes.append([r, c])
    return strikes

def lightning_simulation_sample(town_size, expected_daily_lightning_stikes, no_of_days):
    town = Town(town_size)

    survive = 1
    survival_day = 0

    #town.print_town()

    strikes = generate_lightning_strikes(town.size, expected_daily_lightning_stikes, no_of_days)
    for day, strikes_in_a_day in enumerate(strikes):
        survival_day += 1
        #print(f"\n--- Day {day + 1} ---")
        for asset in assets:
            if asset.is_destroyed():
                asset.repair()
        for i in range(len(strikes_in_a_day[0])):
            strike_row = int(strikes_in_a_day[0][i])
            strike_col = int(strikes_in_a_day[1][i])
            #print(f"Day {day + 1}, Strike {i+1} at ({strike_row}, {strike_col})")
            for asset in assets:
                if asset.row == strike_row and asset.col == strike_col:
                    asset.take_damage(np.random.randint(1, 5))  # Random damage between 1 and 4
        #print(f"Town status at the end of Day {day + 1}:")
        #town.print_town()
        if town.is_destroyed():
            #print("All assets in the town have been destroyed!")
            survive = 0
            break
    # Return [survival status, total num of days, day town survived till, total assets, num of destroyed assets, all assets (type, row, col, destroyed?), daily lightning strike counts]
    return [survive, len(strikes), survival_day, len(assets), sum(1 for asset in assets if asset.is_destroyed()), [[asset.asset_type, asset.row, asset.col, asset.importance, asset.is_destroyed()] for asset in assets], [len(strikes_coords[0]) for strikes_coords in strikes]]


def run_simulations(num_simulations, town_size, expected_daily_lightning_stikes, no_of_days):
    experiment_id = add_experiment_params_if_not_exist(1, town_size, expected_daily_lightning_stikes, no_of_days)
    for i in range(num_simulations):
        print(f"\n=== Simulation Run {i + 1} ===")
        result = lightning_simulation_sample(town_size, expected_daily_lightning_stikes, no_of_days)
        sample_id = add_sample(experiment_id, result[0] == 1, result[1], result[2], result[3], result[4])
        for asset_info in result[5]:
            add_asset(sample_id, asset_info[0], asset_info[1], asset_info[2], asset_info[3], asset_info[4])
        for day, num_strikes in enumerate(result[6]):
            add_lightning_strike(sample_id, day + 1, num_strikes)
        print(f"Simulation {i + 1} results recorded in database.")

reset_db()
run_simulations(1000, 5, 15, 30)