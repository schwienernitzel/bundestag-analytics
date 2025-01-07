use_cuda=True

import re
import pandas as pd
import nltk

from nltk.corpus import stopwords
from HanTa import HanoverTagger as ht
from bertopic import BERTopic

filename = 'output.csv'

print("Downloading NLTK resources...")
nltk.download('stopwords')
nltk.download('punkt')

print("Initializing HanoverTagger...")
tagger = ht.HanoverTagger('morphmodel_ger.pgz')

print(f"Loading data from {filename}...")
content = ''
with open(filename, "r") as file_content:
    for line in file_content.readlines():
        line = line.strip()
        line = re.sub('[\s]+', ' ', line)
        line = line.lower()
        line = re.sub('[^a-zäöüß -]', '', line)

        new_line = ''
        words = nltk.word_tokenize(line)
        tagged_words = tagger.tag_sent(words, taglevel=1)
        for tagged_word in tagged_words:
            lemma = tagged_word[1]
            new_line += ' ' + lemma
        new_line = new_line.strip()
        content += ' ' + new_line
        
print("Data loaded and cleaned.")
content = re.sub('[\s]+', ' ', content)
content = content.strip()
n = 80

print(f"Splitting content into parts of size {n} and removing stopwords...")
parts = [''.join(content[i:i+n]) for i in range(0, len(content), n)]
new_parts = []
german_stopwords = set(stopwords.words('german'))
english_stopwords = set(stopwords.words('english'))
for part in parts:
    word_list = part.split(' ')
    filtered_words = [word for word in word_list if word not in german_stopwords and word not in english_stopwords]
    new_content = ' '.join(filtered_words)
    new_parts.append(new_content)
parts = new_parts
print("Content split and stopwords removed.")

print("Fitting BERTopic model...")
topic_model = BERTopic(language="multilingual", nr_topics=20)
topics, probs = topic_model.fit_transform(parts)
print("BERTopic model fitted.")

print("Visualizing the top topics...")
topic_model.visualize_barchart(top_n_topics=20, n_words=8)
print("Visualization complete.")