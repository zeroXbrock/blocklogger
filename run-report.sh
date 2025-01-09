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

# get vars from user if not set in environment
: ${RPC_URL:=$(read -p "Enter RPC_URL: " REPLY && echo $REPLY)}
: ${SCENARIO:="$(read -p "Enter SCENARIO: " REPLY && echo $REPLY)"}

# print vars
[[ -n "$RPC_URL" ]] && echo RPC_URL: $RPC_URL
[[ -n "$START_BLOCK" ]] && echo START_BLOCK: $START_BLOCK
[[ -n "$END_BLOCK" ]] && echo END_BLOCK: $END_BLOCK
[[ -n "$SCENARIO" ]] && echo SCENARIO: $SCENARIO

if [[ "$fetch_data" =~ ^[yY] ]]; then
    : ${START_BLOCK:=$(read -p "Enter START_BLOCK: " REPLY && echo $REPLY)}
    : ${END_BLOCK:=$(read -p "Enter END_BLOCK: " REPLY && echo $REPLY)}
    echo "Fetching data from $RPC_URL starting at block $START_BLOCK to $END_BLOCK..."
    bun run index.ts $RPC_URL $START_BLOCK $END_BLOCK
else
    echo "Generating report with existing data ($FILENAME)."
fi

mkdir -p output
timestamp=$(date +%s)
REPORT_DIR=output/report_$timestamp
mkdir -p $REPORT_DIR


# these can be run with the data from the TS script
python py-scripts/heatmap.py $FILENAME "$SCENARIO" $RPC_URL $REPORT_DIR/heatmap.png
python py-scripts/gasPerBlock.py $FILENAME "$SCENARIO" $RPC_URL $REPORT_DIR/gasPerBlock.png
python py-scripts/txGasUsage.py $FILENAME "$SCENARIO" $RPC_URL $REPORT_DIR/txGasUsage.png

# this one needs a contender report
contender report
python py-scripts/timeToInclusion.py $HOME/.contender/report.csv "$SCENARIO" $RPC_URL $REPORT_DIR/timeToInclusion.png

# Generate markdown file with image links
MARKDOWN_FILE="$REPORT_DIR/report.md"

echo "# Flashbots Chain Performance Report" > $MARKDOWN_FILE
echo "" >> $MARKDOWN_FILE

echo "## Summary" >> $MARKDOWN_FILE
echo "" >> $MARKDOWN_FILE

echo "*$(date +"%B %d, %Y")*" >> $MARKDOWN_FILE
echo "" >> $MARKDOWN_FILE

echo "***Scenario:** $SCENARIO*" >> $MARKDOWN_FILE
echo "" >> $MARKDOWN_FILE
echo '<img src="../../flashbots_logo_dark.svg" style="width: 20%; height: auto;" />' >> $MARKDOWN_FILE
echo '<div style="page-break-after: always;"></div>' >> $MARKDOWN_FILE
echo "" >> $MARKDOWN_FILE

echo "## Reports" >> $MARKDOWN_FILE

count=0
images=("gasPerBlock.png" "heatmap.png" "timeToInclusion.png" "txGasUsage.png")
for image in "${images[@]}"; do
    header=$(echo $image | sed -e 's/.png//' -e 's/\b\(.\)/\u\1/g' -e 's/\([a-z]\)\([A-Z]\)/\1 \2/g')
    echo "### $header" >> $MARKDOWN_FILE
    echo "" >> $MARKDOWN_FILE
    echo "![$header](./$image)" >> $MARKDOWN_FILE
    echo "" >> $MARKDOWN_FILE
    count=$((count+1))
    if [ $count -lt ${#images[@]} ]; then
        echo '<div style="page-break-after: always;"></div>' >> $MARKDOWN_FILE
        echo "" >> $MARKDOWN_FILE
    fi
done

echo "Markdown file '"$MARKDOWN_FILE"' generated with image links."
