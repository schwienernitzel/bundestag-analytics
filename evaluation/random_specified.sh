#!/bin/bash
if [ -z "$AMOUNT" ]; then
    echo "Please set the AMOUNT environment variable before running the script."
    echo "Example: export AMOUNT=100"
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

echo "Picking $AMOUNT random lines per label from $input_file..."

labels=("Kriminelle" "Kostenintensive" "Willkommene" "Nutzbringende")

> "$output_file"

lines_per_label=$((AMOUNT / ${#labels[@]}))

for label in "${labels[@]}"; do
    grep "^$label" "$input_file" | shuf -n "$lines_per_label" >> "$output_file"
done

echo -e "\033[32mDone! File has been saved to $output_file\033[0m"
