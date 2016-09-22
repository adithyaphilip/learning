#include <stdio.h>
int bc[100][100];
int comb(int n, int k) {
    if(bc[n][k]!=0) return bc[n][k];
    if(k==0 || k==n) return 1;
    return comb(n-1,k-1) + comb(n-1,k);
}
int main() {
    int t;
    scanf("%d",&t);
    while(t--) {
        int i,j,n,k;
        scanf("%d %d",&n,&k);
        for(i=0;i<n;i++)
            for(j=0;j<k;j++)
                bc[i][j]=0;
        printf("%d",comb(n,k));
    }
}
