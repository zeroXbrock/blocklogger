import sys
import json
import matplotlib.pyplot as plt
import numpy as np
import plot


def parse_hex_to_int(hex_str):
    """Convert a hexadecimal string to an integer."""
    return int(hex_str, 16)


def format_large_number(value):
    """Format large numbers with two decimal points of precision."""
    if value >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    elif value >= 1_000:
        return f"{value / 1_000:.2f}K"
    return f"{value:.0f}"


def plot_gas_usage_histogram(filename, scenario, network):
    """Read JSON data from a file and plot a histogram of gas usage."""
    try:
        with open(filename, "r") as file:
            data = json.load(file)

        txs = data.get("txs", [])

        if not txs:
            print("No transactions data found in the file.")
            return

        # Extract gas used for each transaction
        gas_used_values = [
            parse_hex_to_int(tx["receipt"]["gasUsed"])
            for tx in txs
            if tx.get("receipt") and tx["receipt"].get("gasUsed")
        ]
        # Extract block numbers from each transaction
        block_numbers = [
            parse_hex_to_int(tx["receipt"]["blockNumber"])
            for tx in txs
            if tx.get("receipt") and tx["receipt"].get("blockNumber")
        ]

        if not block_numbers:
            print("No valid block number data found in the transactions.")
            return

        min_block = min(block_numbers)
        max_block = max(block_numbers)

        if not gas_used_values:
            print("No valid gas usage data found in the transactions.")
            return

        # Define histogram bins (increments of 25K)
        max_gas = max(gas_used_values)
        bins = np.arange(0, max_gas + 12000, 12000)

        # Plot histogram
        plt.figure(figsize=(10, 6))
        plt.hist(gas_used_values, bins=bins, color="blue", edgecolor="black", alpha=0.7)

        # Customize X-axis labels
        labels = [
            format_large_number(bin_edge) if i % 2 == 0 else ""
            for i, bin_edge in enumerate(bins)
        ]
        plt.xticks(ticks=bins, labels=labels, rotation=45)
        plt.tight_layout()

        title = (
            "Gas Usage - "
            + scenario
            + " Scenario on "
            + network
            + " (blocks "
            + str(min_block)
            + "-"
            + str(max_block)
            + ")"
        )

        # Show plot
        plt.grid(axis="y")
        plot.save_plot(
            plt, title, "Gas Used", "Number of Transactions", "output/txGasUsage.png"
        )

    except FileNotFoundError:
        print(f"File not found: {filename}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {filename}")
    except KeyError as e:
        print(f"Missing expected key in data: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python txGasUsage.py <filename> <scenario> <network>")
    else:
        filename = sys.argv[1]
        scenario = sys.argv[2]
        network = sys.argv[3]
        plot_gas_usage_histogram(filename, scenario, network)
