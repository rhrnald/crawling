#include "bits/stdc++.h"
using namespace std;
int l[50];
int r[50];
int b[50];
string s;

const int start_idx = 1;
const int end_idx = 3445333;
const int total_num= end_idx-start_idx+1;
const int thread_num= 32;
const int block_size=int((total_num+thread_num-1)/thread_num);

int main(void) {
	for(int i=0; i<40; i++) l[i] = start_idx+block_size*i;
	for(int i=0; i<40; i++) b[i] = l[i];
	int idx=0;
	while(cin >> s) {
		int len = s.size();
		int cur=stoi(s.substr(0, len-4));
		while(cur>=l[idx+1]) idx++;
		b[idx] = cur;	
	}
	for(int i=0; i<32; i++) printf("%d/(%d,%d) - (%2.2f %%)\n", b[i], l[i], l[i+1], 1.0*(b[i]-l[i])/(l[i+1]-l[i]));
	for(int i=0; i<32; i++) printf("%d,", b[i]+1);
	printf("\n");
}
