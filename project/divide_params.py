'''
Есть настройка секций (папка new_parser_settings), какой столбец соответствует какому Id параметра. 
Нужно сделать программу, которая создаст такой файл:
[
{"Name": "Eri1",
" Parameters":
{
"5": ["первое значение разделенного параметра", "второе значение разделенного параметра", ..],
...}
},
...
]
Такие файлы должны быть для каждой категории, как с именами и ТУ, 
но при этом файлы шаблонов даны на секцию (промежуток между двумя subtitle)

результат хранится в data_params
'''

import os
import json
import re
import sys

# функция для вытаскивания нужного парметра по цифре
def check_params(number):
    if number in l:
        # это индекс в файлах настроек
        index = int(number) - 1
        l_splitted = l.split(our_splitter)
        l_splitted[-1] = l_splitted[-1].replace(')', '')
        while '' in l_splitted:
            l_splitted.remove('')
        print(l_splitted, 'splitter=', our_splitter)
        data_index = l_splitted.index(number)
        # тут проверяю есть ли вообще настройка для нашего параметра
        if len(data_params[k]['HierarchicalParameters']) >= index + 1:
            id = data_params[k]['HierarchicalParameters'][index]['Parameter']['LinkedInparId']
            dict_ekb['Parameters'][id] = [cur_param[data_index]]
        # если не нашлось, то ищу ее в subparameters
        elif len(data_params[k]['HierarchicalParameters'][-1]['SubParameters']) > 0: 
            if len(data_params[k]['HierarchicalParameters'][index - 1]['SubParameters']) >= index:
                id = data_params[k]['HierarchicalParameters'][index - 1]['SubParameters'][0]['LinkedInparId']
                dict_ekb['Parameters'][id] = [cur_param[data_index]]
        else:
            with open('errors.txt', 'a', encoding = 'utf-8') as f:
                f.write(f'Файл {file}, настройка {j[:25]}, LinkedInparId для параметра {cur_param} элемента {dict_ekb["Name"]} не нашелся\n')

# список всех файлов json
files = sorted(os.listdir('./json'))
# список всех файлов с настройками парсера
files_params = os.listdir('./new_parser_settings')
# здесь создаю папку куда буду записывать результат
if not os.path.isdir("./data_params"):
    os.mkdir('./data_params')

# здесь чищу файл ошибок
with open('errors.txt', 'w', encoding = 'utf-8') as f:
    pass
