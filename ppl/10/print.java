import java.util.*;
public class print {
    public static void main(String[] args) {
        print(1);
        print(1.0);
        print("hmm");
        printN(1);
        printN(1.0);
        //printN("hmm");//error due to extends
        List<Integer> i = new ArrayList<>();
        i.add(1);
        List<Float> f = new ArrayList<>();
        f.add(2.0f);

        //printf(i);//error due to wildcard bound
        printf(f);
        printd(i);
        printd(f);
    }
    public static<T> void print(T obj) {
        System.out.println(obj);
    }
    public static<T extends Number> void printN(T obj) {
        System.out.println(obj);
    }

    public static void printf(List<? super Float> a) {
        System.out.println(a);
    }

    public static void printd(List<? extends Number> a) {
        System.out.println(a);
    }
}
