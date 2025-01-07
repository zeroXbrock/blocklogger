import sys
import json
import matplotlib.pyplot as plt


def parse_hex_to_int(hex_str):
    """Convert a hexadecimal string to an integer."""
    return int(hex_str, 16)


def plot_gas_used_per_block(filename):
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
        plt.title("Gas Used Per Block")
        plt.xlabel("Block Number")
        plt.ylabel("Gas Used")
        plt.xticks(block_numbers, block_numbers, rotation=45, fontsize=8)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()

        plt.show()

    except FileNotFoundError:
        print(f"File not found: {filename}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {filename}")
    except KeyError as e:
        print(f"Missing expected key in data: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python gasPerBlock.py <filename>")
    else:
        filename = sys.argv[1]
        plot_gas_used_per_block(filename)
