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

class TreeHeight {
   int n;
   std::vector<int> parent;

public:
   void read() {
      std::cin >> n;
      parent.resize(n);
      for (int i = 0; i < n; i++)
         std::cin >> parent[i];
   }

   int compute_height() {

      int root = -1;
      // forming the nodes with child entries
      // empty entries are leaf nodes
      std::vector<vector<int>> nodes(n);
      std::vector<int> depth(n);

      for (int i = 0; i < parent.size(); i++)
      {
         if (parent[i] == -1)
            root = i;
         else
            nodes[parent[i]].push_back(i);

         // default height
         depth.push_back(0);
      }

      depth[root] = 1;
      // since there are might be many children
      // we have a queue to process the children
      // in order of levels to get depth
      queue<int> node_process;
      node_process.push(root);

      while (!node_process.empty())
      {
         int current = node_process.front();
         node_process.pop();

         for (int i = 0; i < nodes[current].size(); i++)
         {
            int child = nodes[current][i];
            // the depth of the children will be
            // one more than parent's depth
            depth[child] = depth[parent[child]] + 1;
            node_process.push(child);
         }

         // cout << "updating " << current << endl;
         // for (auto i : depth)
         //    cout << i << " ";
         // cout << endl;
      }

      return *max_element(depth.begin(), depth.end());
   }
};

int main() {
   std::ios_base::sync_with_stdio(0);
   TreeHeight tree;
   tree.read();
   std::cout << tree.compute_height() << std::endl;
}
