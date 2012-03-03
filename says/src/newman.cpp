#include <vector>
#include <tuple>
#include <string>
#include <fstream>
#include <iostream>

#include "graph.hpp"

using namespace std;

void readfrom(const string& path) {

  mlcommon::graph g;

	int s,f,t,w;
  ifstream ifs(path.c_str(), ios::in); {
    
    while (ifs >> s >> f >> w) {
      
      if (f < s) { t = s; s = f; f = t; }
      g.append_edge(s, f, w);
    }
    ifs.close();
  }

  const int numnodes = g.number_of_nodes();
  const int numlinks = g.number_of_edges();

  cout << numnodes << ", " << numlinks << endl;
}

int main(int argc, char* argv[]) {

  readfrom(argv[1]);

  return 0;
}
