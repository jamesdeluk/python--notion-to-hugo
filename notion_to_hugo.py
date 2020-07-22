#!/usr/bin/env python

# to do: privatise IPs, delete empty folders, fix /img rename, move to processed folder, deal with top-level file, check linux compatibility

import glob
import os
from pathlib import Path
import shutil
import re
from urllib.parse import unquote

# loop through files
def process_file(f):
    # extract filename, removing notion note ID
    f = str(f)
    path = '\\'.join(f.split('\\')[:-1])
    title = f.split('\\')[-1][:-3]
    title = '-'.join(title.split(' ')[:-1])
    filename = title.lower()

    # open file
    with open(f'{f}', 'r', encoding="utf8") as original: data = original.readlines()
    
    # header
    header_line = f'---\n'
    data.insert(0,header_line)
    data[1] = f"title: '{data[1][2:].rstrip()}'\n"
    data.insert(2,header_line)

    # internal links
    print('=== Internal Links ===')
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
    print('=== Images ===')
    img_count = 0
    line_id = 0
    for line in data:
        regex_img_http = r'!\[.*\]\(http.*\)'
        regex_img = r'!\[.*\]\(.*\)'
        if re.match(regex_img_http,line):
            print(f'External image: {line.strip()}')
            continue
        elif re.match(regex_img,line):
            try:
                os.mkdir(f'{path}/img')
            except:
                pass
            print(line.strip())
            img_count += 1
            img_path = unquote(line.replace('[','|').replace(']','|').split('|')[1])
            filetype = img_path.split('.')[-1]
            img_new_name = f'{filename}_img{img_count}'
            shutil.copy(f'{path}/{img_path}', f'{path}/img/{img_new_name}.{filetype}')
            os.remove(f'{path}/{img_path}')
            data[line_id] = f'![{img_new_name}](img/{img_new_name}.{filetype})\n'
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
    with open(f'{path}/{filename}.md', 'w', encoding="utf8") as modified: modified.writelines(data)

    # delete original
    os.remove(f)
# end def

# process files
for md in Path(".").glob("**/*.md"):
    print(f'{md}')
    process_file(md)

# rename folders
for path in Path(".").glob("**/*"):
    if path.is_dir():
        if '/img' in str(path):
            print(path)
        else:
            target = path.parent / " ".join(path.name.split()[:-1]).lower()
            try:
                path.rename(target)
            except:
                print(f'Failed to rename {path} to {target}')