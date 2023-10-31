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

print(check_type('ST'))
print(check_type('CL'))
print(check_type('GT'))
a=('ST','CL',)
print(check_type(a))