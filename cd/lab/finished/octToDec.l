%%
[0-7]+ {printf("%d", octToDec(yytext));}
%%
int main(int count, char *argv[]) {
	yyin = fopen(argv[1], "r");
	yylex();
	return 0;
}
int octToDec(char *oct) {
	int i = 0, sum =0;
	while(oct[i] != '\0') {
		sum = 8*sum + oct[i++] - '0';
	}
	return sum;
}
