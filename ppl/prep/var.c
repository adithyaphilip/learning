#include<stdio.h>
#include<stdarg.h>
int f(int num, ...) {
    va_list list;
    va_start(list, num);
    int sum = 0;
    while (num--)
        sum+=va_arg(list, int);
    return sum;
    va_end(list);
}

int main() {
    printf("%d", f(3,1,2,3,4));
    return 0;
}