all_templates = set()
for file in files:
    # оставляю только основное название как в настройках парсера
    file_cut = file.split('_')[0]
    # здесь пропускается часть 1 так как для нее нет настроек
    if file_cut not in files_params:
        continue
    # папка текущей книги куда будут записываться результирующие файлы
    curr_file_path = "./data_params/" + file.split('.')[0]
    # здесь создается эта папка
    if not os.path.isdir(curr_file_path):
        os.mkdir(curr_file_path)
    # здесь обращаемся к папке текущей книги с настройками парсера
    res_path_params = './new_parser_settings/' + file_cut
    # берем список всех файлов оттуда
    files_params_names = os.listdir(res_path_params)
    # загружаю текущую книгу json
    with open('./json/' + file, 'r',  encoding='utf-8') as f:
        data = json.load(f)

    i, c = 0, 0
    file_name = ''
    res = []

    while i < len(data):

        c += 1
        dict_ekb = {'Name': '', "Parameters": {}}

        if data[i]['type'] == 'title':

            if c != 1:
                file_name = file_name.strip('_')
                # загружаем элементы одного блока в итоговый файл
                res_name = curr_file_path + '/' + file_name + '.json'

                with open(res_name, 'w', encoding='utf-8') as f:
                    json.dump(res, f, ensure_ascii=False, indent=4)

                file_name = ''
                res = []

            # формируем название итого файла из тайтлов
            while data[i]['type'] == 'title':
                file_name += data[i]['data'][0].split()[0] + '_'
                i += 1
            data_params = None

            # ищем нужный файл настроек парсера и читаем его
            for j in files_params_names:
                setting_titles = j.split('_')
                if any([x in setting_titles for x in file_name.strip('_').split('_')]):
                    if 'Раздел 1' in file:
                        if ('раздел1' in j) or ('раздел2' not in j):
                            with open(res_path_params + '/' + j, 'r',  encoding='utf-8') as f:
                                data_params = json.load(f) 
                            break
                    elif 'Раздел 2' in file:
                        if ('раздел2' in j) or ('раздел1' not in j):
                            with open(res_path_params + '/' + j, 'r',  encoding='utf-8') as f:
                                data_params = json.load(f) 
                            break
                    else:
                        with open(res_path_params + '/' + j, 'r',  encoding='utf-8') as f:
                            data_params = json.load(f) 
                        break
            # если не нашли нужный, пишем в файл ошибок
            if data_params == None:
                with open('errors.txt', 'a', encoding = 'utf-8') as f:
                    f.write(f'Файл {file}, ни одного из элементов группы {file_name} нет в настройках парсинга\n')    

        if data[i]['type'] == 'element':
            if data_params:
                dict_ekb['Name'] = data[i]['data'][1].strip()
                for k in range(min(len(data_params), len(data[i]['data'][5:]))):

                    if data_params[k]['HierarchicalParameters']:
                        parser_string = data_params[k]['ParserString'].split("=")[0].split("|")
                        parser_template = {}
                        # здесь обрабатываю все шаблоны и формирую словарь изначальный шаблон:регулярка
                        for s in parser_string:
                            s = s.strip()
                            cur_num = s
                            for r in ['1', '2', '3', '4', '5']:
                                cur_num = cur_num.replace(r, '.+')
                            parser_template[s] = cur_num
                        # здесь удаляю шаблон -, так как обрабатываем его отдельно
                        if '-' in parser_template:
                            parser_template.pop('-')
                        # подготавливаю текущие данные
                        cur_param = data[i]['data'][k+5].strip()
                        print('Файл', file, ', итоговый файл', file_name, ', настройка парсера', j[:25])
                        print('Настройки парсера', parser_template, ', текущий параметр:', cur_param)
                        if (cur_param == '-') or (cur_param == ''):
                            continue
                        else:
                            # флаг на то есть ли шаблон 1 в текущей parser string
                            is_1 = 0
                            is_2 = 0
                            if '1' in parser_template:
                                is_1 = 1
                                # удаляю пока шаблон 1 чтобы по нему сразу не парсились все данные
                                parser_template.pop('1')
                            if '/2/' in parser_template:
                                is_2 = 1
                                # удаляю пока шаблон /2/ чтобы по нему сразу не парсились данные которые подходят под шаблон 1/2/
                                parser_template.pop('/2/')
                            f = 0
                            for l in parser_template:
                                all_templates.add(l)
                                if re.search(parser_template[l], cur_param):
                                    # этот шаблон не обрабатываю
                                    if l == '1(2);':
                                        with open('errors.txt', 'a', encoding = 'utf-8') as f:
                                            f.write(f'Файл {file}, настройка {j[:25]}, шаблон {l} имеет всего один параметр в настройках парсера\n')
                                    else:
                                        f = 1
                                        # здесь избегаю случаев когда шаблон 1(2), а его регулярка .+(.+)
                                        # по такой регулярке проходят любые данные, в том числе и вообще без скобок
                                        if '(' in l and '(' not in cur_param:
                                            continue
                                        # здесь обхожу случаи когда шаблон 1(2), а данные например (3.1)
                                        if '(' in l and (cur_param[0] == '('):
                                            with open('errors.txt', 'a', encoding = 'utf-8') as f:
                                                f.write(f'Файл {file}, настройка {j[:25]}, параметр {cur_param} элемента {dict_ekb["Name"]} пытается парситься по шаблону {parser_template[l]}\n') 
                                            continue
                                        # здесь разделяю наши данные по разделителю из шаблона
                                        for splitter in "(/,;&×:":
                                            if splitter in l:
                                                our_splitter = splitter
                                                cur_param = cur_param.split(splitter)
                                                cur_param[-1] = cur_param[-1].replace(')', '')
                                                # здесь удаляю пустые строки, образовавшиеся в списках после сплитовки
                                                while '' in cur_param:
                                                    cur_param.remove('')
                                        print('Шаблон:', l)
                                        print('Текущий параметр:', cur_param)
                                        # здесь начинаю обрабатывать параметр 1
                                        if '1' in l:
                                            id = data_params[k]['HierarchicalParameters'][0]['Parameter']['LinkedInparId']
                                            if '2' in l or '3' in l or '4' in l or '5' in l:
                                                l_splitted = l.split(our_splitter)
                                                for sp in range(len(l_splitted)):
                                                    l_splitted[sp] = l_splitted[sp].strip()
                                                l_splitted[-1] = l_splitted[-1].replace(')', '')
                                                while '' in l_splitted:
                                                    l_splitted.remove('')
                                                print(l_splitted, 'splitter=', our_splitter)
                                                data_index = l_splitted.index('1')
                                                dict_ekb['Parameters'][id] = [cur_param[data_index]]
                                            else:
                                                dict_ekb['Parameters'][id] = cur_param
                                        # здесь обрабатываю параметры 2-5
                                        for nums in ['2', '3', '4', '5']:
                                            check_params(nums)
                                    break
                            # тут уже если остальные шаблоны не подошли и у нас был шаблон /2/, то парсим по нему
                            if is_2 == 1:
                                parser_template['/2/'] = '/.+/'
                                if f == 0 and '/' in cur_param:
                                    f = 1
                                    print('Шаблон: /2/')
                                    if len(data_params[k]['HierarchicalParameters']) >= 2:
                                        id = data_params[k]['HierarchicalParameters'][1]['Parameter']['LinkedInparId']
                                        dict_ekb['Parameters'][id] = [cur_param.replace('/', '')]
                                    else:
                                        with open('errors.txt', 'a', encoding = 'utf-8') as f:
                                            f.write(f'Файл {file}, элемент {dict_ekb["Name"]}, настройка {j[:25]}, шаблон /2/ для параметра {cur_param} имеет недостаточно параметров в настройках парсера\n')
                            # тут уже если остальные шаблоны не подошли и у нас был шаблон 1, то парсим по нему
                            if is_1 == 1:
                                parser_template['1'] = '.+'
                                if f == 0:
                                    f = 1
                                    print('Шаблон: 1')
                                    id = data_params[k]['HierarchicalParameters'][0]['Parameter']['LinkedInparId']
                                    dict_ekb['Parameters'][id] = [cur_param]
                            print(dict_ekb)
                            print()
                            if f == 0:
                                with open('errors.txt', 'a', encoding = 'utf-8') as f:
                                    f.write(f'Файл {file}, настройка {j[:25]}, параметр {cur_param} элемента {dict_ekb["Name"]} не распрарсился по шаблону {parser_template}\n') 
                    else:
                        with open('errors.txt', 'a', encoding = 'utf-8') as f:
                            f.write(f'Файл {file}, в {j[:25]} пустые Hierarchical Parameters для элемента {dict_ekb["Name"]} и его параметра {cur_param}\n')
                res.append(dict_ekb)

        if i == len(data) - 1:
            file_name = file_name.strip('_')
            res_name = curr_file_path + '/' + file_name + '.json'

            with open(res_name, 'w', encoding='utf-8') as f:
                json.dump(res, f, ensure_ascii=False, indent=4)

        i += 1


print(all_templates)