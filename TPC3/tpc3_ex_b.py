import re
import math

def printTable(title, key_title, value_title, dictionary, width = 5, separator = "|"):
    print(f"{title}")
    header = f"{key_title:<{width}} | {value_title}"
    print(header)
    print("-" * len(header))
    for key, value in dictionary.items():
        print(f"{str(key):<{width}} {separator} {value}")
    print()

def remove_s(phrase):
    words = phrase.split()
    new_words = []
    for word in words:
        while word.endswith('s'):
            word = word[:-1]
        new_words.append(word)
    new_phrase = ' '.join(new_words)
    return new_phrase


# Exercício a)
def get_process_per_year(data):
    dic = {}
    for p in data:
        dob = p["dob"]
        fields = dob.split("-")
        ano = fields[0]
        if ano in dic:
            dic[ano] += 1
        else:
            dic[ano] = 1
    # dic = dict(sorted(dic.items())) # ordenação pelo ano
    dic = dict(sorted(dic.items(), key = lambda x:x[1], reverse=True)) # ordenação pelo numero de processos
    
    printTable("Distribuição de processos por ano", "Ano", "Nº de processos", dic)


def get_seculo(ano):
    return math.ceil(ano/100)


# Exercício b)
def get_process_per_century(data):
    dic = {}
    for p in data:
        dob = p["dob"]
        fields = dob.split("-")
        ano = int(fields[0])
        seculo = get_seculo(ano)
        all_nomes = []
        for n in ["nome", "nome-pai", "nome-mae"]:
            if n in p:
                all_nomes.append(p[n])
        if "parentesco" in p:
            for tup in p["parentesco"]:
                all_nomes.append(tup[0])
        
        for nome in all_nomes: 
            # TODO talvez aqui definir uma separação entre o first_name e last_name
            first_and_last = nome.split()
            if len(first_and_last) > 1:
                first_and_last = first_and_last[0:1] + first_and_last[-1:]
            for nome in first_and_last:
                if seculo in dic:
                    if nome in dic[seculo]:
                        dic[seculo][nome] += 1
                    else:
                        dic[seculo][nome] = 1
                else:
                    dic[seculo] = {nome: 1}
                    # dic[seculo][nome] = 1
    
    # Sorting dictionaries
    for key in dic:
        print(f"TOP 5 do século {key}:")
        sec = dic[key]
        sec = dict(sorted(sec.items(), key=lambda x:x[1], reverse=True))
        for i, k in enumerate(sec):
            print(f"-> {k} : {sec[k]}")
            if i == 5:
                print()
                break
    return dic


# Exercício c)
def get_graus_parentesco(data):
    freq_final = {} # {parentesco: frequência}
    for p in data:
        if "parentesco" not in p:
            continue        
        lista_p = p["parentesco"]
        for _, grau_de_parentesco in lista_p:
            if grau_de_parentesco in freq_final:
                freq_final[grau_de_parentesco] += 1
            else:
                freq_final[grau_de_parentesco] = 1
    freq_final = dict(sorted(freq_final.items(), key=lambda x:x[1], reverse=True))
    printTable("Frequências de graus de parentesco", "Grau de Parentesco", "Frequência", freq_final, width=25)
    return freq_final





### MAIN
file = open("processos.txt")
processos = []
regex = r"(([A-Z][a-z ,]+)+),(\w+\s*\w*\s*\w+)\.[^::]"
pattern = re.compile(regex)

for n, line in enumerate(file):
    line = line.strip()
    if not line: 
        continue
    fields = re.split(r'::+', line)
    fields = list(filter(lambda x:x!="", fields))
    dic = {}
    for i, f in enumerate(fields):
        if i == 0:
            dic["id"] = f
        elif i == 1:
            dic["dob"] = f
        elif i == 2:
            dic["nome"] = f
        elif i == 3:
            dic["nome-pai"] = f
        elif i == 4:
            dic["nome-mae"] = f
        elif i == 5:
            # regex = r"(([A-Z][a-z ,]+)+),(\w+\s*\w*\s*\w+)\."
            matches = pattern.finditer(f)
            final_value_dict = {"obs": f}
            parentescos = []
            for match in matches:
                grau_de_parentesco = match.group(3)
                if grau_de_parentesco[-1] == "s":
                    grau_de_parentesco = remove_s(grau_de_parentesco)
                # if grau_de_parentesco == "Frei":
                #     print(f)
                nomes = match.group(1)
                arr_nomes = re.split(r"\se\s|\s?,\s?", nomes)
                for nome in arr_nomes:
                    tup = (nome, grau_de_parentesco)
                    parentescos.append(tup)

            dic["obs"] = f
            dic["parentesco"] = parentescos
            # print(dic)
    processos.append(dic)

# for p in processos:
#     if "obs" in p:
#         print(p["obs"])

# get_process_per_year(processos)
# get_process_per_century(processos)
get_graus_parentesco(processos)


file.close()

