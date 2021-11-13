#include<cstdio>
#include<ctime>
#include<algorithm>
using namespace std;
const int T=20;    
bool flag;
int num[11],a[11][11],b[11][11];
bool s[11],v[11][11],v1[11][11],v2[11][11],vv[82];
int check(int x,int y){
	if (x<4){
		if (y<4) return 1;
		if (y<7) return 2;
		return 3;
	}
	if (x<7){
		if (y<4) return 4;
		if (y<7) return 5;
		return 6;
	}
    if (y<4) return 7;
	if (y<7) return 8;
	return 9;
}
void dg(int x,int y){
	if (x==10){
		flag=1;
		return;
	}
	for (int i=1;i<=9;i++){
		if (!v[x][num[i]]&&!v1[y][num[i]]&&!v2[check(x,y)][num[i]]){
			a[x][y]=num[i];
			v[x][num[i]]=v1[y][num[i]]=v2[check(x,y)][num[i]]=1;
			if (y==9) dg(x+1,1);
			else dg(x,y+1);
			if (flag) return;
			v[x][num[i]]=v1[y][num[i]]=v2[check(x,y)][num[i]]=0; 
		}
	}
}
int main(){
//  	freopen("shudu.txt","w",stdout);
	srand((unsigned)time(NULL));
	for (int i=1;i<=9;i++){
	  while (!num[i]||s[num[i]]) num[i]=rand()%9+1;
	  s[num[i]]=1;
	}
	dg(1,1);
	for (int i=1;i<=T;i++)
  	{
  	   int x=rand()%81+1;
  	   while (vv[x]) x=rand()%81+1;	   
  	   vv[x]=1;
  	   a[x/9+1][x-x/9*9]=0;	
  	} 
  	for (int i=1;i<=9;i++)
  	{
  	  for (int j=1;j<=9;j++)
  	  printf("%d ",a[i][j]);
      printf("\n");
    }
}
