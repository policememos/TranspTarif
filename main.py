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
                tar_name = n
                n = n.split('-')
                if len(n) == 5:
                    dic = {
                        'z': n[0],
                        'fot': n[1],
                        'type': (n[2],),
                        'tonns': n[3].replace('Т','').replace('T',''),
                        'len': n[4].replace('M','').replace('М',''),
                        'tar_name': tar_name,
                        'prices': dict()
                    }
                    dicts.append(dic)
                elif len(n) == 6:
                    dic = {
                        'z': n[0],
                        'fot': n[1],
                        'type': (n[2],n[3]),
                        'tonns': n[4].replace('Т','').replace('T',''),
                        'len': n[5].replace('M','').replace('М',''),
                        'tar_name': tar_name,
                        'prices': dict()
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

def check_type(_type):
    if _type == 'CL':
        return 'CL'
    if _type == 'ST':
        return 'ST'
    if 'CL' in _type:
        if 'ST' in _type:
            return 'CLST'
    else:
        return _type
  

def parce_mat_names(tarifs, zmat, skipping):
    tarif_with_number = []
    for tarif in tarifs:
        if skipping:
            if any(lambda x: 1 for x in ['SM','PS','LG'] if x in tarif['type']):
                print(f"Скипаем тариф {tarif['z']}-{tarif['fot']}-{''.join(tarif['type'])}-{tarif['tonns']}T-{tarif['len']}M\nОн Врф/Пцс/Логистика\nПараметр skipping=1\n")
                continue
        for zmat in zmat_list[1:]:
            _type, _tonns, _len, _num = ['GT'], float(zmat[6]), float(zmat[5]), zmat[1]
            if zmat[3] is not None:
                zmat[3] = 'X'
            if zmat[4] is not None:
                zmat[4] = 'X'
            if zmat[3]== 'X' and zmat[4] == 'X':
                _type = ['CL', 'ST']
            elif zmat[3] == 'X':
                _type = ['ST']
            elif zmat[4] == 'X':
                _type = ['CL']
            tar_tonns = float(tarif['tonns'])
            tar_len = float(tarif['len'])


            # {'z': 'Z',
            #  'fot': 'PO1033',
            #  'type': ('GT',), ST-манип, CL-сборная
            #  'tonns': '1.5',
            #  'len': '6',
            #  'tar_name': 'Z-PO1033-GT-1.5T-6M',
            #  'prices': {'TZRU63-0001': {...},}

            tr_type_cheker = check_type(tarif['type'])

            # костыль для мэппинга 13.5м 20тонн
            # ИСПРАВЬ
            if tar_tonns == 20 and tar_len in (13.5,13.0,11.7):
                tar_len = 12.0
                tarif['len'] = '12' # в тарифе
                print(f'Подмена тарифа {tarif["tar_name"]} \n')

            # Автодоставка сборная Манипулятор 3.5Т 6м
            if tr_type_cheker == 'CLST':
                if tar_tonns in (0.5,1.0,1.5,2.0,3.0) and tar_len == 6.0:
                    tar_tonns = 3.5
                    tarif['tonns'] = '3.5'
                    tar_len = 6.0
                    tarif['len'] = '6.0'
                    print(f'Подмена тарифа {tarif["tar_name"]} - сбор манип, 3.5т 6м')
                if tar_tonns in (1.0,2.0) and tar_len == 6.2:
                    tar_tonns = 3.5
                    tarif['tonns'] = '3.5'
                    tar_len = 6.0
                    tarif['len'] = '6.0'
                    print(f'Подмена тарифа {tarif["tar_name"]} - сбор манип, 3.5т 6м')

            # Автодоставка  Манипулятор 3.5Т 6м
            if tr_type_cheker == 'ST':
                if tar_tonns in (2.5,3.0) and tar_len == 6.0:
                    tar_tonns = 3.5
                    tarif['tonns'] = '3.5'
                    tar_len = 6.0
                    tarif['len'] = '6.0'
                    print(f'Подмена тарифа {tarif["tar_name"]} - манип 3.5т 6м ')
                if tar_tonns == 0.5 and tar_len == 6.2:
                    tar_tonns = 3.5
                    tarif['tonns'] = '3.5'
                    tar_len = 6.0
                    tarif['len'] = '6.0'
                    print(f'Подмена тарифа {tarif["tar_name"]} - манип 3.5т 6м ')
                if tar_tonns == 1.5 and tar_len == 6.4:
                    tar_tonns = 3.5
                    tarif['tonns'] = '3.5'
                    tar_len = 6.0
                    tarif['len'] = '6.0'
                    print(f'Подмена тарифа {tarif["tar_name"]} - манип 3.5т 6м ')


            # Автодоставка  Манипулятор 5Т 6м
            # if len(tarif['type']) == 1:
            #     if 'ST' in tarif['type']:
            #         if tar_tonns in (4.0,5.0) and tar_len == 6.0:
            #             # if 'CL' in
            #             tar_tonns = 5.0
            #             tarif['tonns'] = '5.0'
            #             tar_len = 6.0
            #             tarif['len'] = '6.0'
            #             print(f'Подмена тарифа {tarif["tar_name"]} - манип 5т 6м \n')

            # Автодоставка сборная Манипулятор 5Т 6м
            if tr_type_cheker == 'CLST':
                if tar_tonns == 4.0 and tar_len == 6.0:
                    tar_tonns = 5.0
                    tarif['tonns'] = '5.0'
                    tar_len = 6.0
                    tarif['len'] = '6.0'
                    print(f'Подмена тарифа {tarif["tar_name"]} - сбор, манип 5т 6м ')

            # Автодоставка  Манипулятор 9Т 6,7м
            if tr_type_cheker == 'ST':
                if tar_tonns == 4.0 and tar_len in (6.0,6.4):
                    tar_tonns = 9.0
                    tarif['tonns'] = '9.0'
                    tar_len = 6.7
                    tarif['len'] = '6.7'
                    print(f'Подмена тарифа {tarif["tar_name"]}- Манипулятор 9Т 6,7м ')
                if tar_tonns == 5.0 and tar_len in (5.4,5.5,5.8,6.0,6.2,6.4):
                    tar_tonns = 9.0
                    tarif['tonns'] = '9.0'
                    tar_len = 6.7
                    tarif['len'] = '6.7'
                    print(f'Подмена тарифа {tarif["tar_name"]}- Манипулятор 9Т 6,7м ')

            # Автодоставка сборная Манипулятор 9Т 6,7м
            # if tr_type_cheker == 'CLST':
            #     if tar_tonns == 9.0 and tar_len in (6.7,):
            #         tar_tonns = 9.0
            #         tarif['tonns'] = '9.0'
            #         tar_len = 6.7
            #         tarif['len'] = '6.7'
                    # print(f'Подмена тарифа {tarif["tar_name"]} \n')

            # Автодоставка  Манипулятор 10Т 8м
            # Z-PO1106-ST-10T-6.4M будет исправлен, сейчас попадает в манип 20Т 12м
            if tr_type_cheker == 'ST':
                if tar_tonns == 6.0 and tar_len in (7.0,6.0):
                    tar_tonns = 10.0
                    tarif['tonns'] = '10.0'
                    tar_len = 8.0
                    tarif['len'] = '8.0'
                    print(f'Подмена тарифа {tarif["tar_name"]} - Манипулятор 10Т 8м')
                if tar_tonns == 8.0 and tar_len in (6.0,):
                    tar_tonns = 10.0
                    tarif['tonns'] = '10.0'
                    tar_len = 8.0
                    tarif['len'] = '8.0'
                    print(f'Подмена тарифа {tarif["tar_name"]} - Манипулятор 10Т 8м')
                if tar_tonns == 10.0 and tar_len in (6.0,6.4):
                    tar_tonns = 10.0
                    tarif['tonns'] = '10.0'
                    tar_len = 8.0
                    tarif['len'] = '8.0'
                    print(f'Подмена тарифа {tarif["tar_name"]} - Манипулятор 10Т 8м')

            # Автодоставка  Манипулятор 20Т 12м
            if tr_type_cheker == 'ST':
                if tar_tonns == 10.0 and tar_len in (8.0,8.2,8.4,8.5):
                    tar_tonns = 20.0
                    tarif['tonns'] = '20.0'
                    tar_len = 12.0
                    tarif['len'] = '12.0'
                    print(f'Подмена тарифа {tarif["tar_name"]} - Манипулятор 20Т 12м')
                if tar_tonns == 15.0 and tar_len == 9.6:
                    tar_tonns = 20.0
                    tarif['tonns'] = '20.0'
                    tar_len = 12.0
                    tarif['len'] = '12.0'
                    print(f'Подмена тарифа {tarif["tar_name"]} - Манипулятор 20Т 12м')








            # Автодоставка сборная 1.5Т 4м
            if tr_type_cheker == 'CL':
                if tar_tonns in (0.5,0.7) and tar_len == 4.0:
                    tar_tonns = 1.5
                    tarif['tonns'] = '1.5'
                    tar_len = 4.0
                    tarif['len'] = '4.0'
                    print(f'Подмена тарифа {tarif["tar_name"]} - сборная 1.5Т 4м')
                if tar_tonns in (0.5,) and tar_len == 6.2:
                    tar_tonns = 1.5
                    tarif['tonns'] = '1.5'
                    tar_len = 4.0
                    tarif['len'] = '4.0'
                    print(f'Подмена тарифа {tarif["tar_name"]} - сборная 1.5Т 4м')
                if tar_tonns == 1.0 and tar_len == 8.2:
                    tar_tonns = 1.5
                    tarif['tonns'] = '1.5'
                    tar_len = 4.0
                    tarif['len'] = '4.0'
                    # print(f'Подмена тарифа {tarif["tar_name"]} \n')

            # Автодоставка  сборная 1.5Т 6м
            if tar_tonns in (0.5,1.5,1) and tar_len == 6.0:
                tar_tonns = 1.5
                tarif['tonns'] = '1.5'
                tar_len = 6.0
                tarif['len'] = '6.0'
                # print(f'Подмена тарифа {tarif["tar_name"]} \n')
            if tar_tonns == 1 and tar_len == 6.2:
                tar_tonns = 1.5
                tarif['tonns'] = '1.5'
                tar_len = 6.0
                tarif['len'] = '6.0'
                # print(f'Подмена тарифа {tarif["tar_name"]} \n')

            # Автодоставка сборная 2Т 6м
            if tar_tonns == 2.0 and tar_len in (6.0,8.2,6.5,6.2):
                tar_tonns = 2.0
                tarif['tonns'] = '2.0'
                tar_len = 6.0
                tarif['len'] = '6.0'
                # print(f'Подмена тарифа {tarif["tar_name"]} \n')

            # Автодоставка сборная 3Т 6м
            if tar_tonns == 3.0 and tar_len in (6.0,8.2):
                tar_tonns = 3.0
                tarif['tonns'] = '3.0'
                tar_len = 6.0
                tarif['len'] = '6.0'
                # print(f'Подмена тарифа {tarif["tar_name"]} \n')

            # Автодоставка сборная 5Т 6м
            if tar_tonns == 4.0 and tar_len in (6.0,8.2):
                tar_tonns = 5.0
                tarif['tonns'] = '5.0'
                tar_len = 6.0
                tarif['len'] = '6.0'
                # print(f'Подмена тарифа {tarif["tar_name"]} \n')
            if tar_tonns == 5.0 and tar_len in (6.0,6.2,8.2):
                tar_tonns = 5.0
                tarif['tonns'] = '5.0'
                tar_len = 6.0
                tarif['len'] = '6.0'
                # print(f'Подмена тарифа {tarif["tar_name"]} \n')

            # Автодоставка сборная 10Т 6м
            if tar_tonns in (6.0,10.0) and tar_len == 13.2:
                tar_tonns = 10.0
                tarif['tonns'] = '10.0'
                tar_len = 6.0
                tarif['len'] = '6.0'
                # print(f'Подмена тарифа {tarif["tar_name"]} \n')
            if tar_tonns == 7.0 and tar_len == 6.0:
                tar_tonns = 10.0
                tarif['tonns'] = '10.0'
                tar_len = 6.0
                tarif['len'] = '6.0'
                # print(f'Подмена тарифа {tarif["tar_name"]} \n')

            # Автодоставка  1.5Т 4м
            if tar_tonns in (1.5,1.0) and tar_len == 6.0:
                tar_tonns = 1.5
                tarif['tonns'] = '1.5'
                tar_len = 4.0
                tarif['len'] = '4.0'
                # print(f'Подмена тарифа {tarif["tar_name"]} \n')
            if tar_tonns == 1.5 and tar_len == 5.0:
                tar_tonns = 1.5
                tarif['tonns'] = '1.5'
                tar_len = 4.0
                tarif['len'] = '4.0'
                # print(f'Подмена тарифа {tarif["tar_name"]} \n')

            # Автодоставка  2Т 6м
            if tar_tonns == 2.0 and tar_len in (4.2,6.0,12.0):
                tar_tonns = 2.0
                tarif['tonns'] = '2.0'
                tar_len = 6.0
                tarif['len'] = '6.0'
                # print(f'Подмена тарифа {tarif["tar_name"]} \n')

            # Автодоставка  3Т 6м
            if tar_tonns in (3.0,2.5) and tar_len == 6.0:
                tar_tonns = 3.0
                tarif['tonns'] = '3.0'
                tar_len = 6.0
                tarif['len'] = '6.0'
                # print(f'Подмена тарифа {tarif["tar_name"]} \n')
            if tar_tonns == 3.0 and tar_len in (3.0,5.0):
                tar_tonns = 3.0
                tarif['tonns'] = '3.0'
                tar_len = 6.0
                tarif['len'] = '6.0'
                # print(f'Подмена тарифа {tarif["tar_name"]} \n')

            # Автодоставка  5Т 6м
            if tar_tonns == 4.0 and tar_len == 6.0:
                tar_tonns = 5.0
                tarif['tonns'] = '5.0'
                tar_len = 6.0
                tarif['len'] = '6.0'
                # print(f'Подмена тарифа {tarif["tar_name"]} \n')
            if tar_tonns == 4.5 and tar_len == 6.0:
                tar_tonns = 5.0
                tarif['tonns'] = '5.0'
                tar_len = 6.0
                tarif['len'] = '6.0'
                # print(f'Подмена тарифа {tarif["tar_name"]} \n')
            if tar_tonns == 5.0 and tar_len in (5.4,5.5,5.0,6.0,6.5):
                tar_tonns = 5.0
                tarif['tonns'] = '5.0'
                tar_len = 6.0
                tarif['len'] = '6.0'
                # print(f'Подмена тарифа {tarif["tar_name"]} \n')

            # Автодоставка  10Т 6м
            if tar_tonns == 10.0 and tar_len in (6.2,6.4,6.0,7.0):
                tar_tonns = 10.0
                tarif['tonns'] = '10.0'
                tar_len = 6.0
                tarif['len'] = '6.0'
                # print(f'Подмена тарифа {tarif["tar_name"]} \n')
            if tar_tonns in (7.0,8.0,6.0) and tar_len == 6.0:
                tar_tonns = 10.0
                tarif['tonns'] = '10.0'
                tar_len = 6.0
                tarif['len'] = '6.0'
                # print(f'Подмена тарифа {tarif["tar_name"]} \n')
            if tar_tonns == 6.0 and tar_len == 7.0:
                tar_tonns = 10.0
                tarif['tonns'] = '10.0'
                tar_len = 6.0
                tarif['len'] = '6.0'
                # print(f'Подмена тарифа {tarif["tar_name"]} \n')

            # Автодоставка  15Т 8.2м
            if tar_tonns == 15.0 and tar_len in (7.0,8.2):
                tar_tonns = 15.0
                tarif['tonns'] = '15.0'
                tar_len = 8.2
                tarif['len'] = '8.2'
                # print(f'Подмена тарифа {tarif["tar_name"]} \n')

            # Автодоставка  25Т 12м
            if tar_tonns == 25.0 and tar_len == 13.5:
                tar_tonns = 25.0
                tarif['tonns'] = '25.0'
                tar_len = 12.0
                tarif['len'] = '12.0'
                # print(f'Подмена тарифа {tarif["tar_name"]} \n')

            # АВТОДОСТАВКА 40Т 12М
            if tar_tonns in (27.0,28.0,30.0) and tar_len == 12.0:
                tar_tonns = 40.0
                tarif['tonns'] = '40.0'
                tar_len = 12.0
                tarif['len'] = '12.0'
                # print(f'Подмена тарифа {tarif["tar_name"]} \n')
            if tar_tonns == 30.0 and tar_len == 13.5:
                tar_tonns = 40.0
                tarif['tonns'] = '40.0'
                tar_len = 12.0
                tarif['len'] = '12.0'
                # print(f'Подмена тарифа {tarif["tar_name"]} \n')



            if _tonns == tar_tonns and _len == tar_len:
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
            print(f'Ошибка при создании новго экселя с тарифом Z-{f_col}-{ttp}-{g_col}-{h_col}\n---> Нет подходящего материала в zmat_list\n')
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

mapped_tarifs = parce_mat_names(tarif_codes, zmat_list, skipping=True)
# {'z': 'Z', 'fot': 'PO1033', 'type': ('GT',), 'tonns': '1.5', 'len': '6', 'numeber': 3000009096}

for tar in mapped_tarifs:
    print(f"{tar['z']}-{tar['fot']}-{''.join(tar['type'])}-{tar['tonns']}T-{tar['len']}M {tar.get('numeber', '')}")

zspk_all_xlsx = openpyxl.load_workbook('ZSPK_ALL_unprotected.xlsx')
first_sheet = zspk_all_xlsx.active
last_row = first_sheet.dimensions.split(':')[1][1:]
fill_first_sheet(first_sheet)
zspk_all_xlsx.save('result.xlsx')