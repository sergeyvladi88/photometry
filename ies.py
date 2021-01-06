#!/usr/bin/env python


# Функция поиска опциональных параметров
def keywrds_srch(keyword, string):
    if keyword in string:
        start = string.find(keyword)
        end = string.find("\n", start)
        str_lst = string[start:end].split()
        keywrds_str = ' '
        return keywrds_str.join(str_lst[1:])
    else:
        return -1


# Функция чтения ies файла
def reader(fid):
    ies_dct = {}
    ies = fid.read()
    
    # Записываем в словарь ies_dct значение формата файла
    frmt = ies[0:ies.find('\n')]
    ies_dct['FORMAT'] = frmt
    
    # Формируем список опциональных параметров
    keywrds_lst = ['[TEST]', '[DATA]', '[LUMINAIRE]',
                   '[MORE]', '[MANUFAC]', '[OTHER]', 
                   '[LUMCAT]', '[LAMP]', '[TESTLAB]', 
                   '[TESTDATE]', '[ISSUEDATE]', 
                   '[LAMPPOSITION]', ]
    
    
    # Находим и записываем в словарь ies_dct значения 
    # опциональных параметров
    for i in keywrds_lst:
        temp = keywrds_srch(i, ies)
        if temp != -1:
            ies_dct[i] = temp
      
        
    # Находим и записываем в словарь ies_dct строку TILT
    starttilt = ies.find('TILT')
    endtilt = ies.find("\n", ies.find("TILT"))  
    ies_dct['TILT'] = ies[starttilt:endtilt]
    
    # Считываем числа идущие после строки TILT до конца файла 
    # в список ies
    ies = ies[endtilt:].split()
    ies = [float(i) for i in ies]

    # Первые 13 чисел соответсвуют обязательным параметрам.
    parametrs = ies[0:13]
    
    
    # Четвёртое число в списке оязательных параметров
    # соответсвует количеству полярных углов
    pc = int(parametrs[3])

    # Пятое число в списке оязательных параметров
    # соответсвует количеству азимутальных углов.
    ac = int(parametrs[4])

    # Определяем тип фотометрии
    if parametrs[5] == 1:
        ies_dct['PHOTOMETRY']='C'
    elif parametrs[5] == 2:
        ies_dct['PHOTOMETRY']='B'
    else:
        ies_dct['PHOTOMETRY']='A'

    # Записываем в словарь ies_dct электрическую мощность
    # светильника. Последнее число в списке обязательных параметров
    ies_dct['POWER'] = parametrs[-1]
    
    # Определяем значения полярных углов
    start_polar = 13
    end_polar = start_polar + pc
    polar_angles = ies[start_polar:end_polar]
   
    # Определяем значения азимутальных углов
    end_azimut = end_polar + ac
    azimut_angles = ies[end_polar:end_azimut]
   
    # Определяем значения силы света
    endI = end_azimut + pc * ac
    I = ies[end_azimut:endI]
    k = parametrs[2]
    I = [i * k for i in I]
   
    # Формируем словарь, содержащий угловое распределние силы света.
    # Для доступа к значению силы света используется два ключа:
    # первый ключ --- это азимутальный угол, второй --- меридиональный
    I_table = {}

    if azimut_angles[-1] == 90:
        for j in azimut_angles:
            intensity_curve = {}
            for i in polar_angles:
                intensity_curve[i] = I[polar_angles.index(i) + 
                                       pc*azimut_angles.index(j)]      
            I_table[j] = intensity_curve
            I_table[180-j] = intensity_curve
            I_table[180+j] = intensity_curve
            I_table[360-j] = intensity_curve
            
    elif azimut_angles[-1] == 360:
        for j in azimut_angles:
            intensity_curve = {}
            for i in polar_angles:
                intensity_curve[i] = I[polar_angles.index(i) + 
                                       pc*azimut_angles.index(j)]      
            I_table[j] = intensity_curve
        
    temp = list(I_table.keys())
    temp.sort()

    I_table_sort = {}

    for i in temp:
        I_table_sort[i]=I_table[i]

    ies_dct['I_TABLE'] = I_table_sort        
    return ies_dct

   
# Функция записи ies файла
def writer(fid, ies_dct):
    pass

if __name__ == "__main__":
    import sys
    fid = open(sys.argv[1], encoding='cp1251')
    ies = reader(fid)
