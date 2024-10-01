'''
Необходимо сделать json со списком всех ЭКБ в следующем виде:
{
    "ekbName": "Название ЭКБ", 
    "tuName": ["Первое", "Второе", ...], 
    "manufacturerName": тоже список производителей текстом
}
Элементы разделены в файлы по title и каждый файл лежит в папке с названием книги, 
в которой были соответсвующие элементы.

Результат лежит в папке data
'''

import os
import json
import re

files = os.listdir('./json')
if not os.path.isdir("./data"):
    os.mkdir('./data')

for file in files:
    with open('./json/' + file, 'r',  encoding='utf-8') as f:
        data = json.load(f)
    if not os.path.isdir("./data/" + file):
        os.mkdir('./data/' + file)
    dict_mnf = {}
    for i in data:
        if i['type'] == 'mnf':
            dict_mnf[i['data'][0].strip()] = i['data'][1].strip()
    i = 0
    c = 0
    file_name = ''
    res = []
    while i < len(data):
        c += 1
        dict_ekb = {'ekbName': '', 'tuName': [], 'manufacturerName': []}
        if data[i]['type'] == 'title':
            if c != 1:
                file_name = file_name.strip('_')
                res_name = './data/' + file + '/' + file_name + '.json'
                with open(res_name, 'w', encoding='utf-8') as f:
                    json.dump(res, f, ensure_ascii=False, indent=4)
                file_name = ''
                res = []
            while data[i]['type'] == 'title':
                file_name += data[i]['data'][0].split()[0] + '_'
                i += 1
        if data[i]['type'] == 'element':
            dict_ekb['ekbName'] = data[i]['data'][1].strip()
            tu = list(map(str.strip, data[i]['data'][2].split(';')))
            dict_ekb['tuName'].extend(tu)
            # print(file)
            # print(data[i]['data'][4])
            mnf = list(map(str.strip, re.split(';|,', data[i]['data'][4].split('/')[0])))
            for j in range(len(mnf)):
                if (file == 'Часть 18 Книга 2_диск.json') and (mnf[j] == '17'):
                    dict_mnf['17'] = 'РАДАР ММС'
                mnf[j] = dict_mnf[mnf[j]]
            dict_ekb['manufacturerName'].extend(mnf)
            res.append(dict_ekb)
        if i == len(data) - 1:
            file_name = file_name.strip('_')
            res_name = './data/' + file + '/' + file_name + '.json'
            with open(res_name, 'w', encoding='utf-8') as f:
                json.dump(res, f, ensure_ascii=False, indent=4)
        i += 1
