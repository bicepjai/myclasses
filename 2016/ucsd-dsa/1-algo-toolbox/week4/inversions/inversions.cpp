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

ll MergeStep(vector<ll> &a, size_t left, size_t mid, size_t right)
{
   ll inversions = 0;
   size_t l = left;
   size_t r = mid + 1;
   size_t i = 0, j;
   vector<ll> v(right - left + 1);

   // cout << "left: " << left << " mid: " << mid << " right: " << right << endl;
   // for (j = 0; j < a.size(); j++) {
   //    cout << a[j] << " ";
   // } cout << endl;

   while (l <= mid && r <= right) {
      if(a[l] <= a[r])
      {
         v[i] = a[l];
         l++;
      } else {
         inversions += mid - l +1;
         // cout << l << " inversions " << inversions << endl;
         v[i] = a[r];
         r++;
      }
      i++;
   }

   while (l <= mid) {
      v[i] = a[l];
      i++; l++;
   }

   while (r <= right) {
      v[i] = a[r];
      i++; r++;
   }

   for (i = left, j = 0; i <= right; i++, j++) a[i] = v[j];

   // for (size_t i = 0; i < a.size(); i++) {
   //    cout << a[i] << " ";
   // } cout << endl << "--------" << endl;

   return inversions;
}

ll MergeSort(vector<ll> &a, size_t left, size_t right)
{
   ll inversions = 0;
   if (left >= right) return 0;
   size_t mid = left + (right - left) / 2;
   inversions = MergeSort(a, left, mid);
   inversions += MergeSort(a, mid + 1, right);
   inversions += MergeStep(a, left, mid, right);
   return inversions;
}


int main() {

   // didnt do stress testing here

   ll n;
   cin >> n;
   vector<ll> a(n);
   cout << endl;
   for (size_t i = 0; i < a.size(); i++) {
      cin >> a[i];
   }

   // cout << endl;
   // for (size_t i = 0; i < a.size(); i++) {
   //    cout << a[i] << " ";
   // }

   std::cout << MergeSort(a, 0, a.size() - 1) << '\n';
}
