#!/bin/bash

FILENAME="storageData.json"

# check if storageData.json exists
if [ -f "$FILENAME" ]; then
    echo "$FILENAME exists."
    read -p "Do you want to fetch new data? (y/N): " fetch_data
else
    echo "$FILENAME does not exist."
    fetch_data="y"
fi

if [[ "$fetch_data" =~ ^[yY] ]]; then
    [[ -n "$RPC_URL" ]] && echo RPC_URL: $RPC_URL
    [[ -n "$START_BLOCK" ]] && echo START_BLOCK: $START_BLOCK
    [[ -n "$END_BLOCK" ]] && echo END_BLOCK: $END_BLOCK

    : ${RPC_URL:=$(read -p "Enter RPC_URL: " REPLY && echo $REPLY)}
    : ${START_BLOCK:=$(read -p "Enter START_BLOCK: " REPLY && echo $REPLY)}
    : ${END_BLOCK:=$(read -p "Enter END_BLOCK: " REPLY && echo $REPLY)}

    echo "Fetching data from $RPC_URL starting at block $START_BLOCK to $END_BLOCK..."
    bun run index.ts $RPC_URL $START_BLOCK $END_BLOCK
else
    echo "Generating report with existing data ($FILENAME)."
fi

python py-scripts/heatmap.py $FILENAME
python py-scripts/gasPerBlock.py $FILENAME
