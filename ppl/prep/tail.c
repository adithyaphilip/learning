#include<stdio.h>
int f(int p, int n) {
    if (n==0) return p*1;
    return f(p*n, n-1);
}

int main() {
    printf("%d\n", f(1,6));
    return 0;
}
