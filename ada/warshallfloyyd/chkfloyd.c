#include<stdio.h>
#define min(a,b) (a)>(b)?(b):(a);
void goFloyd(int n,void* rpt, void* rnt, int k) {
    int (*rp)[n] = rpt;
    int (*rn)[n] = rnt;
    int i,j;
    for(i=0;i<n;i++) {
	for(j=0;j<n;j++) {
	    rn[i][j] = min(rp[i][j],rp[i][k] + rp[k][j]);
	}
    }
}
int main() {
    int t;
    scanf("%d",&t);
    while(t--) {
	int n;
	scanf("%d",&n);
	int rp[n][n];
	int i,j;
	for(i=0;i<n;i++) {
	    for(j=0;j<n;j++) {
		scanf("%d",&rp[i][j]);
	    }
	}
	int k;
	int rn[n][n];
	for(k=0;k<n;k++) {
	    goFloyd(n,rp,rn,k);
	    for(i=0;i<n;i++) {
		for(j=0;j<n;j++) {
		    rp[i][j] = rn[i][j];
		}
	    }
	}
	for(i=0;i<n;i++) {
		if(rp[i][i]<0) {
			printf("NEGATIVE CYCLE!");
			return;
		}
	}
	for(i=0;i<n;i++) {
	    for(j=0;j<n;j++) {
		printf("%d ",rp[i][j]);
	    }
	    printf("\n");
	}
    }
}
