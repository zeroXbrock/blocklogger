# import json
# import os
# import matplotlib.pyplot as plt


# # Define the types for the data structure
# class StorageSlotGroup:
#     def __init__(self, slots: dict[str, str]):
#         self.slots = slots


# class Data:
#     def __init__(
#         self,
#         block_number: int,
#         tx_hash: str,
#         storage_slots: list[StorageSlotGroup or None],
#     ):
#         self.block_number = block_number
#         self.tx_hash = tx_hash
#         self.storage_slots = storage_slots


# # Read data from pubUni.json file
# data_file_path = os.path.join(os.path.dirname(__file__), "pubUni.json")
# with open(data_file_path, "r") as file:
#     raw_data = file.read()
# DATA = json.loads(raw_data)


# def count_storage_slot_frequencies(data: list[dict]) -> dict[str, dict[str, int]]:
#     """
#     Count the frequency of each unique storage slot in the data and the number of data entries that touch each slot.
#     """
#     slot_frequency: dict[str, dict[str, int]] = {}

#     for record_index, record in enumerate(data):
#         storage_slots = record.get("storageSlots", [])
#         for slot_group in storage_slots:
#             if slot_group:  # Skip null entries
#                 for slot in slot_group:
#                     if slot not in slot_frequency:
#                         slot_frequency[slot] = {
#                             "total_frequency": 0,
#                             "entries_touched": 0,
#                         }
#                     slot_frequency[slot]["total_frequency"] += 1
#                     slot_frequency[slot]["entries_touched"] += 1

#     return slot_frequency


# def plot_bar_graph(slot_frequency: dict[str, dict[str, int]]) -> None:
#     """
#     Plot a bar graph of the slot frequencies using Matplotlib.
#     """

#     # Sort storage slots to ensure consistency in display
#     unique_slots = sorted(slot_frequency.keys())

#     # Extract the frequencies and entries touched for each slot
#     total_frequencies = [
#         slot_frequency[slot]["total_frequency"] for slot in unique_slots
#     ]
#     entries_touched = [slot_frequency[slot]["entries_touched"] for slot in unique_slots]

#     # Abbreviate slot labels for better display
#     abbreviated_labels = [slot[2:8] + "..." + slot[-6:] for slot in unique_slots]

#     x = range(len(unique_slots))

#     plt.figure(figsize=(12, 5))

#     plt.bar(x, total_frequencies, label="Total Frequency", color="orange", alpha=0.7)

#     plt.xlabel("Storage Slot (Abbreviated)")
#     plt.ylabel("# Times Updated")
#     plt.title(
#         "Storage Slot Access Frequency (all contracts) -- Contender UniswapV2 Scenario on Public Unichain Endpoint (blocks 7638184 - 7638199)"
#     )
#     plt.xticks(ticks=x, labels=abbreviated_labels, rotation=90, fontfamily="monospace")
#     plt.legend()
#     plt.show()


# def main() -> None:
#     slot_frequency = count_storage_slot_frequencies(DATA)
#     plot_bar_graph(slot_frequency)


# if __name__ == "__main__":
#     main()


import json
import os
import matplotlib.pyplot as plt
import numpy as np


# Define the types for the data structure
class StorageSlotGroup:
    def __init__(self, slots: dict[str, str]):
        self.slots = slots


class Data:
    def __init__(
        self,
        block_number: int,
        tx_hash: str,
        storage_slots: list[StorageSlotGroup or None],
    ):
        self.block_number = block_number
        self.tx_hash = tx_hash
        self.storage_slots = storage_slots


# Read data from pubUni.json file
data_file_path = os.path.join(os.path.dirname(__file__), "pubUni.json")
with open(data_file_path, "r") as file:
    raw_data = file.read()
DATA = json.loads(raw_data)


def count_storage_slot_frequencies(data: list[dict]) -> dict[str, dict[int, int]]:
    """
    Count the frequency of each unique storage slot across all block numbers in the data.
    """
    slot_frequency: dict[str, dict[int, int]] = {}

    for record in data:
        block_number = record.get("blockNumber")
        storage_slots = record.get("storageSlots", [])
        for slot_group in storage_slots:
            if slot_group:  # Skip null entries
                for slot in slot_group:
                    if slot not in slot_frequency:
                        slot_frequency[slot] = {}
                    slot_frequency[slot][block_number] = (
                        slot_frequency[slot].get(block_number, 0) + 1
                    )

    return slot_frequency


def plot_heatmap(slot_frequency: dict[str, dict[int, int]]) -> None:
    """
    Plot a heatmap where the x-axis represents block numbers and the y-axis represents storage slots.
    """

    # Extract unique block numbers and storage slots
    unique_blocks = sorted(
        {block for slot_data in slot_frequency.values() for block in slot_data.keys()}
    )
    unique_slots = sorted(slot_frequency.keys())

    # Create a 2D array to visualize the heatmap
    heatmap = np.zeros((len(unique_slots), len(unique_blocks)))

    for row_index, slot in enumerate(unique_slots):
        for col_index, block in enumerate(unique_blocks):
            heatmap[row_index, col_index] = slot_frequency.get(slot, {}).get(block, 0)

    plt.figure(figsize=(12, 8))
    plt.imshow(heatmap, cmap="hot", interpolation="nearest", aspect="auto")
    plt.colorbar(label="Frequency of Slot Access")
    plt.title(
        "Storage Slot Access Frequency (all contracts) -- Contender UniswapV2 Scenario on Public Unichain Endpoint (blocks 7638184 - 7638199)"
    )

    # Abbreviate slot labels to 6 hex digits
    abbreviated_labels = [slot[:6] for slot in unique_slots]

    plt.xticks(
        ticks=range(len(unique_blocks)),
        labels=[str(block) for block in unique_blocks],
        rotation=90,
        fontfamily="monospace",
    )
    plt.yticks(
        ticks=range(0, len(unique_slots), max(1, len(unique_slots) // 40)),
        labels=[
            abbreviated_labels[i]
            for i in range(0, len(unique_slots), max(1, len(unique_slots) // 40))
        ],
        fontfamily="monospace",
    )

    # plt.yticks(
    #     ticks=range(len(unique_slots)),
    #     labels=abbreviated_labels,
    #     fontfamily="monospace",
    # )
    plt.xlabel("Block Number")
    plt.ylabel("Storage Slots (Abbreviated)")
    plt.show()


def main() -> None:
    slot_frequency = count_storage_slot_frequencies(DATA)
    plot_heatmap(slot_frequency)


if __name__ == "__main__":
    main()
