import pandas as pd
import re

input_file = 'output/dataset-filtered.csv'
output_file = 'output/dataset-extracted.csv'
keywords_regex = r"(migration|flüchtling|asyl|einwanderung|zuwanderung)"
df = pd.read_csv(input_file, header=None, sep='\t', encoding='utf-8')

def extract_unique_snippets(redebeitrag, regex):
    sentences = re.split(r'(?<=[.!?])\s+', redebeitrag)
    unique_snippets = set()

    for sentence in sentences:
        if re.search(regex, sentence, re.IGNORECASE):
            unique_snippets.add(sentence.strip())

    return " | ".join(unique_snippets) if unique_snippets else None

df['Ausschnitt'] = df[4].apply(lambda x: extract_unique_snippets(x, keywords_regex))
df.to_csv(output_file, index=False, header=False, sep='\t', encoding='utf-8')