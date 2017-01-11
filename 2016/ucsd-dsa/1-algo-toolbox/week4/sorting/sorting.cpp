#include <iostream>
#include <cassert>
// #include <ctime>
#include <vector>
#include <algorithm>
#include <tuple>
#include <set>
#include <iterator>
#include <limits>

typedef unsigned long long ull;
typedef long long ll;

using namespace std;

ll partition2(vector<ll> &a, ll l, ll r) {
  ll x = a[l];
  ll j = l;
  for (ll i = l + 1; i <= r; i++) {
    if (a[i] <= x) {
      j++;
      swap(a[i], a[j]);
    }
  }
  swap(a[l], a[j]);
  return j;
}

void randomized_quick_sort2(vector<ll> &a, ll l, ll r) {
  if (l >= r) {
    return;
  }

  ll k = l + rand() % (r - l + 1);
  swap(a[l], a[k]);
  ll m = partition2(a, l, r);

  randomized_quick_sort2(a, l, m - 1);
  randomized_quick_sort2(a, m + 1, r);
}

tuple<ll, ll> partition3(vector<ll> &a, ll l, ll r) {
   ll x = a[l];
   ll end = l;
   ll start = l;

   // cout << "before: ";
   // for (size_t i = l; i <= r; ++i) cout << a[i] << ' ';
   // cout << endl;

   for (ll i = l + 1; i <= r; i++) {

      // cout << "-------- "<< i << endl;
      if (a[i] < x) {
         // cout << "lesst:  ";
         swap(a[i], a[start]);
         start++;
         end++;
         swap(a[i], a[end]);
      }
      else if (a[i] > x) {
         // cout << "great:  ";
      }
      else {
         // cout << "equal:  ";
         end++;
         swap(a[i], a[end]);
      }
      // cout << "x:" << x << " s:"<< start << " e:"<< end;
      // cout << " l:" << l << " r:"<< r << endl;
      // for (size_t j = l; j <= r; j++) cout << a[j] << ' ';
      // cout << endl;
   }
   // no swapping

   // cout << "after:  ";
   // for (size_t i = l; i <= r; ++i) cout << a[i] << ' ';
   // cout << endl;
   // cout << "########" << endl;

   return make_tuple(start, end);
}

void randomized_quick_sort3(vector<ll> &a, ll l, ll r) {
   if (l >= r) {
      return;
   }

   ll k = l + rand() % (r - l + 1);
   swap(a[l], a[k]);

   tuple<ll, ll> mid = partition3(a, l, r);
   randomized_quick_sort3(a, l, get<0>(mid) - 1);
   randomized_quick_sort3(a, get<1>(mid) + 1, r);
}

int main() {

   // ull start_s = 0;
   // ull stop_s = 0;
   // ull iteration_count = 0;

   // while (true) {
   //    ull n = (rand() % 100000);
   //    cout << "n: " << n << endl;
   //    if(n==0) continue;

   //    vector<ll> res1(n);
   //    vector<ll> res2(n);

   //    res1.clear();
   //    res2.clear();
   //    for(ll i=0;i<n;i++){
   //       ll e = rand() % 1000000000;
   //       res1.push_back(e);
   //       res2.push_back(e);
   //       // cout << e << " ";
   //    }
   //    // cout << endl;

   //    start_s = clock();
   //    randomized_quick_sort3(res1, 0, res1.size() - 1);
   //    stop_s = clock();
   //    // for (auto i: res1) cout << i << ' ';
   //    // cout << endl;
   //    cout << "randomized_quick_sort3 time: " << (stop_s - start_s) / double(CLOCKS_PER_SEC) * 1000 << " ms" << endl;

   //    start_s = clock();
   //    randomized_quick_sort2(res2, 0, res2.size() - 1);
   //    stop_s = clock();

   //    // for (auto i: res2) cout << i << ' ';
   //    // cout << endl;
   //    cout << "randomized_quick_sort2 time: " << (stop_s - start_s) / double(CLOCKS_PER_SEC) * 1000 << " ms" << endl;

   //    if (res1 == res2) {
   //       cout << "OK" << endl;
   //    }
   //    else {
   //       cout << "Wrong answer " << endl;
   //       getchar();
   //       // break;
   //    }

   //    cout << iteration_count++ << "====================\n";

   //    // getchar();
   // }

   ll n;
   std::cin >> n;
   vector<ll> a(n);
   for (size_t i = 0; i < a.size(); ++i) {
      std::cin >> a[i];
   }
   randomized_quick_sort3(a, 0, a.size() - 1);
   for (size_t i = 0; i < a.size(); ++i) {
      std::cout << a[i] << ' ';
   }
}
