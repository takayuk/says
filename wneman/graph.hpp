#pragma once

#include <vector>
#include <tuple>
#include <unordered_map>

namespace mlcommon {

  using namespace std;

  struct hash_eq
    : binary_function< std::tuple<int, int>, std::tuple<int, int>, bool > {

      bool operator()(const std::tuple<int, int>& x, const std::tuple<int, int>& y) const {
        return get<0>(x) == get<0>(y) && get<1>(x) == get<1>(y);
      }
  };

  class edge_hash
    : unary_function< std::tuple<int, int>, size_t > {

      private:
        const hash<int> h_int;

      public:
        edge_hash(): h_int() {}
        size_t operator()(const std::tuple<int, int>& p) const {

          size_t seed = h_int(get<0>(p));
          return h_int(get<1>(p)) + 0x9e3779b9 + (seed<<6) + (seed>>2);
        }
  };

  class graph {

    private:
      unordered_map< std::tuple<int, int>, int, edge_hash, hash_eq > edges_;
      unordered_map< int, vector<int> > adj_;
      int maxid_;

    public:
      graph() {}
      ~graph() {}

      void append_edge(const int& u, const int& v, const int& w) {

        const std::tuple<int, int> e(make_tuple(u, v));
        
        const bool edge_exists = (edges_.end() != edges_.find(e));
        if (!edge_exists) {
      
          edges_[e] = w;

          const bool u_exists = (adj_.end() != adj_.find(u));
          if (!u_exists) {
            adj_[u] = vector<int>(1, v); 
            if (u > this->maxid_) { this->maxid_ = u; }
          }
          else {
            adj_[u].push_back(v);
          }
          const bool v_exists = (adj_.end() != adj_.find(v));
          if (!v_exists) {
            adj_[v] = vector<int>(1, u); 
            if (v > this->maxid_) { this->maxid_ = v; }
          }
          else {
            adj_[v].push_back(u);
          }
        }
      }
      
      bool has_edge(const int& u, const int& v) const {

        const std::tuple<int, int> e(make_tuple(u, v));

        const bool exists = (edges_.end() != edges_.find(e));
        if (exists) {
          return true;
        }
        else {
          return false;
        }
      }

      int degree(const int& u) {

        return 0;
      }

      int eachnode() {

        return 0;
      }

      void nodes(vector<int>& ids) {
        /*
        for (unordered_map< int, unordered_map<int, int> >::iterator i = adj.begin(); i != adj.end(); ++i) {
          ids.push_back(i->first);
        }
        */
      }
      
      void edges(const int& u, vector< std::tuple<int, int> >& v_ids) const {

        /*
        if (adj.end() == adj.find(u)) { return; }
        
        unordered_map< int, unordered_map<int, int> >::const_reference ref = *(adj.find(u));
        for (unordered_map<int, int>::const_iterator i = ref.second.begin(); i != ref.second.end(); ++i) {

          v_ids.push_back(make_tuple(i->first, i->second));
        }
        */
      }

      size_t number_of_nodes() const { return this->adj_.size(); }
      size_t number_of_edges() const { return this->edges_.size(); }
      
      int maxid() const { return this->maxid_; }
  };
}


