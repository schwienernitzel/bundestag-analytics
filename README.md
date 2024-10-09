## XMLparser: Parse speeches of German plenary sessions (Bundestag)

### Usage:

```bash
python3 execute.py > output.csv  ## Run the conversion script
sed -i '/<redner id="[^:]*:/d' output.csv  ## Remove regex leftovers
sed -i 's/#//g' output.csv  ## Remove seperators
```
