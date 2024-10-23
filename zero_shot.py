#!pip install transformers
#!pip install tf-keras

use_cuda=True

import re
from datetime import datetime
from transformers import pipeline

filename = '/Users/felix/Desktop/bundestag_XMLparser/out/output_migration.csv'

corpus = []
comments = []
with open(filename, "r") as file_content:
    for line in file_content.readlines():
        line = line.strip()
        cells = line.split('\t')
        if len(cells) < 4:
            continue
        text = cells[4]
        corpus.append(line)
        comments.append(text)

labels_thema = ['Migration']
labels_standpunkt = ['Kriminelle', 'Nützliche', 'Kostenintensive', 'Integrationswillige', 'Willkommene']
classifier = pipeline("zero-shot-classification", model="joeddav/xlm-roberta-large-xnli")

for k, comment in enumerate(comments):
    out = classifier(comment, labels_thema)
    highest_score = 0
    score_for_migration = 0
    highest_label = '-'
    scores = out['scores']

    for i, score in enumerate(scores):
        if out['labels'][i] == 'Migration':
            score_for_migration = score
        if score > highest_score:
            highest_score = score
            highest_label = out['labels'][i]

    print_line = highest_label+'\t'+str(highest_score)+'\t'+str(score_for_migration)

    if (highest_label == 'Migration'):
        out = classifier(comment, labels_standpunkt)
        highest_score = 0
        highest_label = '-'
        scores = out['scores']

        for i, score in enumerate(scores):
            if score > highest_score:
                highest_score = score
                highest_label = out['labels'][i]
                print_line += '\t'+highest_label+'\t'+str(highest_score)
    else:
        print_line += '\t - \t - '

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print_line += '\t'+str(now)
    print_line += '\t'+corpus[k]+'\n'
    print (print_line)

    with open('/Users/felix/Desktop/output_migration-annotated.csv', 'a') as writefile:
        writefile.write(print_line)
