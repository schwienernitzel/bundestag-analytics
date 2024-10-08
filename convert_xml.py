from sys import argv
from sys import stderr
import re

def main(filename):
    content = get_content(filename)

    redner = '-'
    partei = '-'
    rede_id = '-'
    rede = []
    datum = '-'
    print_text = ''

    for i, line in enumerate(content):
        line = re.sub('[\s]+', ' ', line)

        if re.search('sitzung-datum', line):
            datum = re.sub('.*sitzung-datum="([^"]+)".*', r'\1', line)

        if re.search('<p', line) and not re.search('<vorname>', line):
            absatz = re.sub("<[^>]*>", '', line)
            absatz = absatz.strip()
            rede.append(absatz)

        if re.search('<redner', line) and re.search('rede id', content[i-1]):
            redner = re.sub('.*/redner>([^<]+).*', r'\1', line)
            redner = re.sub(':', '', redner)
            redner = redner.strip()

        if re.search('<fraktion>.*</fraktion>', line) and re.search('rede id', content[i-1]):
            partei = re.sub('.*<fraktion>(.*)</fraktion>.*', r'\1', line)

        if re.search('<rolle_kurz>.*</rolle_kurz>', line) and re.search('rede id', content[i-1]):
            partei = re.sub('.*<rolle_kurz>(.*)</rolle_kurz>.*', r'\1', line)

        if re.search("rede id=", line) and rede_id == '-':
            rede_id = re.sub('.*rede id="([^"]+)".*', r'\1', line)

        if re.search('rede id', line) or re.search('<sitzungsende', line):
            gesamte_rede = ' ## '.join(rede)
            print_text += '\n'+rede_id+'\t'+redner+'\t'+partei+'\t'+datum+'\t'+gesamte_rede
            redner = '-'
            rede = []
            rede_id = re.sub('.*rede id="([^"]+)".*', r'\1', line)

        if re.search('<sitzungsende', line):
            break
        
    print (print_text)
    pass

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