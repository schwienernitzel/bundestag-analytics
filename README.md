### Usage:

```bash
cd protocols && ls *.xml | wc -l  ## Check total number of protocols
cd protocols && grep -Hrn "endgültige Stenografische"  ## Check for incomplete protocols
python3 execute.py > output.csv  ## Run the conversion script
sed -i '/<redner id="[^:]*:/d' output.csv  ## Remove regex leftovers
sed -i 's/#//g' output.csv  ## Remove seperators
sed -i 's/[0-9]\+Anlage.*//g' output.csv  ## Remove more leftovers
wc -l output.csv  ## Check total number of lines
grep -i "migration" output.csv > output_migration.csv  ## Filter for context, e.g. "migration"
jupyter notebook --no-browser --port=8888  ## Start a local jupyter environment
```

> Note: Install `python3` on your current runtime, which preferably should be a Linux distribution. If you use this parser for the first time, you can also run `./quick_run.sh` inside of your Terminal.

> [!WARNING]
> Make sure that you move previous output files out of the way before you generate any further ones in order to avoid data loss!
