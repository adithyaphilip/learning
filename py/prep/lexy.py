import ply.lex as lex
tokens = ["ID", "OP"]
t_ignore = " \t"
t_ID = "[a-zA-Z0-9]+"
t_OP= r"--|[+-><*/]"

def t_error(t):
    t.lexer.skip(1)

lexer = lex.lex()
s = input()
lexer.input(s)

while True:
    tok = lexer.token()
    if not tok:
        break
    print((tok.value, tok.type), end="")
print()

