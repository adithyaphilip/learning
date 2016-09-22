#include<stdio.h>
#include<mcheck.h>
#include<stdlib.h>
#include<setjmp.h>
jmp_buf j;
void f() {
//    longjmp(j, 2);
    printf("Hello!");
    int *a = malloc(sizeof(int));
    printf("Hello!");
    printf("Hello!");
}
int main() {
    mtrace();
    typedef int myint;
    //if(setjmp(j)==0) 
    f(); 
    myint a = 1;
    int b = a;
    muntrace();
}
