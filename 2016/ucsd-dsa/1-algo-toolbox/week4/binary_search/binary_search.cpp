#include <iostream>
#include <cassert>
// #include <ctime>
#include <vector>
#include <algorithm>
#include <tuple>
#include <set>
#include <iterator>
#include <limits>

using namespace std;
typedef long long ll;
typedef unsigned long long ull;

using std::vector;

bool ascend(ll i, ll j) {
   return (i < j) ;
}

ll binary_search(const vector<ll> &a, ll x) {
   ll left = 0, right = (ll)a.size() - 1;
   ll mid;
   // cout << endl;
   while(left <= right)
   {
      mid = left + (right - left) / 2;
      // cout << "(" << left <<"-" << mid << "-" << right<< "  " << x << "=="<< a[mid] << ")" << "+";
      if (x < a[mid]) right = mid - 1;
      else if (x > a[mid]) left = mid + 1;
      else {
         // cout << endl;
         return mid;
      }
   }
   // cout << endl;
   return -1;
}

ll linear_search(const vector<ll> &a, ll x) {
   for (size_t i = 0; i < a.size(); ++i) {
      if (a[i] == x) return i;
   }
   return -1;
}

int main() {
/*
   ll start_s = 0;
   ll stop_s = 0;
   while (true) {

      cout << "=========" << endl;
      ll n = 1 + rand() % 10000; // 10E5
      cout << "n: "<< n << endl;
      set<ll> set_a;
      for (size_t i = 0; i < n; i++) {
         set_a.insert(rand() % 1000000000); //10E9
      }
      vector<ll> a(set_a.size());
      copy(set_a.begin(), set_a.end(), a.begin());
      n = a.size();

      // for (size_t i = 0; i < a.size(); i++) {
      //    cout << i << "-" << a[i] << " ";
      // } cout << endl;

      sort(a.begin(), a.end(), ascend);

      cout << "-----" << endl;
      ll m = rand() % n;
      cout << "m: " << m << endl;
      vector<ll> b(m);
      for (size_t i = 0; i < m; i++) {
         b[i] = a[rand() % m];
      }

      // for (auto i: b) cout << i << ' ';
      // cout << endl;

      cout << "-----" << endl;
      start_s = clock();
      vector<ll> res1(m);
      for (size_t i = 0; i < m; i++) {
         res1[i] = binary_search(a, b[i]);
      }

      // cout << "binary_search" << endl;
      // for (auto i: res1) cout << i << ' ';
      // cout << endl;

      stop_s = clock();
      cout << "binary_search:" << " time: " << (stop_s - start_s) / double(CLOCKS_PER_SEC) * 1000 << " ms" << endl;

      start_s = clock();
      vector<ll> res2(m);
      for (size_t i = 0; i < m; i++) {
         res2[i] = linear_search(a, b[i]);
      }

      // cout << "linear_search" << endl;
      // for (auto i: res2) cout << i << ' ';
      // cout << endl;

      stop_s = clock();
      cout << "linear_search:" << " time: " << (stop_s - start_s) / double(CLOCKS_PER_SEC) * 1000 << " ms" << endl;

      if (res1 == res2) {
         cout << "OK\n";
      }
      else {
         cout << "Wrong answer " << "\n";
         getchar();
         // break;
      }

      cout << "\n";
      // getchar();
   }
*/
     ll n;
     std::cin >> n;
     vector<ll> a(n);
     for (size_t i = 0; i < a.size(); i++) {
       std::cin >> a[i];
     }
     ll m;
     std::cin >> m;
     vector<ll> b(m);
     for (ll i = 0; i < m; ++i) {
       std::cin >> b[i];
     }
     for (ll i = 0; i < m; ++i) {
       //replace with the call to binary_search when implemented
       std::cout << binary_search(a, b[i]) << ' ';
     }

}
