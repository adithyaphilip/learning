public class Sync {
    private Integer deadlock1; Thread dead1, dead2;
    private Integer deadlock2;
    public static void main(String args[]) throws Exception {
        new Thread() {
            @Override
            public void run() {
                print("Thread1");
            }
        }.start();
        new Thread() { 
            @Override
            public void run() {
                print("Thread2");
            }
        }.start();
        Runnable r = new Runnable() {
            @Override
            public void run() {
                print("Hello"+Math.random());
            }

            public void print(String s) {
                synchronized(this) {
                for(int i = 0; i< 5;i++) {
                try{Thread.sleep(100);System.out.println(s);}catch (Exception e){}
                }
                }
            }
        };
        new Thread(r).start();
        Thread t2 = new Thread(r);
        t2.start();
        t2.join();
        System.out.println("FINISHED!");
        Thread th = new Thread() {
            @Override
            public void run() {
                try{Thread.sleep(2000);}catch(Exception e) {}
    //                notify();
                try{Thread.sleep(5000);} catch (Exception e) {}
                System.out.println("Notifying thread");
            }
        };
        th.start();
//        th.wait();
        System.out.println("Finished waiting!");
        Thread.currentThread().join();//deadlock
    }

    public static synchronized void print(String out) {
        for(int i = 0;i<100;i++) {
            System.out.println(out);
        }
    }
}

