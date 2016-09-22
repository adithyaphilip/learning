#include<stdio.h>
#include<limits.h>

int findMin(int arr[], int n)
{
    // Calculate sum of all elements
    int sum = 0; 
    for (int i = 0; i < n; i++)
        sum += arr[i];
 
    // Create an array to store results of subproblems
    bool dp[n+1][sum+1];
 
    // Initialize first column as true. 0 sum is possible 
    // with all elements.
    for (int i = 0; i <= n; i++)
        dp[i][0] = true;
 
    // Initialize top row, except dp[0][0], as false. With
    // 0 elements, no other sum except 0 is possible
    for (int i = 1; i <= sum; i++)
        dp[0][i] = false;
 
    // Fill the partition table in bottom up manner
    for (int i=1; i<=n; i++)
    {
        for (int j=1; j<=sum; j++)
        {
            // If i'th element is excluded
            dp[i][j] = dp[i-1][j];
 
            // If i'th element is included
            if (arr[i-1] <= j)
                dp[i][j] |= dp[i-1][j-arr[i-1]];
        }
    }
  
    // Initialize difference of two sums. 
    int diff = INT_MAX;
     
    // Find the largest j such that dp[n][j]
    // is true where j loops from sum/2 t0 0
    for (int j=sum/2; j>=0; j--)
    {
        // Find the 
        if (dp[n][j] == true)
        {
            diff = sum-2*j;
            break;
        }
    }
    return diff;
}

int main() {
    int t;
    scanf("%d", &t);
    int i;
    for (i = 0;i <t; i++) {
        int n;
        scanf("%d", &n);
        int j;
        int l1 = n +1  - (n+1)/2;
        int l2 = (n+1)/2;
        int a1[l1];
        int a2[l2];
/*        
        for(j=0;j<n+1;j++) {
            if (j%2 == 0) {
                scanf("%d", a1 + j/2);
  //              printf("a1:%d\n", a1[j/2]);
            } else {
                if (j==n) {
                    scanf("%d", a2 + j/2); 
                } else {
                scanf("%d", a2 + j/2); 
                }
    //          printf("a2:%d\n", a2[j/2]);
            }
            char c;
            if (j!=n) {
                scanf("%c", &c);
                scanf("%c", &c);
                scanf("%c", &c);
            }
        }
        */
for(j=0;j<2*n+1;j++) {
    if (j%2 == 0) {
        if(j%4 == 0) {
        scanf("%d", a1 + j/4);
        }
        else {
        scanf("%d", a2 + j/4);
        }
    } else {
        char c;
        scanf("%c", &c); 
    }
    
}
        printf("\n");
       for(j =0; j<l1;j++) {
          printf("%d ", a1[j]);
     }
     printf("\n");
    for(j =0; j<l2;j++) {
        printf("%d ", a2[j]);
   }
  printf("\n");
        
        int s1 = findMin(a1, l1);
        int s2 = findMin(a2, l2);
        printf("%d\n", s1 + s2);
    }
    
    return 0;
}
