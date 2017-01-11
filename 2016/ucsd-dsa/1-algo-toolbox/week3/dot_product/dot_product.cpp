#include <iostream>
#include <vector>
#include <algorithm>
#include <tuple>
typedef long long ll;
typedef unsigned long long ull;

using namespace std;

bool ascend(ll i, ll j) {
   return (i > j) ;
}

bool descend(ll i, ll j) {
   return (i < j) ;
}

ll MinDotProduct(vector<ll> a, vector<ll> b) {

  sort(a.begin(), a.end(), descend);
  sort(b.begin(), b.end(), ascend);

  ll result = 0;
  for (size_t i = 0; i < a.size(); i++) {
    result += a[i] * b[i];
  }

  return result;
}

int main() {

   // ull start_s = 0;
   // ull stop_s = 0;
   // while (true) {
   //    ull n = (rand() % 1000);
   //    vector<int> a(n), b(n);
   //    for (size_t i = 0; i < n; i++) {
   //       ull range = 100000;
   //       a[i] = 2*(rand() % range) - range;
   //       b[i] = 2*(rand() % range) - range;
   //   }
   //    cout << n << endl;
   //    start_s = clock();
   //    double res1 = MinDotProduct(a, b);
   //    stop_s = clock();
   //    cout << "MinDotProduct:" << res1 << " time: " << (stop_s - start_s) / double(CLOCKS_PER_SEC) * 1000 << " ms" << endl;

   //    cout << "====================\n";
   //    // getchar();
   // }


  size_t n;
  std::cin >> n;
  vector<ll> a(n), b(n);
  for (size_t i = 0; i < n; i++) {
    std::cin >> a[i];
  }
  for (size_t i = 0; i < n; i++) {
    std::cin >> b[i];
  }
  std::cout << MinDotProduct(a, b) << std::endl;
}
