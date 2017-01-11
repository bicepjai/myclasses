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

class TreeOrders {
   int n;
   vector <int> key;
   vector <int> left;
   vector <int> right;

public:
   void read() {
      cin >> n;
      key.resize(n);
      left.resize(n);
      right.resize(n);
      for (int i = 0; i < n; i++) {
         cin >> key[i] >> left[i] >> right[i];
      }
   }

   void inorder_recur(int current, vector<int> &result)
   {
      if(left[current] == -1 &&
         right[current] == -1)
      {
         result.push_back(key[current]);
         return;
      }

      if(left[current] != -1)
      {
         inorder_recur(left[current], result);
      }

      result.push_back(key[current]);

      if(right[current] != -1)
      {
         inorder_recur(right[current], result);
      }
   }

   vector <int> in_order() {
      vector<int> result;
      // Finish the implementation
      // You may need to add a new recursive method to do that
      inorder_recur( 0, result);
      return result;
   }

   void preorder_recur(int current, vector<int> &result)
   {
      if(left[current] == -1 &&
         right[current] == -1)
      {
         result.push_back(key[current]);
         return;
      }

      result.push_back(key[current]);

      if(left[current] != -1)
      {
         preorder_recur(left[current], result);
      }

      if(right[current] != -1)
      {
         preorder_recur(right[current], result);
      }
   }

   vector <int> pre_order() {
      vector<int> result;
      // Finish the implementation
      // You may need to add a new recursive method to do that
      preorder_recur( 0, result);
      return result;
   }

   void postorder_recur(int current, vector<int> &result)
   {
      if(left[current] == -1 &&
         right[current] == -1)
      {
         result.push_back(key[current]);
         return;
      }

      if(left[current] != -1)
      {
         postorder_recur(left[current], result);
      }

      if(right[current] != -1)
      {
         postorder_recur(right[current], result);
      }

      result.push_back(key[current]);
   }

   vector <int> post_order() {
      vector<int> result;
      // Finish the implementation
      // You may need to add a new recursive method to do that
      postorder_recur( 0, result);
      return result;
   }
};

void print(vector <int> a) {
   for (size_t i = 0; i < a.size(); i++) {
      if (i > 0) {
         cout << ' ';
      }
      cout << a[i];
   }
   cout << '\n';
}

int main() {
   ios_base::sync_with_stdio(0);
   TreeOrders t;
   t.read();
   print(t.in_order());
   print(t.pre_order());
   print(t.post_order());
   return 0;
}
