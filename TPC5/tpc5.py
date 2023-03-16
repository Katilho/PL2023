import ply.lex as lex
import re
import sys

saldo = 0

tokens = (
   'LEVANTAR',
   'POUSAR',
   'MOEDAS',
   'NUMERO',
   'ABORTAR'
)

states = (
   ('on','exclusive'),  # estado "on"
   ('off','exclusive'), # estado "off"
)

def printed_saldo(saldo: float):
    euro = int(saldo)
    try: # Se o saldo for maior que 1 euro, apresenta euro e centimos.
        cents = int(saldo%euro * 100)
   
    except ZeroDivisionError: # Se o saldo for menor que 1 euro, apresenta apenas os centimos.
        cents = int(saldo*100)

    res = f"{f'{euro}e' if euro>0 else ''}{cents}c"
    return res


def t_off_LEVANTAR(t):
    r'LEVANTAR'
    lexer.begin('on')
    print("MAQ: Introduza moedas.")

def t_on_ABORTAR(t):
    r'ABORTAR'
    global saldo
    # tratar de lógico de moedas a devolver - OPCIONAL
    print(f"MAQ: Troco = {printed_saldo(saldo)}; Volte sempre!")
    saldo = 0
    lexer.begin('off')

def t_on_POUSAR(t):
    r'POUSAR'
    global saldo
    # tratar de lógico de moedas a devolver - OPCIONAL
    print(f"MAQ: Troco = {printed_saldo(saldo)}; Volte sempre!")
    saldo = 0
    lexer.begin('off')

def t_on_MOEDAS(t):
    r"MOEDA (\s?(\d+[c|e]),?)+"
    global saldo
    err = ""
    moedas = t.value.split("A ")[1]
    arr = re.split(r"[,.] ?", moedas)
    for m in arr:
        value = int(m[:-1])
        if m[-1] == "c" and value in (1, 2, 5, 10, 20, 50):
            value /= 100
            saldo += value
        elif m[-1] == "e" and value in (1, 2):
            saldo += value
        else:
            err += f"{m} - moeda inválida; "
    print(f"MAQ: {err}Saldo = {printed_saldo(saldo)}")

    return t

def t_on_NUMERO(t):
    r'T=(\d{9}|00\d+)'
    global saldo
    grupos = t.lexer.lexmatch.groups()
    num = t.value.split("=")[1]

    if re.match("(?:601|641)\d+", num):
        print("MAQ: Chamada bloqueada (começa com 601 ou 641). Digite outro número.", end=" ")

    elif re.match("00\d+", num):
        if saldo>=1.5:
            saldo -= 1.5
        else:
            print(f"MAQ: Saldo inválido!", end=" ")

    elif num[0] == "2":
        if saldo>=0.25:
            saldo -= 0.25
        else:
            print("MAQ: Saldo inválido!", end=" ")

    elif re.match("800\d+", num):
        pass

    elif re.match("808\d+", num):  
        if saldo>=0.10:
            saldo -= 0.10
        else:
            print("MAQ: Saldo inválido!", end=" ")

    ## Outra chamada qualquer, defini que custa 50 cent.
    else: 
        if saldo>=0.50:
            saldo -= 0.50
        else:
            print("MAQ: Saldo inválido!", end=" ")
    
    print(f"Saldo = {printed_saldo(saldo)}")
    return t

# Define a rule so we can track line numbers
def t_ANY_newline(t):
    r'\n+'
    # t.lexer.lineno += len(t.value)

t_ANY_ignore  = ' \t'

def t_ANY_error(t):
    skiped_token = re.split(r" \n", t.value, 1)[0]
    print(f"MAQ: Illegal input: {skiped_token}")
    t.lexer.skip(len(skiped_token))


## MAIN ##

lexer = lex.lex()

# Set the initial state of the lexer to 'off'
lexer.begin('off')

for data in sys.stdin:
    lexer.input(data)
    tok = lexer.token()

