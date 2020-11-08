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
    keywrds_lst = ['[TEST]', '[DATE]', '[LUMINAIRE]',
                   '[MORE]', '[MANUFAC]', '[OTHER]', 
                   '[LUMCAT]', '[LAMP]', '[TESTLAB]', 
                   '[TESTDATE]', '[ISSUEDATE]', 
                   '[LAMPPOSITION]' ]
    
    
    # Находим и записываем в словарь ies_dct значения 
    # опциональных параметров
    keyword_dct = {}
    for i in keywrds_lst:
        temp = keywrds_srch(i, ies)
        if temp != -1:
            keyword_dct[i] = temp
      
    ies_dct['OPTIONAL'] = keyword_dct     
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
    
    parametrs_dct = {}
    # Число ламп в светильнике
    parametrs_dct['N_L'] = int(parametrs[0])

    # Световой поток лампы
    parametrs_dct['FLUX_LAMP'] = int(parametrs[1])

    # Множитель, на который при необходимости могут быть умножены все
    # значения силы света
    parametrs_dct['LUMINOUS_INTENSITY_FACTOR'] = int(parametrs[2])

    
    # Четвёртое число в списке оязательных параметров
    # соответсвует количеству полярных углов
    parametrs_dct['N_PA'] = int(parametrs[3])

    # Пятое число в списке оязательных параметров
    # соответсвует количеству азимутальных углов.
    parametrs_dct['N_AA'] = int(parametrs[4])


    
    # Определяем тип фотометрии
    if parametrs[5] == 1:
        parametrs_dct['PHOTOMETRY']='C'
    elif parametrs[5] == 2:
        parametrs_dct['PHOTOMETRY']='B'
    else:
        parametrs_dct['PHOTOMETRY']='A'

    # Система единиц
    parametrs_dct['SYSTEM_OF_UNITS'] = int(parametrs[6])
    # Ширина светильника
    parametrs_dct['WIDTH'] = int(parametrs[7])
    # Длина светильника
    parametrs_dct['LENGTH'] = int(parametrs[8])
    # Высота светильника
    parametrs_dct['HEIGHT'] = int(parametrs[9])
    # Коэффициент балласта
    parametrs_dct['BALLAST_FACTOR'] = int(parametrs[10])
    # Признак версии
    parametrs_dct[''] = int(parametrs[11])

    # Записываем в словарь ies_dct электрическую мощность
    # светильника. Последнее число в списке обязательных параметров
    parametrs_dct['POWER'] = parametrs[12]

    ies_dct['PARAMETRS'] = parametrs_dct
    
    # Определяем значения полярных углов
    start_polar = 13
    end_polar = start_polar + parametrs_dct['N_PA']
    polar_angles = ies[start_polar:end_polar]
   
    # Определяем значения азимутальных углов
    end_azimut = end_polar + parametrs_dct['N_AA']
    azimut_angles = ies[end_polar:end_azimut]
   
    # Определяем значения силы света
    endI = end_azimut + parametrs_dct['N_PA'] * parametrs_dct['N_AA']
    I = ies[end_azimut:endI]
    k = parametrs[2]
    I = [i * k for i in I]
   
    # Формируем словарь, содержащий угловое распределние силы света.
    # Для доступа к значению силы света используется два ключа:
    # первый ключ --- это азимутальный угол, второй --- меридиональный
    I_table = {}
    for j in azimut_angles:
        intensity_curve = {}
        for i in polar_angles:
            intensity_curve[i] = I[polar_angles.index(i) + 
                           parametrs_dct['N_PA']*azimut_angles.index(j)]      
        I_table[j] = intensity_curve
    
    ies_dct['I_TABLE'] = I_table
  
    ies_dct['POLAR'] = polar_angles
    ies_dct['AZIMUT'] = azimut_angles
    fid.close()
    return ies_dct

# Функция записи ies файла
def writer(fid, ies_dct):
    fid.write(ies['FORMAT']+'\n')

    for i in ies_dct['OPTIONAL']:
        fid.write("{0} {1}\n".format(i,ies_dct['OPTIONAL'][i]))
 
    # Определяем тип фотометрии
    if ies_dct['PARAMETRS']['PHOTOMETRY']=='C':
        ies_dct['PARAMETRS']['PHOTOMETRY'] = 1
    elif ies_dct['PARAMETRS']['PHOTOMETRY']=='B':
        ies_dct['PARAMETRS']['PHOTOMETRY'] = 2
    else:
        ies_dct['PARAMETRS']['PHOTOMETRY'] = 3



    fid.write("{0}\n".format(ies['TILT']))

    for i in ies_dct['PARAMETRS']:
        fid.write("{0} ".format(ies_dct['PARAMETRS'][i]))
    fid.write("\n")

    itable = ies_dct['I_TABLE']
    azimut_lst = sorted(itable.keys())
    polar_lst = itable[0].keys()

    for i in polar_lst:
        fid.write("{0} ".format(i))
    fid.write("\n")


    for i in azimut_lst:
        fid.write("{0} ".format(i))
    fid.write("\n")

    for i in azimut_lst:
        for j in polar_lst:
            fid.write("{0} ".format(itable[i][j]))
        fid.write("\n")
    fid.close()


    # Функция записи ies файла
def rotekv(ies_dct, angle = 0):
    itable = ies_dct['I_TABLE']
    new_itable = {}

    for key in itable:
        temp = key + angle
        if temp >= 360: 
            temp = temp - 360 

        new_itable[temp] = itable[key]

    ies_dct['I_TABLE'] = new_itable
    return ies_dct



if __name__ == "__main__":
    import sys
    fid1 = open(sys.argv[1], encoding='cp1251')
    ies = reader(fid1)
    ies = rotekv(ies, angle = float(sys.argv[2]))

    fid2 = open("{0}_{1}".format(sys.argv[2], sys.argv[1]), encoding='cp1251', mode = 'w')
    writer(fid2, ies)
    

