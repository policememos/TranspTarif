import openpyxl


fot_tarif_name = 'samara_tarif.xlsx'
zmat_list_name = 'ZMAT_LIST.xlsx'
zfortest_name = 'ZFORTEST.xlsx'
tarif_types = {
    'LG': 'Логистика', # в таблице согласованных тарифов отсутствует
    'ST': 'Манипулятор',
    'GT': 'Общие условия',
    'CL': 'Сборные',
    'PS': 'ПЦС', # в таблице согласованных тарифов отсутствует
    'SM': 'ВРФ', # в таблице согласованных тарифов отсутствует
}

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

def fill_first_sheet(sheet_my):
    line_flag = False
    if not line_flag:
        line_counter = int(last_row)+1
        line_flag = True
    for tarif in mapped_tarifs:
        a_col = ('ZR11', 'ZW91')
        b_col = ('73', '*')
        f_col = tarif['fot']
        g_col = tarif['tonns']+'T'
        h_col = tarif['len']+'M'
        i_col = 'X' if 'ST' in tarif['type'] else ''
        j_col = 'X' if 'CL' in tarif['type'] else ''
        if not tarif.get('numeber', False):
            ttp = "-".join(tarif['type'])
            print(f'Ошибка при создании новго экселя с тарифом Z-{f_col}-{ttp}-{g_col}-{h_col}')
            continue
        c_col = tarif['numeber']

        for start_mpl, end_mpl in tarif['prices'].items():
            if isinstance(end_mpl, dict):
                for _end_mpl, _pr in end_mpl.items():
                    d_col = start_mpl
                    e_col = _end_mpl
                    k_col = _pr
                    for i in a_col:
                        sheet_my.cell(row=line_counter, column=1, value=i)

                        if i == 'ZR11':
                            sheet_my.cell(row=line_counter, column=2, value=b_col[0])
                        else:
                            sheet_my.cell(row=line_counter, column=2, value=b_col[1])

                        sheet_my.cell(row=line_counter, column=3, value=c_col)
                        sheet_my.cell(row=line_counter, column=4, value=d_col)
                        sheet_my.cell(row=line_counter, column=5, value=e_col)
                        sheet_my.cell(row=line_counter, column=6, value=f_col)
                        sheet_my.cell(row=line_counter, column=7, value=g_col)
                        sheet_my.cell(row=line_counter, column=8, value=h_col)
                        sheet_my.cell(row=line_counter, column=9, value=i_col)
                        sheet_my.cell(row=line_counter, column=10, value=j_col)
                        sheet_my.cell(row=line_counter, column=11, value=k_col)
                        line_counter += 1

def backup_fill_first_sheet(sheet_my):
    ed_sheet = sheet_my
    for tarif in mapped_tarifs:
        line_counter = int(last_row)+1
        a_col = ('ZR11', 'ZW91')
        b_col = ('73', '*')
        f_col = tarif['fot']
        g_col = tarif['tonns']+'T'
        h_col = tarif['len']+'M'
        i_col = 'X' if 'ST' in tarif['type'] else ''
        j_col = 'X' if 'CL' in tarif['type'] else ''
        if not tarif.get('numeber', False):
            ttp = "-".join(tarif['type'])
            print(f'Ошибка при создании новго экселя с тарифом Z-{f_col}-{ttp}-{g_col}-{h_col}')
            continue
        c_col = tarif['numeber']

        for start_mpl, end_mpl in tarif['prices'].items():
            if isinstance(end_mpl, dict):
                for _end_mpl, _pr in end_mpl.items():
                    d_col = start_mpl
                    e_col = _end_mpl
                    k_col = _pr
                    for i in a_col:
                        ed_sheet.cell(row=line_counter, column=1, value=i)

                        if i == 'ZR11':
                            ed_sheet.cell(row=line_counter, column=2, value=b_col[0])
                        else:
                            ed_sheet.cell(row=line_counter, column=2, value=b_col[1])

                        ed_sheet.cell(row=line_counter, column=3, value=c_col)
                        ed_sheet.cell(row=line_counter, column=4, value=d_col)
                        ed_sheet.cell(row=line_counter, column=5, value=e_col)
                        ed_sheet.cell(row=line_counter, column=6, value=f_col)
                        ed_sheet.cell(row=line_counter, column=7, value=g_col)
                        ed_sheet.cell(row=line_counter, column=8, value=h_col)
                        ed_sheet.cell(row=line_counter, column=9, value=i_col)
                        ed_sheet.cell(row=line_counter, column=10, value=j_col)
                        ed_sheet.cell(row=line_counter, column=11, value=k_col)
                        line_counter += 1

    return ed_sheet

zmat_list = read_xslx(zmat_list_name)
fot_tarif = read_xslx(fot_tarif_name)
zfortest = read_xslx(zfortest_name)
tarif_codes = parce_tarifs_naming(fot_tarif)

mapped_tarifs = parce_mat_names(tarif_codes, zmat_list)
# {'z': 'Z', 'fot': 'PO1033', 'type': ('GT',), 'tonns': '1.5', 'len': '6', 'numeber': 3000009096}

zspk_all_xlsx = openpyxl.load_workbook('ZSPK_ALL_unprotected.xlsx')
first_sheet = zspk_all_xlsx.active
last_row = first_sheet.dimensions.split(':')[1][1:]
fill_first_sheet(first_sheet)
zspk_all_xlsx.save('result.xlsx')