#include <cstdio>
#include <iostream>
#include <string>

using namespace std;

int main() {
  string line, lastline;
  char x = '-';
  double subsum[20];
  int subtop = -1;
  while (getline(cin, line)) {
    if (line[0] == '[' && (line[2] == ']' || line[3] == ']')) {
      cout<<line<<endl;
      if (line[1] != x) {
        subsum[++subtop] = 0;
        x = line[1];
      }
    }
    if (line[0] == '#' && line.length() == 7) {
      cout<<lastline<<endl;
      subsum[subtop] += stod(lastline);
    }
    lastline = line;
  }
  double avg = 0;
  cout.precision(9);
  cout<<'['<<endl;
  for (int i=0;i<=subtop;i++) {
    avg += subsum[i];
    cout<<fixed<<subsum[i]<<endl;
  }
  cout<<']'<<endl;
  avg/=(subtop+1);
  cout<<"average: "<<fixed<<avg<<endl;
  return 0;
}