import java.util.*;
public class Class<T,V> {
    
    public static void main(String[] args) {
        Class <Integer, Float> c= new Class<>();
        c.m(1);
        // c.m(1.0f); //float cannot be converted to an integer
        c.m2(1.0f);
        List<String> l = new ArrayList<>();
        String s = new String("a");
        String s2 = new String("a");
        l.add("b");
        l.add("c");
        l.add(s);
        l.add(s2);
        l.add("d");
        System.out.println(l);
        Collections.sort(l);
        if (l.get(0)==s) System.out.println("In place!");
        else System.out.println("Not in place!");
        System.out.println(l);
        c.m3("hello");
    }

    public void m(T i) {
        System.out.println(i);
    }

    public void m2(V i) {
        System.out.println(i);
    }

    public <V>void m3(V l) {
        System.out.println("Generic method: " + l);
    }
}

