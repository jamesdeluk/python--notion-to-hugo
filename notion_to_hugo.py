#!/usr/bin/env python

# for Windows, cwd
# to do: subdirectories

import glob
import os
import shutil
import re
from urllib.parse import unquote

# collect files
files = glob.glob('*.md')
print(f'{len(files)} files')
# files_l1 = glob.glob('*', recursive=True)
# print(files_l1)
# files_l2 = []
# for f in files_l1:
#     print(f)
#     files_l2.append(glob.glob(f'{f}/*', recursive=True))
# print(files_l2)

# # using pathlib
# from pathlib import Path
# print(Path('.').rglob('*'))

# create file to store processed file in
try:
    os.mkdir('processed')
except:
    'file already exists'
try:
    os.mkdir('processed/img')
except:
    'file already exists'

# loop through files
counter = 1
for f in files:
    # extract filename, removing notion note ID
    title = f.split('\\')[-1][:-3]
    title = '-'.join(title.split(' ')[:-1])
    filename = title.lower()
    print(f'({counter}) {filename}.md')

    # open file
    with open(f'{f}', 'r', encoding="utf8") as original: data = original.readlines()
    
    # header
    header_line = f'---\n'
    data.insert(0,header_line)
    data[1] = f"title: '{data[1][2:].rstrip()}'\n"
    data.insert(2,header_line)

    # internal links
    print('\n=== Internal Links ===')
    for line in data:
        regex1 = r'\[.*\]\(.*\)' # all links
        regex2 = r'\[.*\]\(.*\.md\)' # markdown files - likely internal
        regex3 = r'\[.*\]\(http.*\)' # external links
        if re.match(regex1,line):
            if re.match(regex2,line):
                print(f'{line.rstrip()}')
            elif re.match(regex3,line):
                pass
            else:
                print(f'{line.rstrip()}')

    # images
    print('\n=== Images ===')
    img_count = 0
    line_id = 0
    for line in data:
        regex_img = r'!\[.*\]\(.*\)'
        if re.match(regex_img,line):
            print(line.strip())
            img_count += 1
            img_path = unquote(line.replace('[','|').replace(']','|').split('|')[1])
            filetype = img_path.split('.')[-1]
            img_new_name = f'img{img_count}'
            shutil.copy(img_path, f'processed/img/{img_new_name}.{filetype}')
            data[line_id] = f'![{img_new_name}](img/{img_new_name})\n'
        line_id += 1

    # toc
    toc = []
    for line in data:
        split = line.split(' ')
        if split[0] == '##':
            first = " ".join(split[1:]).strip()
            second = "-".join(split[1:]).strip().replace('/','').replace('→','').replace('(','').replace(')','').lower()
            toc.append(f'- [{first}](#{second})\n')
        if split[0] == '###':
            first = " ".join(split[1:]).strip()
            second = "-".join(split[1:]).strip().replace('/','').replace('→','').replace('(','').replace(')','').lower()
            toc.append(f'\t- [{first}](#{second})\n')
        if split[0] == '####':
            first = " ".join(split[1:]).strip()
            second = "\t-".join(split[1:]).strip().replace('/','').replace('→','').replace('(','').replace(')','').lower()
            toc.append(f'- [{first}](#{second})\n')
    for c in reversed(toc):
        data.insert(3,c)
    data.insert(3,'\n')

    # save file
    with open(f'processed\\{filename}.md', 'w', encoding="utf8") as modified: modified.writelines(data)
    counter += 1