from ply import lex
from ply import yacc


tokens = ["B1", "B2", "B3", "CB1", "CB2", "CB3"]
t_B1 = r"\("
t_B2 = r"\["
t_B3 = r"\{"
t_CB1 = r"\)"
t_CB2 = r"\]"
t_CB3 = r"\}"

def t_error(t):
    t.lexer.skip(1)

error = False

def p_expr(p):
    '''S : B1 S CB1 S
        | B2 S CB2 S
        | B3 S CB3 S
    S : '''
    
def p_error(p):
    error = True
    print("Invalid!")

lexer = lex.lex()
parser = yacc.yacc()
inp = input()
parser.parse(inp)
if not error: print("Valid!")
