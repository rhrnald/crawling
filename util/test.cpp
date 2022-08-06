#include "bits/stdc++.h"
using namespace std;
int a[50];
int b[50];
string s;
int main(void) {
	const int block_size=48259;
	for(int i=0; i<40; i++) a[i] = i*block_size;
	int idx=0;
	while(cin >> s) {
		int len = s.size();
		int cur=stoi(s.substr(0, len-4));
		if(cur>a[idx+1]) idx++;
		b[idx] = cur;	
	}
	for(int i=0; i<32; i++) printf("%d,", b[i]);
	printf("\n");
	for(int i=0; i<32; i++) printf("%d,", a[i]);
}
