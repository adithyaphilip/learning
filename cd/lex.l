%{
   #include"y.tab.h"
   #include<string.h>
%}
%%
[a-z] {return ID;}
[0-9]+"."[0-9]+f {return FNUM;} 
[0-9]+"."[0-9]+ {return DNUM;} 
[0-9]+ {return NUM;} 
[+"-"*/] {return OPR;} 
= {return EQ;}
%%
int yywrap(){
return 1;
}

