import pandas as pd
from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

input_csv_path = "out/output_191.csv"
output_csv_path = "zeroshot/output_zeroshot.csv"

df = pd.read_csv(input_csv_path, sep='\t', header=None)
categories = ["Kriminelle", "Nützliche", "Kostenintensive", "Integrationswillige", "Willkommene"]

predicted_labels = []
total_rows = len(df)
print(f"Starte die Klassifikation von {total_rows} Zeilen...")

for index, text in enumerate(df.iloc[:, 4]):
    if pd.isnull(text):
        predicted_labels.append("Keine Daten")
        print(f"Zeile {index + 1}/{total_rows}: Übersprungen (Keine Daten)")
        continue

    result = classifier(text, candidate_labels=categories)
    best_label = result["labels"][0]
    predicted_labels.append(best_label)
    print(f"{best_label} - '{text}'")

df["prediction"] = predicted_labels
df.to_csv(output_csv_path, sep='\t', index=False, header=False)

print(f"Klassifizierung abgeschlossen! Ergebnisse wurden in '{output_csv_path}' gespeichert.")