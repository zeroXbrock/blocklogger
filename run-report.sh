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

: ${RPC_URL:=$(read -p "Enter RPC_URL: " REPLY && echo $REPLY)}
: ${START_BLOCK:=$(read -p "Enter START_BLOCK: " REPLY && echo $REPLY)}
: ${END_BLOCK:=$(read -p "Enter END_BLOCK: " REPLY && echo $REPLY)}
: ${SCENARIO:=$(read -p "Enter SCENARIO: " REPLY && echo $REPLY)}

if [[ "$fetch_data" =~ ^[yY] ]]; then
    [[ -n "$RPC_URL" ]] && echo RPC_URL: $RPC_URL
    [[ -n "$START_BLOCK" ]] && echo START_BLOCK: $START_BLOCK
    [[ -n "$END_BLOCK" ]] && echo END_BLOCK: $END_BLOCK
    [[ -n "$SCENARIO" ]] && echo SCENARIO: $SCENARIO


    echo "Fetching data from $RPC_URL starting at block $START_BLOCK to $END_BLOCK..."
    bun run index.ts $RPC_URL $START_BLOCK $END_BLOCK
else
    echo "Generating report with existing data ($FILENAME)."
fi

mkdir -p output

# these can be run with the data from the TS script
python py-scripts/heatmap.py $FILENAME $SCENARIO $RPC_URL
python py-scripts/gasPerBlock.py $FILENAME $SCENARIO $RPC_URL
python py-scripts/txGasUsage.py $FILENAME $SCENARIO $RPC_URL

# this one needs a contender report
contender report
python py-scripts/timeToInclusion.py $HOME/.contender/report.csv $SCENARIO $RPC_URL
