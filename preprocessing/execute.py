import os
import subprocess

curdir = os.getcwd()
protocols = os.path.join(curdir, '../protocols')
os.chdir(protocols)

files = []

for file in os.listdir(protocols):
    if file.endswith('.xml'):
        number = int(file[:-4])
        files.append((number, file))

files.sort()
total = len(files)

for number, file in files:
    num = file[2:-4]
    try:
        result = subprocess.run(['python3', '../preprocessing/convert_xml.py', file], check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Verarbeiten von {file}: {e.stderr}")
