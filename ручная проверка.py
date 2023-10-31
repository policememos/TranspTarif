# ИСПРАВЬ
if tar_tonns == 20 and tar_len in (13.5,13.0,11.7):
    tar_len = 12.0
    tarif['len'] = '12' # в тарифе
    print(f'Подмена тарифа {tarif["tar_name"]} \n')

# Автодоставка сборная Манипулятор 3.5Т 6м
if tr_type_cheker == 'CLST':
    if tar_tonns <= 3.5 and tar_len == 6.0:
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