#include<stdio.h>
#include<string.h>
int fact(int, int);
char* rev(char *a, int l, char *s) {
    if(l<=1) return s;
    char t = a[0];
    a[0] = a[l-1];
    a[l-1] = t;
    return rev(a+1,l-2,s);
}
int main() {
    int f;
    f = fact(f,1);
    //scanf("%d",&f);
    printf("%d\n",f);
    char c[100];
    scanf("%s",c);
    printf("%s\n", rev(c,strlen(c),c));
}

int fact(int n, int p) {
    if (n==0) return p;
    return fact(n-1, p*n);
}
