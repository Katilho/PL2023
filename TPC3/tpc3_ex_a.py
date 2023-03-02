import re

def printTable(title, key_title, value_title, dictionary, width = 10, separator = "|"):
    print(f"{title}")
    header = f"{key_title:<{width}} | {value_title}"
    print(header)
    print("-" * len(header))
    for key, value in dictionary.items():
        print(f"{str(key):<5} {separator} {value}")
    print()


f = open("TPC3/processos.txt")
regex = r':+(\d{4})-(\d{2})-(\d{2}):+'
dic = {}
for i, line in enumerate(f):
    if not line.strip():
        continue
    res = re.search(regex, line)
    grupos = res.groups()
    # print(f"{i}º linha -> {grupos}")
    ano = grupos[0]
    if ano in dic:
        dic[ano] += 1
    else:
        dic[ano] = 1

# dic = dict(sorted(dic.items())) # ordenação pelo ano
dic = dict(sorted(dic.items(), key = lambda x:x[1])) # ordenação pelo numero de processos
# print(dic)
printTable("Frequência de processos por ano", "Ano", "Total", dic, width=5)
