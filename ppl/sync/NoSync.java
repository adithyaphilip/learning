public class NoSync {
    public static void main(String args[]) throws Exception {
        Runnable r1 = new Runnable() {
            @Override
            public void run() {
                for (int i = 0;i<100;i++) {
                    for(int j = 0;j<2000000000;j++);
                    System.out.println("Thread1");
                }
            }
        };
        Runnable r2 = new Runnable() {
            @Override
            public void run() {
                for (int i = 0;i<100;i++) {
                    for(int j = 0;j<2000000000;j++);
                    System.out.println("Thread2");
                }
            }
        };
        new Thread(r1).start();
        new Thread(r2).start();
    }
}

