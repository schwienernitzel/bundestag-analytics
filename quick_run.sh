#!/bin/bash
echo "Executing the python script..."
python3 execute.py > output.csv
echo "Conversion complete. Removing leftovers..."
sed -i '/<redner id="[^:]*:/d' output.csv
sed -i 's/#//g' output.csv
echo -e "\033[32mDone!\033[0m"
