from typing import List

# Lê o ficheiro e retorna uma estrutura de dados com a informação armazenada.
def get_data_struct(filepath:str):
    f = open(filepath)
    # Ignora a primeira linha com as descrições dos campos
    f.readline()

    # Lista de listas em que cada lista tem a informação de uma linha.
    final_struct = []

    # TALVEZ NESTE PARSE ELIMINAR LOGO OS REGISTOS DOS QUE NÃO TEM DOENÇA
    i = 1
    for line in f:
        arr = line.split(",")
        try:
            arr[0] = int(arr[0])
            arr[2] = int(arr[2])
            arr[3] = int(arr[3])
            arr[4] = int(arr[4])
            arr[5] = int(arr[5])
        except ValueError:
            print(f"Valor inválido na linha {i}!")
            continue
        i+=1
        final_struct.append(arr)
    return final_struct

def get_distr_sexo(data_struct):
    
    distr = {}
    for line in data_struct:
        sexo = line[1]
        temDoenca = line[5]
        if temDoenca == 1:
            if sexo not in distr:
                distr[sexo] = 1
            else:
                distr[sexo] += 1

    return distr


def get_distr_age(data_struct):
    distr = {}
    for line in data_struct:
        idade = line[0]
        temDoenca = line[5]
        if temDoenca == 1:
            if idade not in distr:
                distr[idade] = 1
            else:
                distr[idade] += 1

    distr = dict(sorted(distr.items(), key=lambda x:x[0]))

    bottom = 30
    interval = 4
    current_top = bottom + interval
    faixa = (bottom, current_top)
    final_distr = {faixa:0}
    for age in distr:
        while age > current_top:
            bottom = current_top + 1
            current_top = bottom + interval
            faixa = (bottom, current_top)
            final_distr[faixa] = 0
        final_distr[faixa] += distr[age]

    return final_distr


def get_distr_colesterol(data_struct):
    distr = {}
    for line in data_struct:
        colesterol = line[3]
        temDoenca = line[5]
        if temDoenca == 1:
            if colesterol not in distr:
                distr[colesterol] = 1
            else:
                distr[colesterol] += 1

    distr = dict(sorted(distr.items(), key=lambda x:x[0]))

    bottom = min(distr) 
    interval = 9
    current_top = bottom + interval
    faixa = (bottom, current_top)
    final_distr = {faixa:0}
    for col in distr:
        while col > current_top:
            bottom = current_top + 1
            current_top = bottom + interval
            faixa = (bottom, current_top)
            final_distr[faixa] = 0
        final_distr[faixa] += distr[col]

    return final_distr

def draw_table(title, key_title, value_title, struct):
    print("------------------------")
    print(f"{title}")
    print(f"{key_title} {value_title}")
    
    print("------------------------")


def print_dict_table(title, key_title, value_title, dictionary):
    print(f"{title}\n{key_title:<15} | {value_title}")
    print("-" * 25)
    for key, value in dictionary.items():
        print(f"{str(key):<15} | {value}")



filename = "TPC1/myheart.csv"
# filename = "TPC1/test.csv"

data_struct = get_data_struct(filename)

distr_sex = get_distr_sexo(data_struct)
# print("Distr_sex ::")
# print(distr_sex)
print_dict_table("Distribuição por sexo", "Sexo", "Total", distr_sex)
print()


distr_age = get_distr_age(data_struct)
# print("Distr_age ::")
# print(distr_age)
print_dict_table("Distribuição por idade", "Faixa etária", "Total", distr_age)
print()


distr_colesterol = get_distr_colesterol(data_struct)
# print("Distr_colesterol ::")
# print(distr_colesterol)
print_dict_table("Distribuição por níveis de colesterol", "Nível de Colesterol", "Total", distr_colesterol)
print()

