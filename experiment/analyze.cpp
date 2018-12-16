#include <cstdio>
#include <iostream>
#include <string>

using namespace std;

int main() {
  string line, lastline;
  while (getline(cin, line)) {
    if (line[0] == '[' && line[2] == ']') cout<<line<<endl;
    if (line[0] == '#' && line.length() == 7) cout<<lastline<<endl;
    lastline = line;
  }
  return 0;
}