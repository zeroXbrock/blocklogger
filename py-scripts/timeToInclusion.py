import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plot


def format_large_number(value):
    """Format large numbers with two decimal points of precision."""
    if value >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    elif value >= 1_000:
        return f"{value / 1_000:.2f}K"
    return f"{value:.0f}"


def plot_time_to_inclusion_histogram(filename, scenario, network):
    """Read CSV data from a file and plot a histogram of time-to-inclusion."""
    try:
        # Read the CSV file into a DataFrame
        data = pd.read_csv(filename)

        # Ensure required columns exist
        required_columns = ["start_time", "end_time"]
        for column in required_columns:
            if column not in data.columns:
                print(f"Missing required column: {column}")
                return

        # Calculate time-to-inclusion
        data["time_to_inclusion"] = data["end_time"] - data["start_time"]
        min_block = data["block_number"].min()
        max_block = data["block_number"].max()

        # Define histogram bins (increments of 1 second)
        max_time = data["time_to_inclusion"].max()
        bins = np.arange(0, max_time + 1, 1)

        # Plot histogram
        plt.figure(figsize=(10, 6))
        plt.hist(
            data["time_to_inclusion"],
            bins=bins,
            color="blue",
            edgecolor="black",
            alpha=0.7,
        )

        # Customize X-axis ticks
        labels = [
            format_large_number(bin_edge) if i % 2 == 0 else ""
            for i, bin_edge in enumerate(bins)
        ]
        plt.xticks(ticks=bins, labels=labels)
        plt.tight_layout()
        plt.grid(axis="y")

        title = (
            "Time-to-Inclusion Histogram - "
            + scenario
            + " Scenario on "
            + network
            + " (blocks "
            + str(min_block)
            + "-"
            + str(max_block)
            + ")"
        )

        plot.save_plot(
            plt,
            title,
            "Time-to-Inclusion (seconds)",
            "Number of Transactions",
            "output/timeToInclusion.png",
        )

    except FileNotFoundError:
        print(f"File not found: {filename}")
    except pd.errors.EmptyDataError:
        print(f"No data found in file: {filename}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python timeToInclusion.py <filename> <scenario> <network>")
    else:
        filename = sys.argv[1]
        scenario = sys.argv[2]
        network = sys.argv[3]
        plot_time_to_inclusion_histogram(filename, scenario, network)
