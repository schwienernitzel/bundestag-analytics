import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

data = pd.read_csv('output/dataset-annotated-241124.csv', delimiter='\t', header=None)
tags = data[0]
total_rows = len(data)

print(f"Gesamtanzahl der Zeilen: {total_rows}")
target_tags = ['Kriminelle', 'Kostenintensive', 'Willkommene', 'Nutzbringende']
filtered_tags = [tag for tag in tags if tag in target_tags]
tag_counts = Counter(filtered_tags)
labels = list(tag_counts.keys())
sizes = list(tag_counts.values())
total = sum(sizes)

print("\nAnalyse der Ziel-Tags:")
for label, size in zip(labels, sizes):
    percentage = (size / total) * 100 if total > 0 else 0
    print(f"Tag: {label}, Anzahl: {size}, Anteil: {percentage:.2f}%")

print(f"\nGesamtanzahl Ziel-Tags: {total}")
if total > 0:
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title(f'Verteilung der Tags (Insgesamt: {total})')
    plt.axis('equal')
    plt.show()
else:
    print("Keine Ziel-Tags gefunden.")