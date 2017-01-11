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

ll get_majority_element(vector<ll> &a, ll left, ll right) {
   if (left >= right) {
      // cout << "base:" << a[left] << endl;
      return a[left];
   }


   ll half = (right - left) / 2;
   ll mid = left + half;

   // cout << "=>left:" << left << " mid:" << mid << " right:" << right << endl;
   ll left_maj = get_majority_element(a, left, mid);

   // cout << "->left:" << left << " mid:" << mid << " right:" << right << endl;
   ll right_maj = get_majority_element(a, mid + 1, right);

   // cout << "l: " << left << " r:" << right << endl;

   // took long time to figure this shit out
   // handling 0 case
   if((right - left)%2 != 0) half = (right - left + 1) / 2;

   // getting count
   ll left_maj_count = 0;
   ll right_maj_count = 0;
   for (ll i = left; i <= right; i++) {
      if (a[i] == left_maj) left_maj_count++;
      else if (a[i] == right_maj) right_maj_count++;
   }

   if (right_maj == left_maj) {
      // cout << "retx==y: (" << left_maj << "[" << left_maj_count << "]," << right_maj << "[" << right_maj_count;
      // cout << "], h[" << half << "]) " << right_maj << endl;
      return right_maj;
   }
   else if (left_maj != -1 && left_maj_count > half) {
      // cout << "ret_left_maj: (" << left_maj << "[" << left_maj_count << "]," << right_maj << "[" << right_maj_count;
      // cout << "], h[" << half << "]) " << left_maj << endl;
      return left_maj;
   }
   else if (right_maj != -1 && right_maj_count > half) {
      // cout << "ret_right_maj: (" << left_maj << "[" << left_maj_count << "]," << right_maj << "[" << right_maj_count;
      // cout << "], h[" << half << "]) " << right_maj << endl;
      return right_maj;
   }
   else {
      // cout << "ret_-1: (" << left_maj << "[" << left_maj_count << "]," << right_maj << "[" << right_maj_count;
      // cout << "], h[" << half << "]) -1" << endl;
      return -1;
   }

}

int main() {

   // ll start_s = 0;
   // ll stop_s = 0;
   // ll run_iteration = 0;
   // while (true) {

   //    cout << "=========" << endl;
   //    ll n = 1 + rand() % 10; // 10E5
   //    cout << "n: " << n << endl;
   //    vector<ll> seq;
   //    if(n==1 || n==2) continue;
   //    int res2;
   //    if (rand() % 2 == 0)
   //    {
   //       cout << "majority exists:" << endl;
   //       res2 = 1;

   //       for (size_t i = 0; i < n/2; i++) {
   //          seq.push_back(rand() % 100); //10E9
   //       }

   //       int remaining = n-seq.size();
   //       ll maj_elem = rand() % 100; //10E9
   //       for (size_t i = 0; i < remaining; i++) {
   //          seq.push_back(maj_elem); //10E9
   //       }
   //       seq[rand() % (n/2)] = maj_elem;

   //    } else {
   //       // this condition has bug
   //       cout << "majority doesnt exists:" << endl;
   //       res2 = 0;
   //       for (size_t i = 0; i < n; i++) {
   //          seq.push_back(rand() % 100); //10E9
   //       }
   //    }
   //    random_shuffle ( seq.begin(), seq.end() );

   //    for (size_t i = 0; i < seq.size(); i++) {
   //       cout << i << "-" << seq[i] << " ";
   //    } cout << endl;

   //    cout << "-------" << endl;
   //    start_s = clock();
   //    int res1 = (get_majority_element(seq, 0, seq.size() - 1) != -1);
   //    stop_s = clock();
   //    cout << run_iteration++ << ") get_majority_element:" << res1 << " time: " << (stop_s - start_s) / double(CLOCKS_PER_SEC) * 1000 << " ms" << endl;

   //    if (res1 == res2) {
   //       cout << "OK\n";
   //    }
   //    else {
   //       cout << "Wrong answer " << "\n";
   //       getchar();
   //       // break;
   //    }

   //    cout << "\n";
   //    // getchar();
   // }

   ll n;
   std::cin >> n;
   vector<ll> a(n);
   for (size_t i = 0; i < a.size(); ++i) {
      std::cin >> a[i];
   }
   std::cout << (get_majority_element(a, 0, a.size() - 1) != -1) << '\n';
}
