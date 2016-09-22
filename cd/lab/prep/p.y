%{
#include<stdio.h>
#include<stdlib.h>
int max = 0;
%}
%token A B
%%
S : A S B {$$ = $2 + 1; max = $$; }
    | {$$ = 0;}
    ;
%%
int yyerror() {
    printf("Error!\n");
    exit(0);
}

int main() {
    yyparse();
    printf("n = %d", max);
    return 0;
}
