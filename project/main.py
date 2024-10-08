'''
1) Есть json-файлы с распарсенными книгами (папка json), из них нужно выделить все уникальные ТУ и всех уникальных 
производителей. По ТУ берутся из каждого файла элементы с типом "element", во всех файлах в поле data ТУ 
стоят третьи элементом. Нужно вытащить эти ТУ в общий список. (У одного элемента может быть несколько ТУ, 
тогда они разделены точкой с запятой, в таком случае их вытаскивать как два различных ТУ)
По производителям - это элементы с типом "mnf", почти всегда это вторая строка в data, кроме ликвидированных 
предприятий (последний элемент). Также надо будет сделать список уникальных предприятий из всех книг в одном 
файле. Причем это должен быть скрипт, который "съедает" на входе все эти файлы, и на выходе выдает два файла 
(можно просто txt/csv) со списком УНИКАЛЬНЫХ имен

2) Не все ТУ/производители распарсены правильно. Поэтому необходимо сделать следующее: просмотреть оба 
получившихся списка. Если есть ошибки (условно два ТУ не разделены точкой с запятой), тогда залезть в исходные 
файлы, руками исправить, после чего заново запустить скрипт и убедиться, что все нормально работает

3) После полной проверки и исправления списков ТУ и производителей, отправить следующие файлы: сами списки ТУ 
и производителей + исправленные json'ы
'''

import os
import json

tu, mf = [], []
files = os.listdir('./json')

for file in files:
    with open('./json/' + file, 'r',  encoding='utf-8') as f:
        data = json.load(f)
    for i in data:
        if i['type'] == 'element':
            # if (" " in i['data'][2].strip() or ',' in i['data'][2]) and ';' not in i['data'][2]:
            #     print(i['data'][2], file)
            tus = list(map(str.strip, i['data'][2].split(';')))
            tu.extend(tus)
        elif i['type'] == 'mnf':
            mf.append(i['data'][1].strip())

with open('tu.txt', 'w', encoding='utf-8') as f:
    print(*sorted(set(tu)), sep='\n', file=f)

with open('mf.txt', 'w', encoding='utf-8') as f:
    print(*sorted(set(mf)), sep='\n', file=f)
