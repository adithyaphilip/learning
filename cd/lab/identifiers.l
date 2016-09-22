%{
	#include<stdio.h>
	#include<stdlib.h>
	int i=0;
%}
letter[a-bA-Z]
digit[0-9]
%%
if|else|for|while {printf("Keyword\n");}
{letter}[letter|digit]+ i++;
%%
main(int argc,char **argv)
{
	
}
