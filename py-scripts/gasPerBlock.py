import sys
import json
import matplotlib.pyplot as plt
import plot


def parse_hex_to_int(hex_str):
    """Convert a hexadecimal string to an integer."""
    return int(hex_str, 16)


def plot_gas_used_per_block(filename, scenario, network):
    """Read JSON data from a file and plot gasUsed per block number."""
    try:
        with open(filename, "r") as file:
            data = json.load(file)

        blocks = data.get("blocks", [])

        if not blocks:
            print("No blocks data found in the file.")
            return

        block_numbers_hex = [block["number"] for block in blocks]
        block_numbers = [parse_hex_to_int(num) for num in block_numbers_hex]
        gas_used = [parse_hex_to_int(block["gasUsed"]) for block in blocks]

        # Plot the data
        plt.figure(figsize=(10, 6))
        plt.plot(block_numbers, gas_used, marker="o", linestyle="-", label="Gas Used")
        title = (
            "Gas Used Per Block - "
            + scenario_name
            + " on "
            + network
            + " (blocks "
            + str(min(block_numbers))
            + "-"
            + str(max(block_numbers))
            + ")"
        )
        plt.xticks(block_numbers, block_numbers, rotation=45, fontsize=8)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()

        plot.save_plot(plt, title, "Block Number", "Gas Used", "output/gasPerBlock.png")

    except FileNotFoundError:
        print(f"File not found: {filename}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {filename}")
    except KeyError as e:
        print(f"Missing expected key in data: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python gasPerBlock.py <filename> <scenario_name> <network>")
    else:
        filename = sys.argv[1]
        scenario_name = sys.argv[2]
        network = sys.argv[3]
        print(network)
        plot_gas_used_per_block(filename, scenario_name, network)
