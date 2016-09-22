import ply.lex as lex
import ply.yacc as yacc

tokens = ["NUMBER", "PLUS", "MINUS", "DIV", "MUL"]

def t_NUMBER(t):
    r"\d+"
    t.value = int(t.value)
    return t

t_PLUS = r'\+'
t_MINUS = r"-"
t_DIV = r"/"
t_MUL = r"\*"


def p_exp_plus(p):
    '''expr : NUMBER PLUS NUMBER'''
    p[0] = p[1] + p[3]
    print(type(p))

def t_error(p):
    print("ERROR N00B:", p)

lexy = lex.lex()
parser = yacc.yacc()
res = parser.parse("3+4")
print(res)
