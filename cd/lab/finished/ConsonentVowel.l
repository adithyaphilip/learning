%{
#include<stdio.h>
 int v=0,c=0;
%}
%%
[aeiouAEIOU] v++;
[a-zA-Z] c++;
%%
int main(int argc, char *argv[]) {
	if (argc<2) {
		printf("No file supplied");
		return 1;
	}
	yyin = fopen(argv[1], "r");
	yylex();
	fclose(yyin);
}
int yywrap() {
	printf("V: %d C: %d\n", v, c);
	return 1;
}
