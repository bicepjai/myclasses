#include <iostream>
#include <cassert>
// #include <ctime>
#include <vector>
#include <algorithm>
#include <tuple>
#include <map>
#include <set>
#include <iterator>
#include <climits>

typedef unsigned long long ull;
typedef long long ll;

using namespace std;

vector<ll> MappedMinMoves(ll n) {
   map<ll, ll> bottom_up_map;
   vector<ll> current;
   current.push_back(n);
   bottom_up_map.insert(make_pair(n, n));

   auto iter = bottom_up_map.find(1) ;
   while (iter == bottom_up_map.end())
   {
      vector<ll> next;

      // cout << endl << "current" << " -->";
      // for (size_t i = 0; i < current.size(); ++i) cout << current[i] << " ";
      // cout << endl;

      for (ll x : current) {
         // cout << x << " ==> ";
         auto iter3 = bottom_up_map.find(x / 3) ;
         if (x % 3 == 0 && iter3 == bottom_up_map.end()) {
            next.push_back(x / 3);
            bottom_up_map.insert(make_pair(x / 3, x));
            // cout << x / 3 << " ";
         }

         auto iter2 = bottom_up_map.find(x / 2) ;
         if (x % 2 == 0 && iter2 == bottom_up_map.end()) {
            next.push_back(x / 2);
            bottom_up_map.insert(make_pair(x / 2, x));
            // cout << x / 2 << " ";
         }

         auto iter1 = bottom_up_map.find(x - 1) ;
         if (iter1 == bottom_up_map.end()) {
            next.push_back(x - 1);
            bottom_up_map.insert(make_pair(x - 1, x));
            // cout << x-1 << " ";
         }
      }
      // cout << endl << "next" << " -->";
      // for (size_t i = 0; i < next.size(); ++i) cout << next[i] << " ";
      // cout << endl;

      current = next;
      // cout << endl << "-----" << endl;

      iter = bottom_up_map.find(1) ;
   }

   // getting path by backtracking bottom up map
   vector<ll> path;
   path.push_back(1);
   ll x = 1;
   ll y = bottom_up_map[x];
   while (x != y) {
      path.push_back(y);
      x = y;
      y = bottom_up_map[x];
   }
   return path;
}

int main() {

   ll n ;
   cin >> n;
   // ll n = 932344253;

   vector<ll> sequence = MappedMinMoves(n);
   std::cout << sequence.size() - 1 << std::endl;
   for (size_t i = 0; i < sequence.size(); ++i) cout << sequence[i] << " ";
}
