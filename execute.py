import os
import subprocess

curdir = os.getcwd()
files = []

for file in os.listdir(curdir):
    if file.endswith('.xml'):
        number = int(file[:-4])
        files.append((number, file))

files.sort()
total = len(files)

for number, file in files:
    num = file[2:-4]
    print(f"Plenarprotokoll: {num}. Sitzung")
    try:
        result = subprocess.run(['python3', 'convert_xml.py', file], check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Verarbeiten von {file}: {e.stderr}")
