import matplotlib.pyplot as plt
from simulationdb import ground_strike_count_by_date, strike_count_by_date, cloud_strike_count_by_date, lat_range_distribution, long_range_distribution
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

display_ground_strike_distribution()
display_lat_range_distribution()
display_long_range_distribution()