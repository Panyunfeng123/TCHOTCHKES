#include<cstdio>
#include<cmath>
using namespace std;
int n,ans;
int main()
{	
	scanf("%d",&n);
//	for (int i=1;i<=n;i++)
//		for (int j=i+1;i+j<=n;j++)
//		{
//			s=sqrt(i*i+j*j);
//			if ((int)s>i+j||i+j+(int)s>n) break;
//			if (s==(int)s) ans++;
//		}
	for (int i=2;i<=n;i++)
	{
		int x=i*i;
		for (int j=i;j>=1&&x/j+i<=n;j-=2)
			if (x%j==0) 
				if (x-j*j>i*j*2) 
					if ((x/j-j)%2==0)
						ans++;	
	}
	printf("%d",ans);
}
