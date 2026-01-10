# Monte Carlo Lightning Strike Model
Estimating lightning strikes across a town, & optimising town layout to avoid confetti waste & minimise interference with town member lives

**Critical Town Assets**
- Barn (B)
- Cotton Field (C)
- Apartment (A)
- Grocery Store (G)

Each **Asset** has:
1. Multiple contiguous (x) and (y) coordinates (indicating location of asset)
2. Damage Threshold (1-5)
3. Repair Time (from lightning damage) (1-4)

Each **Lightning Strike** (LS) has:
1. Direct Strike Radius (1-2)
2. Indirect Strike Radius (1-3)
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
1. Day increment occurs after **10** lightning strikes
2. Damaged Assets require corresponding "Repair Time" days to be restored (assuming they are not striked again) -> damaged components have damage threshold = 0

If all assets are **destroyed**, end simulation.

# Objective
To extract optimal layout of town for minimal damage given thunderstorm
