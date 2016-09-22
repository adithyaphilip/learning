%{
#include<stdio.h>
#include<stdlib.h>
int max = 0;
%}
%token IF COND OB CB OFB CFB
%%
S: IF OB COND CB OFB S CFB { $$ = $6 + 1; max = $$;}
    | { $$ = 0; }
%%
int yyerror() {
    printf("Error!\n");
    exit(0);
}
int main() {
    yyparse();
    printf("Nesting level = %d", max);
    return 0;
}

