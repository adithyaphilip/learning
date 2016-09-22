%{
#include "y.tab.h"
%}
%%
-[0-9]+ {yyless(1); return UMINUS;}
[0-9]+ {yylval=atoi(yytext); return D;}
. return yytext[0];
%%
