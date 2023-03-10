import json
import re
from math import prod

my_built_ins = {
    "sum": sum,
    "media": lambda x:sum(x)/len(x),
    "mult": prod,
    "prod": prod,
    "max": max,
    "min": min
}

class FieldInfo:
  
    # Recebe a string do campo
    def __init__(self, string):

        self.name = string.split("{")[0]
        self.lenght = None
        self.func = None
        regex_len = r"{(\d+)(?:,(\d+))?}"

        lenght_param = re.search(regex_len, string)
        if lenght_param:
            groups = lenght_param.groups()
            
            if groups[1] == None:
                groups = int(groups[0]), int(groups[0])
            groups = int(groups[0]), int(groups[1])
            self.lenght = groups
            
            func_param = re.search(r"::(\w+)", string)
            if func_param:
                func_name = func_param.group(1)
                if func_name in my_built_ins:
                    self.func = func_name
                    self.name += f"_{func_name}"
                else:
                    print(f'Atenção: Função pedida no campo "{string}" não está implementada!')

    def is_list(self):
        return self.lenght is not None
    
    def top_lenght(self):
        if self.lenght:
            return self.lenght[1]
        else:
            # print(f"ATENÇÃO! O CAMPO {self.name} NÃO É UMA LISTA!! TOP_LENGHT RETORNOU NONE")
            return None

    def get_func(self):
        return self.func



def read_csv(csv_file_path):
    ficheiro = open(csv_file_path, encoding='utf-8')
    data = []

    # Verificação do nome dos campos do ficheiro, bem como eventuais funções inerentes.
    header = ficheiro.readline()
    arr_header = re.findall(r'[^,{ \n]+(?:{[^\}]+}(?:\:\:\w+)?)?', header)
    
    fields_info = []
    for field in arr_header:
        fields_info.append(FieldInfo(field))


    # Verificação das linhas do ficheiro.
    for line in ficheiro:
        line_split = line.split(",")
        line_i = 0
        fields_i=0
        line_dict = {}
        while line_i < len(line_split):
            obj_field = fields_info[fields_i]
            key_name = obj_field.name
            if not obj_field.is_list():
                line_dict[key_name] = line_split[line_i]
                line_i += 1
            else:
                list_end_index = line_i + obj_field.top_lenght()
                final_list = []
                while line_i<list_end_index:
                    if line_split[line_i] != "" and line_split[line_i] != "\n":
                        final_list.append(int(line_split[line_i]))
                    line_i+=1
                line_dict[key_name] = final_list
                # Verificação de função
                if obj_field.func:
                    function = my_built_ins[obj_field.func]
                    line_dict[key_name] = function(final_list)
            fields_i += 1

        data.append(line_dict)


    ficheiro.close()
    return data

def write_json(data, json_file_path):
    with open(json_file_path, mode='w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)

def csv_to_json(csv_file_path, json_file_path):
    data = read_csv(csv_file_path)
    write_json(data, json_file_path)



csv_to_json("file.csv", "result.json")