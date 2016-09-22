import java.util.*;

public class All {
    public static void main(String[] args) {
        Stack<Integer> s = new Stack<>();
        s.push(1);
        s.push(2);
        System.out.println("STACK: " + s);
        System.out.println("PEEKING: " + s.peek());
        System.out.println("POPPING: " + s.pop());
        System.out.println("POPPING: " + s.pop());

        System.out.println();

        HashMap<String, Integer> hm = new HashMap<>();
        hm.put("abc",1);
        hm.put("def",3);
        hm.put("abc",2);
        System.out.println("HashMap: " + hm);
        System.out.println("HashMap value at abc is " + hm.get("abc"));
        System.out.println("HashMap value at def is " + hm.get("def"));

        System.out.println();
        
        Set<Integer> set = new HashSet<>();
        set.add(56);
        set.add(65);
        set.add(65);
        System.out.println("SET: " + set);
        for(int i:set) {
            System.out.println("SET: " + i);
        }

        System.out.println();

        LinkedList<Integer> l = new LinkedList<>();
        l.add(1);
        l.add(2);
        l.addFirst(3);
        System.out.println("LinkedList: " + l);

        for(int i:l) System.out.println("LinkedList: " + i);
        System.out.println("LinkedList POP: " + l.pop());
        System.out.println("LinkedList removeFirst: " + l.removeFirst());
        System.out.println("LinkedList: " + l);

        System.out.println();

        ArrayList<Integer> l2 = new ArrayList<>();
        l2.add(1);
        l2.add(2);
        l2.remove(1);

        System.out.println("ArrayList: " + l2);
        System.out.println("ArrayList Index Of 2: " + l2.indexOf(2));
        
        for(int i:l2) System.out.println("ArrayList: " + i);
    }
}
    

