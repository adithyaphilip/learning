#include<stdio.h>
#include<string.h>
void solve(int,int,char[]);
char s[3*10000];
int main() {
    scanf("%s",s);
    int q;
    scanf("%d", &q);
    while(q--) {
        int m, l;
        scanf("%d %d", &m,&l);
        solve(m,l,s);
    }
    return 0;
}
    void solve(int m, int l, char s[]) {
        int ctr = 0;
        int i;
        int dp[5020];
        int dp2[5020];
        for(i=0;i<5020;i++) {
            dp[i] = -1;
            dp2[i] = -1;
        }
        int prev = 0;
        int j,t;
        for(i = 0;s[i]!='\0';i++) {
            for(j = i; s[j]!='\0'; j++) {
                int curr;
                if (i==j) {
                    t = s[i]-'0';
                    if(dp[t]==-1) {
                        dp[t]=t%m;
                    }
                    curr = dp[t];
                } else { 
                    t = (prev<<3) + (prev<<1) + s[j] - '0';
                    //printf("%d\n",t);
                    if(dp[t]==-1) dp[t] = t%m;
                    curr = dp[t];
                }
                prev = curr;
                if (curr==l) ctr++;
            }
        }
        printf("%d\n",ctr);
    }
