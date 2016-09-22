import java.util.*;
public class Solution {
	public static void main(String args[]) {
		Scanner sc = new Scanner(System.in);
		int t = sc.nextInt();
		for(int ti = 1; ti<=t;ti++) {
			int d = sc.nextInt();
			int pancakes[] = new int[d];
			for(int i =0;i<d;i++) {
				//System.out.println("LOL"+i);
				pancakes[i] = sc.nextInt();
			}
			int eaten = 0;
			int time = 0;
			
			for(Arrays.sort(pancakes);pancakes[pancakes.length-1]!=0;Arrays.sort(pancakes)) {
				int max = pancakes[pancakes.length-1];
				int min = pancakes[0];
				if(min==0&&max>2) {
					pancakes[0] = pancakes[pancakes.length-1]/2;
					pancakes[pancakes.length-1] -= pancakes[0];
				}
				else if(max>2) {
					int pancakes2[] = new int[pancakes.length+1];
					for(int i=0;i<pancakes.length;i++)
						pancakes2[i] = pancakes[i];
					pancakes2[pancakes.length] = pancakes[pancakes.length-1]/2;
					pancakes2[pancakes.length-1] -= pancakes2[pancakes.length];
					pancakes = pancakes2;
				}
				else {
					for(int i =0;i<pancakes.length;i++) pancakes[i]-=1;
				}
				time++;
			}
			System.out.printf("Case #%d: %d\n",ti,time);
		}
	}
}
