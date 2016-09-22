%%
[A-Z] putchar('a'+(yytext[0]-'A'));
%%
int main(int argc, char* argv[]) {
	yyin = fopen(argv[1], "r");
	yylex();
	return 0;
}
