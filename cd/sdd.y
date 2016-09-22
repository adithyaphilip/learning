// sdd is below

%{
  #include<stdlib.h>
  #include<stdio.h> 
extern char* yytext;
%}
%token IF COND OP CL statement ELSE ID FUNC INT FLOAT DOUBLE Return OPR EQ NUM FNUM DNUM
%left OPR EQ

%%
EXPR:EXPR OPR EXPR  {printf("EXPR-> EXPR OPR EXPR");}
    |EXPR EQ EXPR   {printf("EXPR-> EXPR EQ EXPR");}
    |ID     {printf("EXPR-> ID");}
    |NUM    {printf("EXPR-> NUM");}
    |FNUM   {printf("EXPR-> FNUM");}
    |DNUM {printf("EXPR-> DNUM");}
    ;   
%%
int yyerror(char* x){
    printf("INVALID\n");
        exit(0);
}
int main(){
        int i=yyparse();
}

