import openpyxl
import csv

# ДОБАВЬ СЛУЧАЙ С ТИПОМ CL-ST


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
    # ДОБАВЬ СЛУЧАЙ С ТИПОМ CL-ST
    raw = arrs[4:]
    codes = []
    for name in raw:
        name = name.split('[')[1]
        s = name.find(']')
        if s == -1:
            print(f'ошибка парсинга кода тарифа {name}')
        codes.append(name[:s])
    dicts = []
    for n in codes:
        n = n.upper()
        n = n.split('-')
        dic = {
            'z': n[0],
            'fot': n[1],
            'type': n[2],
            'tonns': n[3].replace('Т','').replace('T',''),
            'len': n[4].replace('M','').replace('М','')
        }
        dicts.append(dic)

            
    return dicts


zmat_list = read_xslx('ZMAT_LIST.xlsx')
surgut_tarif = read_xslx('Surgut_tarif.xlsx')
zfortest = read_xslx('ZFORTEST.xlsx')
tarif_codes = parce_tarifs_naming(surgut_tarif[0])

def parce_mat_names(farifs, zmat):
    for tarif in farifs:
        for zmat in zmat_list:
            _z, _type, _tonns, _len, _num = 'Z', [], zmat[6], zmat[5], zmat[1]
            if 
            _type = 
            tarif.setdefault('numeber', _num)

tarif_types = {
    'LG': 'Логистика',
    'CL': 'Сборные',
    'ST': 'Манипулятор',
    'GT': 'Общие условия',
    'CL': 'Сборные',
    'PS': 'ПЦС',
    'SM': 'ВРФ',
}

res = parce_mat_names(tarif_codes, zmat_list)

print ('done')