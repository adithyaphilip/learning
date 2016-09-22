#include<mcheck.h>
#include<stdlib.h>
f() {
    int *a = malloc(4);
    return 0;
}
int main() {
    mtrace();
    f();
    muntrace();
    return 0;
}
