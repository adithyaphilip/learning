%{
#include<stdio.h>
%}
%%
.* { yyless(0); printf("\nS: %s\n", yytext);}
