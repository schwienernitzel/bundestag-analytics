#!/usr/bin/python
# -*- coding: utf-8 -*-


 
"""
Usage: python3 convert_xml.py 20189.xml
Datum: Okt 2024
Zweck:
"""



from sys import argv
from sys import stderr
import re



# Main
def main(filename):

    # Text lesen
    content = get_content(filename)


    redner = '-'
    partei = '-'
    rede_id = '-'
    rede = []
    datum = '-'
    print_text = ''

    
    for i, line in enumerate(content):

        # Tabulatoren entfernen
        line = re.sub('[\s]+', ' ', line)

        # Metadaten in der XML-Datei sammeln:

        # Datum. Format: sitzung-datum="27.09.2024"
        if re.search('sitzung-datum', line):
            datum = re.sub('.*sitzung-datum="([^"]+)".*', r'\1', line)

        # Texte. Format: <p klasse="O">Für diese Menschen ist das Ganze eine Rentenkürzung...
        if re.search('<p', line) and not re.search('<vorname>', line):
            absatz = re.sub("<[^>]*>", '', line)
            absatz = absatz.strip()
            rede.append(absatz)

        # Redner. Format: </redner>Helmut Kleebank (SPD):</p>
        if re.search('<redner', line) and re.search('rede id', content[i-1]):
            redner = re.sub('.*/redner>([^<]+).*', r'\1', line)
            redner = re.sub(':', '', redner)
            redner = redner.strip()

        # Partei. Format: <fraktion>SPD</fraktion>
        if re.search('<fraktion>.*</fraktion>', line) and re.search('rede id', content[i-1]):
            partei = re.sub('.*<fraktion>(.*)</fraktion>.*', r'\1', line)

        if re.search('<rolle_kurz>.*</rolle_kurz>', line) and re.search('rede id', content[i-1]):
            partei = re.sub('.*<rolle_kurz>(.*)</rolle_kurz>.*', r'\1', line)

        if re.search("rede id=", line) and rede_id == '-':
            rede_id = re.sub('.*rede id="([^"]+)".*', r'\1', line)





        # Das Ende einer Rede wurde erreicht. 
        # Entweder, weil die nächste beginnt (neue rede_id), 
        # oder weil am Textende '<sitzungsende' gefunden wird
        if re.search('rede id', line) or re.search('<sitzungsende', line):

            gesamte_rede = ' ## '.join(rede)
            
            print_text += '\n'+rede_id+'\t'+redner+'\t'+partei+'\t'+datum+'\t'+gesamte_rede

            # ID der nächsten Rede festhalten
            redner = '-'
            rede = []
            rede_id = re.sub('.*rede id="([^"]+)".*', r'\1', line)

        
    print (print_text)
    
    pass



# Datei in Liste
def get_content(filename):
    content = []
    with open(filename, "r") as file_content:
        for line in file_content.readlines():
            line = line.strip()
            content.append(line)           
    return content



if __name__ == '__main__':
    if len(argv) == 2:
        main(argv[1])
    else:
        stderr.write("Error: Wrong number of arguments.\n")

