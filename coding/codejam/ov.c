#include <stdio.h>
int main() {
    int t,ti=t;
    scanf("%d",&t);
    for(ti=1;ti<=t;ti++) {
	int n;
	scanf("%d",&n);
	char s[n+1];
	scanf("%s",s);
	int friends = 0;
	int clappers = s[0]-'0';
	int i;
	for(i=1;i<=n;i++) {
	    int pep = s[i]-'0';
	    if(clappers<i) {
		friends += i - clappers;
		clappers = i + pep;
	    }
	    else {
		clappers += pep;
	    }
	}
	printf("Case #%d: %d\n",ti,friends);
    }
    return 0;
}
