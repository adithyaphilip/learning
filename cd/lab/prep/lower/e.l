%{
#include <stdio.h>
#include<stdlib.h>
%}
%%
[A-Z] printf("%c", yytext[0]-'A'+'a');
%%
int main() {
    yyin = fopen("in", "r");
    yylex();
    fclose(yyin);
}
