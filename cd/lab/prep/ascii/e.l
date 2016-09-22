%{
#include<stdio.h>
#include<ctype.h>
%}
%%
.|\n if(!isprint(yytext[0])) printf("%d\n",yytext[0]);
