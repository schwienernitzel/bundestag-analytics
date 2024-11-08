#!/bin/bash
if [ -z "$AMOUNT" ]; then
    echo "Please set the AMOUNT environment variable before running the script."
    echo "Example: export AMOUNT=100"
    exit 1
fi

if [ -z "$FILTER" ]; then
    echo "Please set the FILTER environment variable before running the script."
    echo "Example: export FILTER=Kriminelle"
    exit 1
fi

if [ $# -ne 2 ]; then
    echo "Usage: $0 <input_file.csv> <output_file.csv>"
    exit 1
fi

input_file="$1"
output_file="$2"

if [ ! -f "$input_file" ]; then
    echo "The file $input_file does not exist."
    exit 1
fi

echo "Picking $AMOUNT random lines containing $FILTER from $input_file..."

grep "$FILTER" "$input_file" | shuf -n "$AMOUNT" > "$output_file"

echo -e "\033[32mDone! File has been saved to $output_file\033[0m"
