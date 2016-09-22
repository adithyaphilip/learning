import java.util.Scanner;

public class ShynessFriends {

       public static void main(String[] args){
               Scanner in = new Scanner(System.in);
               int t = in.nextInt();
               for(int i=0;i<t;i++){
               int n = in.nextInt();//Size of the array +1
               int num = in.nextInt();//The array itself with size n+1;
               int size = n+1;
               splitprint(num, size);
               }
       }
       
       public static void splitprint(int ar, int n){
               
               int[] array = new int[n];
               int count = n-1;
               
               while(ar>0){
                       array[count--] = ar%10;
                       ar = ar/10;
               }
               
               //display(array, n);
               findnumfriends(array, n);
       }
       
       public static void findnumfriends(int[] a, int n){
               /**
                * Given n the size of the array or the max shyness level
                * and the array a where the shyness level of a[k] persons is k
                */
               int numf = 0;
               int case1 = 0;
               int memgotup = 0;
               for(int i=0;i<n;i++){
                       if(i<=memgotup)
                       {
                               memgotup +=  a[i];
                       }
                       else
                       {
                               numf += i-memgotup;
                               memgotup += numf+a[i];
                       }
               }
               //case1++;
               System.out.println("Case #"+case1+": "+numf);
               //case1++;
       }
       
}
