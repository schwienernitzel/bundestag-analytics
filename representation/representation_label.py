import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

data = pd.read_csv('/Users/felix/Desktop/BAabbildungen/flucht_new3.csv', delimiter='\t', header=None)
tags = data[0]
redner_fraktionen = data[6]

valid_tags = ['Flüchtlinge sind kriminell', 'Flüchtlinge sind kostenintensiv', 'Flüchtlinge sind willkommen']
fraktionen = ["afd", "cdu/csu", "fdp", "spd", "bündnis 90/die grünen", "die linke", "bsw", "fraktionslos", "bundes"]
fraktion_title_map = {
    "afd": "AfD",
    "cdu/csu": "CDU/CSU",
    "fdp": "FDP",
    "spd": "SPD",
    "bündnis 90/die grünen": "Bündnis 90/Die Grünen",
    "die linke": "Die Linke",
    "bsw": "BSW",
    "fraktionslos": "Fraktionslose & Andere",
    "bundes": "Mitglieder der Bundesregierung u. Sonstige"
}

fraktion_color_map = {
    "afd": "blue",
    "cdu/csu": "black",
    "fdp": "yellow",
    "spd": "red",
    "bündnis 90/die grünen": "green",
    "die linke": "pink",
    "bsw": "purple",
    "fraktionslos": "grey",
    "bundes": "orange"
}

data = data[tags.isin(valid_tags)]
tags = data[0].reset_index(drop=True)
redner_fraktionen_lower = data[6].str.lower().reset_index(drop=True)
total_contributions = len(tags)
fig, axes = plt.subplots(1, 3, figsize=(15, 10))
axes = axes.flatten()

for i, tag in enumerate(valid_tags):
    tag_mask = tags == tag
    tag_data = redner_fraktionen_lower[tag_mask]
    fraktion_counts = Counter()
    for fraktion in fraktionen:
        fraktion_counts[fraktion] = sum(tag_data.str.contains(fraktion, na=False))

    total = sum(fraktion_counts.values())
    ax = axes[i]

    if total > 0:
        sizes = [count for fraktion, count in fraktion_counts.items() if count > 0]
        colors = [fraktion_color_map[fraktion] for fraktion, count in fraktion_counts.items() if count > 0]
        labels = [
            f"{fraktion_title_map[fraktion]} ({count / total * 100:.1f}%)"
            for fraktion, count in fraktion_counts.items() if count > 0
        ]

        ax.pie(sizes, labels=None, startangle=90, colors=colors)
        ax.set_title(f'{tag} ({total} Beiträge)')
        ax.axis('equal')

        breakdown = "\n".join(
            f"\u25A0 {fraktion_title_map[fraktion]}: {count / total * 100:.1f}%"
            for fraktion, count in fraktion_counts.items() if count > 0
        )
        ax.legend(wedges, labels, title="Fraktionen", loc="center left", bbox_to_anchor=(0, 0), fontsize=9)
    else:
        ax.text(0.5, 0.5, 'Keine Daten', ha='center', va='center', fontsize=12)
        ax.set_title(f'{tag} (0 Beiträge)')
        ax.axis('off')

fig.suptitle(f'Insgesamt: {total_contributions} Beiträge', fontsize=16, weight='bold')
plt.tight_layout(rect=[0, 0, 1, 0.92])
plt.show()