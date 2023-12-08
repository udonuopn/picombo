from main import SearchWindow


def read_demo_list():
    items = []
    with open('demo_list.txt', 'r') as f:
        for i in f:
            items.append(i.strip())
    return items


if __name__ == '__main__':
    search_items = read_demo_list()
    sw = SearchWindow(search_items)
    result = sw.search()
    print(result)