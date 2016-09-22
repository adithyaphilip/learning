%{
int c=0;
%}
%%
"/*"([^*]|(\*+[^*/]))*\*+\/|"//".* c++;
%%
int main() {
    yylex();
    printf("%d", c); 
}
int yywrap() {
    return 1;
}
