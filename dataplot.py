import matplotlib.pyplot as plt
import numpy as np
from simulationdb import ground_strike_count_by_date, strike_count_by_date, cloud_strike_count_by_date, lat_range_distribution, long_range_distribution, get_strike_coords
from scipy.stats import poisson
import matplotlib.pyplot as plt

def display_ground_strike_distribution():
    data = ground_strike_count_by_date()
    counts = [d[1] for d in data]

    plt.figure()
    plt.hist(counts, 
            bins=20,
            density=True, )
    plt.xlabel("Number of Ground Lightning Strikes per Day over 2025 Jan to 2026 Jan")
    plt.ylabel("Probability Density")
    plt.title("Distribution of Daily Ground Lightning Strikes")
    plt.plot(sorted(counts), poisson.pmf(sorted(counts), 2))
    plt.show()

def display_lat_range_distribution():
    data = lat_range_distribution()
    ranges = [item[0] for item in data]
    frequencies = [item[1] for item in data]

    plt.figure()
    plt.bar(sorted(ranges), frequencies, color='steelblue', edgecolor='black')
    plt.xlabel("Latitude Ranges")
    plt.ylabel("Frequency of Lightning Strikes")
    plt.title("Distribution of Latitude Ranges of Lightning Strikes")
    plt.show()

def display_long_range_distribution():
    data = long_range_distribution()
    ranges = [item[0] for item in data]
    frequencies = [item[1] for item in data]

    plt.figure()
    plt.bar(sorted(ranges), frequencies, color='steelblue', edgecolor='black')
    plt.xlabel("Longitude Ranges")
    plt.ylabel("Frequency of Lightning Strikes")
    plt.title("Distribution of Longitude Ranges of Lightning Strikes")
    plt.show()

def strike_distribution():
    arr = get_strike_coords()
    X = [float(item[0]) for item in arr]
    Y = [float(item[1]) for item in arr]

    # create 2D histogram
    heatmap, xedges, yedges = np.histogram2d(X, Y, bins=50)

    # plot
    plt.imshow(
        heatmap.T,                # transpose for correct orientation
        origin='lower',
        aspect='auto',
        extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]]
    )

    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.colorbar(label="Count")
    plt.title("2D Heatmap of Singapore's lightning strike locations in 2025 Jan to 2026 Jan")
    plt.show()
# display_ground_strike_distribution()
# display_lat_range_distribution()
# display_long_range_distribution()
strike_distribution()