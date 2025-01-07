import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

data = pd.read_csv('/Users/felix/Desktop/BAabbildungen/flucht_new3.csv', delimiter='\t', header=None)
tags = data[0]
total_rows = len(data)

print(f"Gesamtanzahl der Zeilen: {total_rows}")
target_tags = ['Flüchtlinge sind kriminell', 'Flüchtlinge sind kostenintensiv', 'Flüchtlinge sind willkommen']
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

color_map = {
    'Flüchtlinge sind kriminell': 'blue',
    'Flüchtlinge sind kostenintensiv': 'orange',
    'Flüchtlinge sind willkommen': 'green'
}
colors = [color_map[label] for label in labels]

if total > 0:
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    plt.title(f'Verteilung der Label (Insgesamt: {total})')
    plt.axis('equal')
    plt.show()
else:
    print("Keine Ziel-Tags gefunden.")