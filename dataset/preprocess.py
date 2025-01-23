import csv
import re

def preprocess_speech(text):
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    if len(sentences) > 4:
        sentences = sentences[2:-2]
    else:
        sentences = []
    return " ".join(sentences)

input_file = "dataset-210125.csv"
output_file = "dataset-210125-preprocessed.csv"

with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8", newline="") as outfile:
    reader = csv.reader(infile, delimiter="\t")
    writer = csv.writer(outfile, delimiter="\t")
    writer.writerow(["Sitzungsnummer", "Datum", "ID", "Redner", "Redebeitrag"])

    for row in reader:
        if len(row) < 5:
            continue

        sitzungsnummer, datum, id_, redner, redebeitrag = row
        redebeitrag = preprocess_speech(redebeitrag)
        writer.writerow([sitzungsnummer, datum, id_, redner, redebeitrag])

print(f"Die vorverarbeiteten Daten wurden in '{output_file}' gespeichert.")