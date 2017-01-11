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
#include <stack>
#include <queue>

typedef unsigned long long ull;
typedef long long ll;

using namespace std;

class HeapBuilder {
private:
   vector<int> data_;
   vector< pair<int, int> > swaps_;

   void WriteResponse() const {
      cout << swaps_.size() << "\n";
      for (int i = 0; i < swaps_.size(); ++i) {
         cout << swaps_[i].first << " " << swaps_[i].second << "\n";
      }

      // cout << endl;
      // for (int i = 0; i < data_.size(); ++i)
      //    cout << data_[i] << " " ;
      // cout << endl;

   }

   void ReadData() {
      int n;
      cin >> n;
      data_.resize(n);
      for (int i = 0; i < n; ++i)
         cin >> data_[i];
   }

   int leftChild(int index)
   {
      if (index == 0)
         return 1;
      else
         return 2 * index + 1;
   }

   int rightChild(int index)
   {

      if (index == 0)
         return 2;
      else
         return 2 * index + 2;
   }

   void siftDown(int index)
   {
      int min_index = index;
      int left = leftChild(index);
      if (left < data_.size() && data_[min_index] > data_[left])
      {
         min_index = left;
      }
      int right = rightChild(index);
      if (right < data_.size() && data_[min_index] > data_[right])
      {
         min_index = right;
      }
      if (index != min_index)
      {
         // cout << index << " " <<  min_index << endl;
         swap(data_[index], data_[min_index]);
         swaps_.push_back(make_pair(index, min_index));
         siftDown(min_index);
      }
   }

   void GenerateSwaps() {
      swaps_.clear();

      for (int i = data_.size() / 2; i >= 0; i--)
      {
         // cout << i << " ===> " << data_[i] << endl;
         siftDown(i);
      }
   }

public:
   void Solve() {
      ReadData();
      GenerateSwaps();
      WriteResponse();
   }
};

int main() {
   std::ios_base::sync_with_stdio(false);
   HeapBuilder heap_builder;
   heap_builder.Solve();
   return 0;
}
