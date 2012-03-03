#include "lsh.hpp"

#include <fstream>
#include <vector>
#include <cmath>

using namespace std;

namespace {

  int const d = 2;
  
  int const k = 4; // ハッシュコード長
  int const L = 10;// バケット数
  int const r = 8; // Hash Parameter

  const int iteration = 10;
  
  typedef std::array<double, d> data_type;
}

double dist(const tuple<double, double>& p, const tuple<double, double>& q) {

  const double d = sqrt( pow(get<0>(p) - get<0>(q), 2.0) + pow(get<1>(p) - get<1>(q), 2.0) );
  return d;
}

void mean_shift(const vector< tuple<double, double> >& dataset, const double& kernel_size, LSH::pStable<double, k, L, d, r>& hash) {

  int counter = 0;
  for (vector< tuple<double, double> >::const_iterator x = dataset.begin(); x != dataset.end(); ++x) {
    //printf("%06d\n", counter++);

    tuple<double, double> mean(make_tuple(get<0>(*x), get<1>(*x)));
    
    for (int ii = 0; ii < iteration; ++ii) {

      int div = 0;
      tuple<double, double> nsum(make_tuple(0.0, 0.0));
     
      auto neighbor = hash.query(data_type{ get<0>(*x), get<1>(*x) });
      for (auto val: neighbor) {

        tuple<double, double> nei(make_tuple(val[0][0], val[0][1]));

        if (dist(nei, mean) <= kernel_size) {

          get<0>(nsum) += get<0>(nei);
          get<1>(nsum) += get<1>(nei);
          ++div;
        }
      }

      tuple<double, double> next_mean(make_tuple(
            get<0>(nsum) / static_cast<double>(div),
            get<1>(nsum) / static_cast<double>(div)));
    
      const double mdist = dist(mean, next_mean);
      get<0>(mean) = get<0>(next_mean);
      get<1>(mean) = get<1>(next_mean);
      
      if (mdist < 3.0e-5) { break; }
    }

    printf("%lf\t%lf\n", get<0>(mean), get<1>(mean));
  }
}


int main(int argc, char* argv[]) {

  LSH::pStable<double, k, L, d, r> hash;
  
  vector< tuple<double, double> > dataset;

  ifstream ifs(argv[1]);
  string buffer;
  while (ifs && getline(ifs, buffer)) {

    double x, y;
    sscanf(buffer.c_str(), "%lf\t%lf", &x, &y);
    //hash.add(data_type{ x, y });
    dataset.push_back(make_tuple(x, y));
  }

  for (vector< tuple<double, double> >::iterator i = dataset.begin(); i != dataset.end(); ++i) {
    hash.add(data_type{ get<0>(*i), get<1>(*i) });
  }

  mean_shift(dataset, 4.0, hash);
  /*
  auto result = hash.query(data_type{ get<0>(dataset[13]), get<1>(dataset[13]) });

  std::cout << "result:" << std::endl;
  for(auto val : result) {
    for(auto v : (*val)) {
      std::cout << v << ",";
    }
    std::cout << std::endl;
  }

  cout << "\n-----------------\n" << endl;
  */
}

