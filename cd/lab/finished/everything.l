%{
	int l=0,sp=0,c=0,w=0;
%}
%%
[ ] {sp++; c++;}
\n l++;
[a-zA-Z]+ {w++; c+=yyleng;}
%%
int main(int argc, char *argv[]) {
	yyin = fopen(argv[1], "r");
	yylex();
	printf("Lines: %d Spaces: %d Chars: %d Words: %d", l, sp, c, w);
	return 0;
}
