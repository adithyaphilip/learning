public class Main {
    public static void main(String[] args) {
        f(1,2);
    }
    public static void f(int... a) {
        System.out.print(a.length);
    }
}
