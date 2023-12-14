#!/bin/env python

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root.joinpath("src")))

import picombo

def read_demo_list():
    items = []
    with open(Path(project_root.joinpath('demo', 'demo_list.txt')), 'r') as f:
        for i in f:
            items.append(i.strip())
    return items


if __name__ == '__main__':
    search_items = read_demo_list()
    pw = picombo.PickWindow(search_items)
    result = pw.search()
    print(result)