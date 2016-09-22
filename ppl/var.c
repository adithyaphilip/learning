#include <stdarg.h>
#include<stdio.h>
int sum(int,...);
int main() {
    printf("%d\n", sum(3,1,2,3.0));
    return 0;
}
int sum(int count, ...)
{
    va_list ap;
    int j;
    double tot = 0;
    va_start(ap, count); //Requires the last fixed parameter (to get the address)
    for(j=0; j<count; j++) {
        if (j>=2) tot += va_arg(ap, double);
        else tot+=va_arg(ap, int); //Requires the type to cast to. Increments ap to the next argument.
    }
    va_end(ap);
    return tot;
}
