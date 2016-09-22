static int x;

int* test() {
    static int a;
    return &a;
}
int main() {
    static int y;
    static float z;
    static char d;
    int p;
    int a = *test();
    a = 10;
}
