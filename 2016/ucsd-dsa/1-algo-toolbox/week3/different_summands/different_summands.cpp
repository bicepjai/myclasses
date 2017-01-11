#include <iostream>
#include <algorithm>
#include <climits>
#include <vector>
#include <tuple>

typedef unsigned long long ull;
typedef long long ll;

using namespace std;

vector<ull> OptimalSummands(ull n) {
   vector<ull> summands;
   ull remaining = n;
   ull current_summand = 1;
   ull running_sum = 0;

   // cout << "--------------------------" << endl;
   while (running_sum + 2*current_summand < n)
   {
      running_sum += current_summand;
      remaining -= current_summand;
      // cout << current_summand << " " << running_sum << " " << remaining << endl;
      summands.push_back(current_summand);
      current_summand++;
   }
   summands.push_back(remaining);
   // cout << "--------------------------" << endl;
   return summands;
}

int main() {

   // ull start_s = 0;
   // ull stop_s = 0;

   // while (true) {
   //    ull n = (rand() % 100)+1;
   //    cout << n << " \n";

   //    start_s = clock();
   //    vector<ull> summands = OptimalSummands(n);
   //    stop_s = clock();

   //    ull sum_of_elems = 0;
   //    for (ull n : summands)
   //       sum_of_elems += n;

   //    cout << "OptimalSummands: " ;
   //    for (size_t i = 0; i < summands.size(); ++i) {
   //       std::cout << summands[i] << " ";
   //    }
   //    cout << "\n time: " << (stop_s - start_s) / double(CLOCKS_PER_SEC) * 1000 << " ms" << endl;

   //    if (sum_of_elems != n) {
   //       cout << "Wrong answer: " << sum_of_elems << ' ' << n << "\n";
   //       getchar();
   //    }
   //    else {
   //       cout << "OK\n";
   //    }

   //    cout << "====================\n";
   //    // getchar();
   // }

  ull n;
  std::cin >> n;
  vector<ull> summands = OptimalSummands(n);
  std::cout << summands.size() << '\n';
  for (size_t i = 0; i < summands.size(); ++i) {
    std::cout << summands[i] << ' ';
  }
}
