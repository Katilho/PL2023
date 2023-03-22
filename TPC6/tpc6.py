import ply.lex as lex
import sys

tokens = (
    'TYPE', ###
    'VARIAVEL', ###
    'PONTOVIRG',#
    'VIRGULA',#
    'FUNCTIONNAME',#
    'FOR',#
    'WHILE',#
    'IF',
    'NUMBER',###
    'PLUS',#
    'MINUS',###
    'TIMES',#
    'DIVIDE',#
    'PAROPEN',#
    'PARCLOSE',#
    'CHAVOPEN',#
    'CHAVCLOSE',#
    'RETOPEN',#
    'RETCLOSE',#
    'ATRIB',#
    # 'EQUALS',
    'MENOR',#
    'MAIOR',#
    'COMMENT',
    'COMMENTBLOCK',
    'RETS'#
)

t_PONTOVIRG = r'\;'
t_VIRGULA = r'\,'
t_NUMBER = r'\d+'###
t_PLUS = r'\+'
t_MINUS = r'\-'###
t_TIMES = r'\*'
t_DIVIDE = r'\/'
t_PAROPEN = r'\('
t_PARCLOSE = r'\)'
t_CHAVOPEN = r'{'
t_CHAVCLOSE = r'}'
t_RETOPEN = r'\['
t_RETCLOSE = r'\]'
t_ATRIB = r'\='
# t_EQUALS = r'\={2}'
t_MENOR = r'\<'
t_MAIOR = r'\>'
t_RETS = r'\.{2}'
t_VARIAVEL = r'[a-z_]\w*'


def t_TYPE(t):
    r'(int|float|double|long|short|void|char|string|bool|program|function)'
    return t

def t_FUNCTIONNAME(t):
    r'(?<=function\s)[a-z_]\w*|[a-z]\w*(?=(?=\()|(?=\{))'
    # r'[a-z]\w*(?=(?=\()|(?=\{))'
    return t

def t_FOR(t):
    r'for'
    return t

def t_WHILE(t):
    r'while'
    return t

def t_IF(t):
    r'if'
    return t

### Comentários

def t_COMMENT(t):
    r'\/\/.*'
    return t # Suposto ignorar, mas para verificar a captura são identificados

def t_COMMENTBLOCK(t):
    r'/\*(.|\n)*?\*/'
    return t # Suposto ignorar, mas para verificar a captura são identificados

t_ignore = ' \t\n'

def t_error(t):
    print(f"Carater Ilegal {t.value[0]}")
    t.lexer.skip(1)

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)



### MAIN ###
lexer = lex.lex()

with open("example1.txt") as f:
    ex1:str = f.read()
with open("example2.txt") as f:
    ex2:str = f.read()

print("-"*20,"EXEMPLO 1 - example1.txt","-"*20)
lexer.input(ex1)
for tok in lexer:
    print(tok)

print()

print("-"*20,"EXEMPLO 2 - example2.txt","-"*20)
lexer.input(ex2)
for tok in lexer:
    print(tok)
