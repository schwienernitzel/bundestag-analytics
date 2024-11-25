from datetime import datetime
from transformers import pipeline

filename_input = '/Users/felix/Desktop/bundestag-analytics/output/dataset-extracted-241124.csv'
filename_output = '/Users/felix/Desktop/bundestag-analytics/output/dataset-annotated-241124.csv'

labels_standpunkt = ['Kriminelle', 'Kostenintensive', 'Willkommene', 'Nutzbringende']
classifier = pipeline("zero-shot-classification", model="joeddav/xlm-roberta-large-xnli")

processed_ids = set()
try:
    with open(filename_output, "r") as output_file:
        for line in output_file:
            cells = line.strip().split('\t')
            if len(cells) >= 6:
                processed_ids.add(cells[5])
except FileNotFoundError:
    print(f"Ausgabedatei {filename_output} existiert noch nicht. Beginne bei Zeile 0.")

corpus = []
comments = []
with open(filename_input, "r") as file_content:
    for line in file_content:
        cells = line.strip().split('\t')
        if len(cells) < 4:
            continue
        unique_id = cells[2]
        text = cells[5]
        if unique_id not in processed_ids:
            corpus.append(line)
            comments.append((unique_id, text))

for k, (unique_id, comment) in enumerate(comments):
    try:
        out = classifier(comment, labels_standpunkt)
        highest_score = 0
        highest_label = '-'
        scores = out['scores']

        for i, score in enumerate(scores):
            if score > highest_score:
                highest_score = score
                highest_label = out['labels'][i]

        print_line = highest_label + '\t' + str(highest_score)
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print_line += '\t' + str(now)
        print_line += '\t' + corpus[k]

        with open(filename_output, 'a') as writefile:
            writefile.write(print_line)
        print(print_line)
    except Exception as e:
        print(f"Fehler bei Kommentar {k} mit ID {unique_id}: {e}. Fortsetzen...")
