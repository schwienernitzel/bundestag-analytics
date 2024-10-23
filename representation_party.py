import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

data = pd.read_csv('out/output_migration-annotated.csv', delimiter='\t', header=None)
tags = data[3]
redner_fraktionen = data[9]

fraktionen = ["afd", "cdu/csu", "fdp", "spd", "bündnis 90/die grünen", "die linke", "bsw", "fraktionslos", "bundes"]
fraktion_title_map = {
    "afd": "AfD-Fraktion",
    "cdu/csu": "CDU/CSU-Fraktion",
    "fdp": "FDP-Fraktion",
    "spd": "SPD-Fraktion",
    "bündnis 90/die grünen": "Fraktion Bündnis 90/Die Grünen",
    "die linke": "Gruppe Die Linke",
    "bsw": "Gruppe BSW",
    "fraktionslos": "Fraktionslose Abgeordnete",
    "bundes": "Mitglieder der Bundesregierung"
}

redner_fraktionen_lower = redner_fraktionen.str.lower()
unique_tags = tags.unique()
colors = plt.cm.tab10(range(len(unique_tags)))
tag_color_map = {tag: colors[i] for i, tag in enumerate(unique_tags)}
fig, axes = plt.subplots(3, 3, figsize=(15, 10))
axes = axes.flatten()
total_rows = len(data)

for i, fraktion in enumerate(fraktionen):
    fraktion_tags = tags[redner_fraktionen_lower.str.contains(fraktion, na=False)]
    tag_counts = Counter(fraktion_tags)
    labels = list(tag_counts.keys())
    sizes = list(tag_counts.values())
    total = sum(sizes)
    title = fraktion_title_map.get(fraktion, fraktion.upper())
    title_with_count = f'{title} ({total} Beiträge)'
    ax = axes[i]

    if total > 0:
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90,
                                          colors=[tag_color_map[label] for label in labels])
        ax.set_title(f'{title_with_count}')
        ax.axis('equal')
    else:
        ax.text(0.5, 0.5, 'Keine Daten', ha='center', va='center', fontsize=12)
        ax.set_title(f'{title_with_count}')
        ax.axis('off')

handles = [plt.Line2D([0], [0], marker='o', color='w', label=tag,
                      markersize=10, markerfacecolor=tag_color_map[tag]) for tag in unique_tags]
fig.legend(handles=handles, title=f"Insgesamt: {total_rows} Redebeiträge", loc='center',
           bbox_to_anchor=(0.5, 0.05), ncol=3)
plt.tight_layout(rect=[0, 0.1, 1, 1])
plt.show()