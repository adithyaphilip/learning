public class jvar {
    public static void main(String[] args) {
        int b[] = {1,2,3};
        System.out.println(sum(b));
        // sum(1,2,3.0);
        int[] a = {1,2};
        r(1,a);
    }
    public static int sum(int... a) {
        int sum= 0;
        for(int i:a) sum+=i;
        return sum;
    }
    public static void r(Object... o) {
        for(Object i:o) System.out.println(i);
    }
}
