#!/usr/bin/env python

import yaml
from string import Template

vars = {
    'Languages': '',
    'TechStack': '',
    'DevOps': '',
    'Tools': '',
}

temp_vars = vars.copy()

with open('.github/Cards.yml', encoding="utf8") as cards:
    rows = yaml.load_all(cards, Loader=yaml.FullLoader)
    for x in rows:
        for k, v in x.items():
            temp_vars[k] = v

for key in temp_vars:
    print(temp_vars[key])
    for lang in temp_vars[key]:
        logo = temp_vars[key][lang] if temp_vars[key][lang] else lang
        vars[key] += f"![{lang}](https://img.shields.io/badge/-{lang}-black?style=flat-square&logo={logo.lower()}) "

with open('.github/TEMPLATE.md', 'r', encoding="utf8") as TM_MD:
    src = Template(TM_MD.read())
    result = src.substitute(vars)
    with open('README.md', 'w', encoding="utf8") as readme:
        readme.write(result)
