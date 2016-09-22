%{
#include<stdio.h>
%}
%token D UMINUS
%left '+' '-'
%left '*' '/'
%right UMINUS
%left '(' ')'
%%
E : S {printf("%d", $$);};
S: S '+' S {$$ = $1 + $3;} | S '-' S {$$ = $1 - $3;} | S '*' S {$$ = $1 * $3;} | S '/' S {$$ = $1 / $3;} 
    | UMINUS S {$$ = - $2;}| '(' S ')'{$$ = $2;} | D {$$ = $1;};
%%
int yyerror() {
    printf("error!");
    return 1;
}
int main() {
    yyparse();
    printf("\n");
    return 0;
}
