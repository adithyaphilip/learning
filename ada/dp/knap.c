#include <stdio.h>
#define max(a,b) (a)>(b)?(a):(b)
int dp[100][100];
int maxKnap(int *w, int *v, int n, int cap) {
    if(dp[n][cap]!=-1) return dp[n][cap];
    int val = maxKnap(w,v,n-1,cap);
    if(w[n]<=cap) val = max(val,v[n] + maxKnap(w,v,n-1,cap-w[n]));
    return dp[n][cap] = val;
}

int main() {
    int t;
    scanf("%d",&t);
    while(t--) {
        int cap,n;
        scanf("%d %d",&cap, &n);
        int i;
        int w[n+1],v[n+1];
        int j;
        for(i=0;i<=n;i++)
            for(j=0;j<=cap;j++) {
                if(i==0||j==0)
                    dp[i][j]=0;
                else
                    dp[i][j]=-1;
            }
        for(i=1;i<=n;i++) {
            scanf("%d",&w[i]);
        }
        for(i=1;i<=n;i++) {
            scanf("%d",&v[i]);
        }
        printf("%d\n",maxKnap(w,v,n,cap));
    }
}
