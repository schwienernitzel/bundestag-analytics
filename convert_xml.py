from sys import argv
from sys import stderr
import re

def main(filename):
    content = get_content(filename)
    redner = '-'
    rede_id = '-'
    rede = []
    datum = '-'
    print_text = ''
    rede_aktiv = False
    redner_aktiv = False

    for i, line in enumerate(content):
        line = re.sub('[\s]+', ' ', line)
        if re.search('sitzung-datum', line):
            datum = re.sub('.*sitzung-datum="([^"]+)".*', r'\1', line)
        if re.search('<p', line)  and not re.search('<vorname>', line) or rede_aktiv:
            absatz = re.sub("<[^>]*>", '', line).strip()
            if absatz:
                rede.append(absatz)
                rede_aktiv = True
            if re.search('</p>', line):
                rede_aktiv = False
        if re.search('</redner>', line) or redner_aktiv:
            if not redner_aktiv:
                redner = re.sub('.*/redner>([^<]*).*', r'\1', line).strip()
                redner_aktiv = True
            else:
                line = re.sub('<[^>]*>', '', line).strip()
                redner += ' ' + line
            if ':' in line:
                redner = re.sub(':', '', redner).strip()
                redner_aktiv = False
        if re.search('rede id', line) or re.search('<sitzungsende', line):
            gesamte_rede = ' ## '.join(rede)
            print_text += '\n'+rede_id+'\t'+datum+'\t'+redner+'\t'+gesamte_rede
            redner = '-'
            rede = []
            rede_id = re.sub('.*rede id="([^"]+)".*', r'\1', line)
        if re.search('<sitzungsende', line):
            break

    print_text = remove_first_line(print_text)
    print (print_text)
    pass

def get_content(filename):
    content = []
    with open(filename, "r") as file_content:
        for line in file_content.readlines():
            line = line.strip()
            content.append(line)
    return content

def remove_first_line(text):
    lines = text.strip().split('\n')
    return '\n'.join(lines[1:]) if len(lines) > 1 else ''

if __name__ == '__main__':
    if len(argv) == 2:
        main(argv[1])
    else:
        stderr.write("Error: Wrong number of arguments.\n")