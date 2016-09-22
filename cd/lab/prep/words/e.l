%{
#include<stdio.h>
int words = 0, c = 0, lines = 0, spaces = 0;
%}
l [a-zA-Z]
d [0-9]
%%
{l}({l}|{d})* {words++; c+=yyleng;}

%%
int yywrap() {
    printf("%d %d\n", words, c);
    return 1;
}
