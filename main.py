import openpyxl
import csv

# ДОБАВЬ СЛУЧАЙ С ТИПОМ CL-ST

fot_tarif_name = 'samara_tarif.xlsx'
zmat_list_name = 'ZMAT_LIST.xlsx'
zfortest_name = 'ZFORTEST.xlsx'

def read_xslx(file):
    csv_data = list()
    xlsx = openpyxl.load_workbook(file)
    sheet = xlsx.active
    data = sheet.rows
    for row in data:
        l = list([el.value for el in row])
        csv_data.append(l)
    return csv_data

def parce_tarifs_naming(arrs):
    flag_names = False
    dicts = []
    for raw in arrs:
        if not flag_names:
            raw = raw[4:]
            codes = []
            for name in raw:
                name = name.split('[')[1].replace(',','.')
                s = name.find(']')
                if s == -1:
                    print(f'ошибка парсинга кода тарифа {name}')
                codes.append(name[:s])
            for n in codes:
                n = n.upper()
                n = n.split('-')
                if len(n) == 5:
                    dic = {
                        'z': n[0],
                        'fot': n[1],
                        'type': (n[2],),
                        'tonns': n[3].replace('Т','').replace('T',''),
                        'len': n[4].replace('M','').replace('М',''),
                        'prices': dict()
                    }
                    dicts.append(dic)
                elif len(n) == 6:
                    dic = {
                        'z': n[0],
                        'fot': n[1],
                        'type': (n[2],n[3]),
                        'tonns': n[4].replace('Т','').replace('T',''),
                        'len': n[5].replace('M','').replace('М','')
                    }
                    dicts.append(dic)
                else:
                    print(f'Аномалия кода тарифа {n}')
            flag_names = True
        else:
            counter = 4
            for _dict in dicts:
                x = raw[counter]
                if x is None:
                    counter += 1
                    continue
                _dict['prices'].setdefault(raw[0], dict())
                pr = x
                _dict['prices'][raw[0]].setdefault(raw[2], pr)
                counter += 1

            
    return dicts


zmat_list = read_xslx(zmat_list_name)
fot_tarif = read_xslx(fot_tarif_name)
zfortest = read_xslx(zfortest_name)
tarif_codes = parce_tarifs_naming(fot_tarif)

def parce_mat_names(tarifs, zmat):
    tarif_with_number = []
    for tarif in tarifs:
        for zmat in zmat_list[1:]:
            _type, _tonns, _len, _num = ('GT',), zmat[6], zmat[5], zmat[1]
            if zmat[3] is not None:
                zmat[3] = 'X'
            if zmat[4] is not None:
                zmat[4] = 'X'
            if zmat[3]== 'X' and zmat[4] == 'X':
                _type = ('CL', 'ST')
            elif zmat[3] == 'X':
                _type = ('ST',)
            elif zmat[4] == 'X':
                _type = ('CL',)
            tar_tonns = float(tarif['tonns'])
            tar_len = float(tarif['len'])

            # костыль для 13.5м 20тонн
            if tar_tonns == 20 and tar_len == 13.5:
                tar_len = 12.0

            if float(_tonns) == tar_tonns and float(_len) == tar_len:
                tarif_types_clear = list(tarif['type'])

                # не учитываем ПЦС, ВРФ, Логистику
                while 'SM' in tarif_types_clear:
                    tarif_types_clear.remove('SM')
                while 'LG' in tarif_types_clear:
                    tarif_types_clear.remove('LG')
                while 'PS' in tarif_types_clear:
                    tarif_types_clear.remove('PS')
                if not len(tarif_types_clear):
                    tarif_types_clear =['GT']

                set_tarif_types = set(tarif_types_clear)
                set_zmat_types = set(_type)
                if set_tarif_types == set_zmat_types:
                    tarif.setdefault('numeber', _num)
                    break
        tarif_with_number.append(tarif)
    return tarif_with_number

tarif_types = {
    'LG': 'Логистика', # в таблице согласованных тарифов отсутствует
    'ST': 'Манипулятор',
    'GT': 'Общие условия',
    'CL': 'Сборные',
    'PS': 'ПЦС', # в таблице согласованных тарифов отсутствует
    'SM': 'ВРФ', # в таблице согласованных тарифов отсутствует
}

res = parce_mat_names(tarif_codes, zmat_list)
# {'z': 'Z', 'fot': 'PO1033', 'type': ('GT',), 'tonns': '1.5', 'len': '6', 'numeber': 3000009096}

# получить название листа
# fot_tarif_xlsx = openpyxl.

# получить скрытые листы
for i in res:
    print(i)