%{
#include<stdio.h>
int comments = 0;
%}
%%
"/*"([^*]|"*"+[^*/])*"*"+"/" comments++;
%%
int yywrap() {
    printf("%d\n", comments);
    return 1;
}
