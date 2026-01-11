# Monte Carlo Lightning Strike Model
Estimating lightning strikes across a town, & optimising town layout to minimise damage to town assets.

**Critical Town Assets**
- Barn (B)
- Hospital (H)
- Apartment (A)
- Field (F)

Each **Asset** has:
1. X and Y coordinates (indicating location of asset)
2. Damage Threshold (1-5)
3. Repair Time (from lightning damage) (1-4)

Each **Lightning Strike** (LS) has:
1. Direct Strike Radius (1)
2. Indirect Strike Radius (1-2)
3. Strength of Lightning Strike (1-4)

In order for an **Asset** to be damaged:
- Direct / Indirect Strike of LS has to overlap with the corresponding (x, y) coordinates of the asset
- Extent of Damage = (1 if LS == Direct else 0.5) x (strength of LS)
- If Damage Threshold - Extent of Damage <= 0, asset is destroyed

## Simulation Details
For each run:
1. Generate Lightning Strike (based on probability distribution)
2. Apply Damage to Asset (D = Damage Threshold - Extent of Damage)

For each day:
1. Damaged Assets require corresponding "Repair Time" days to be restored
2. If Damaged Assets are striked again, their repair time restarts from 0 (assume destroyed again!)

# Objective
To extract optimal layout of town for minimal damage given thunderstorm.

# Data Collection
### Database Schema
1. **ExperimentParams**(eid, town_size, exp_daily_lightning, max_days)
2. **Samples**(id, eid, survived, total_days, survival_day, total_assets, num_of_destroyed)
3. **Assets**(sid, atype, a_row, a_col, destroyed)
4. **LightningStrikes**(sid, day, num_of_strikes)

- `ExperimentParams` notes down the parameters of a given set of Samples (i.e. town size, expected number of lightning strikes per day, and the max days the lightning storm goes on for)
- `Samples` represents the results collected from one sample. One sample involves putting the town (of size `town_size`) under a simulated thunderstorm the goes on for `max_days` days, where each day, the number of lightning strikes follows a probability distribution of Poisson(`exp_daily_lightning`).
  - Striking coordinates of lightning strikes follow a uniform distribution (town is assumed to be level)
  - Each sample consists of 2 instances of ALL asset types (total 8 different buildings), located in fixed and constant positions across ALL samples
- `Assets` contain information about the various assets in each sample, including type, location, and if they were destroyed (NOT DAMAGED) at the end of each run.
- `LightningStrikes` contains information on the number of lightning strikes in a certain day for a given sample
