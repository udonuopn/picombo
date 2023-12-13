#!/bin/env python

import picombo


def read_demo_list():
    items = []
    with open('demo_list.txt', 'r') as f:
        for i in f:
            items.append(i.strip())
    return items


if __name__ == '__main__':
    search_items = read_demo_list()
    pw = picombo.PickWindow(search_items)
    result = pw.search()
    print(result)