# for Windows, cwd

import glob
import os
import re

# create file to store processed file in
try:
    processed = os.mkdir('processed')
except:
    'file already exists'

# collect files
files = glob.glob(f'*.md')
print(f'{len(files)} files')
# loop through files
counter = 1
for file in files:
    # extract filename, removing notion note ID
    title = file.split('\\')[-1][:-3]
    title = '-'.join(title.split(' ')[:-1])
    filename = title.lower()
    print(f'({counter}) {filename}.md')

    # open file
    with open(f'{file}', 'r', encoding="utf8") as original: data = original.readlines()
    
    # header
    header_line = f'---\n'
    data.insert(0,header_line)
    data[1] = f"title: '{data[1][2:].rstrip()}'\n"
    data.insert(2,header_line)

    # internal links
    for line in data:
        regex1 = '\[.*\]\(.*\)' # all links
        regex2 = '\[.*\]\(.*\.md\)' # markdown files - likely internal
        regex3 = '\[.*\]\(http.*\)' # external links
        if re.match(regex1,line):
            if re.match(regex2,line):
                print(f'------ {line.rstrip()}')
            elif re.match(regex3,line):
                pass
            else:
                print(f'------ {line.rstrip()}')

    # toc
    toc = []
    for line in data:
        split = line.split(' ')
        if split[0] == '##':
            first = " ".join(split[1:]).strip()
            second = "-".join(split[1:]).strip().replace('/','').lower()
            toc.append(f'- [{first}](#{second})\n')
        if split[0] == '###':
            first = " ".join(split[1:]).strip()
            second = "-".join(split[1:]).strip().replace('/','').lower()
            toc.append(f'\t- [{first}](#{second})\n')
        if split[0] == '####':
            first = " ".join(split[1:]).strip()
            second = "\t-".join(split[1:]).strip().replace('/','').lower()
            toc.append(f'- [{first}](#{second})\n')
    for c in reversed(toc):
        data.insert(3,c)
    data.insert(3,'\n')

    # save file
    with open(f'processed\\{filename}.md', 'w', encoding="utf8") as modified: modified.writelines(data)
    counter += 1