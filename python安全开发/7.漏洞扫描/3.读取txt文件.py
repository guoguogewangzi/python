


url_file='url.txt'

with open(url_file,encoding='utf-8') as f:
    data = f.readlines()
    for i in data:
        url=i.split('\n')[0]
        print(url)