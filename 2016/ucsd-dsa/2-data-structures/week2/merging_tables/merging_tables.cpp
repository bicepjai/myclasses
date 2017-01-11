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

struct DisjointSetsElement {
   int size, parent, rank;

   DisjointSetsElement(int size = 0, int parent = -1, int rank = 0):
      size(size), parent(parent), rank(rank) {}
};

struct DisjointSets {
   int size;
   int max_table_size;
   vector <DisjointSetsElement> sets;

   DisjointSets(int size): size(size), max_table_size(0), sets(size) {
      for (int i = 0; i < size; i++)
         sets[i].parent = i;
   }

   int getParent(int table) {
      // find parent and compress path
      int current = table;
      int parent = current;
      vector<int> path;
      path.push_back(current);
      while (true)
      {
         parent = current;
         current = sets[current].parent;
         if (current == parent) break;
         path.push_back(current);
      }

      // cout << "parent: " << parent;
      // cout << " path of " << table  << " => ";
      for (int i = 0; i < path.size(); i++)
      {
         // cout << path[i] << " ";
         sets[path[i]].parent = parent;
      }
      // cout << endl;
      return parent;
   }

   void merge(int destination, int source) {

      // cout << "-------------------------------" << endl;
      int realDestination = getParent(destination);
      int realSource = getParent(source);
      // cout << "tables: " << destination << " <- " << source;
      // cout << " parents: " << realDestination << " <- " << realSource << endl;
      // cout << "parents b4 merge: ";
      // for (int i = 0; i < sets.size(); i++)
      //    cout << sets[i].parent << " ";
      // cout << endl;
      // cout << "rank b4 merge: ";
      // for (int i = 0; i < sets.size(); i++)
      //    cout << sets[i].rank << " ";
      // cout << endl;
      // cout << "size b4 merge: ";
      // for (int i = 0; i < sets.size(); i++)
      //    cout << sets[i].size << " ";
      // cout << endl;
      // cout << "---" << endl;
      if (realDestination != realSource) {
         // merge two components
         // use union by rank heuristic
         // update max_table_size
         if (sets[realDestination].rank == sets[realSource].rank)
         {
            sets[realSource].parent = realDestination;
            sets[realDestination].size += sets[realSource].size;
            max_table_size = max(max_table_size, sets[realDestination].size);
            sets[realSource].size = 0;
            sets[realDestination].rank++;
         }

         else if (sets[realDestination].rank > sets[realSource].rank)
         {
            sets[realSource].parent = realDestination;
            sets[realDestination].size += sets[realSource].size;
            max_table_size = max(max_table_size, sets[realDestination].size);
            sets[realSource].size = 0;
         }
         else
         {
            sets[realDestination].parent = realSource;
            sets[realSource].size += sets[realDestination].size;
            sets[realDestination].size = 0;
            max_table_size = max(max_table_size, sets[realSource].size);
         }
      }

      // cout << "parents aftr merge: ";
      // for (int i = 0; i < sets.size(); i++)
      //    cout << sets[i].parent << " ";
      // cout << endl;
      // cout << "rank aftr merge: ";
      // for (int i = 0; i < sets.size(); i++)
      //    cout << sets[i].rank << " ";
      // cout << endl;
      // cout << "size aftr merge: ";
      // for (int i = 0; i < sets.size(); i++)
      //    cout << sets[i].size << " ";
      // cout << endl;
   }
};

int main() {
   int n, m;
   cin >> n >> m;

   DisjointSets tables(n);
   for (auto &table : tables.sets) {
      cin >> table.size;
      tables.max_table_size = max(tables.max_table_size, table.size);
   }

   for (int i = 0; i < m; i++) {
      int destination, source;
      cin >> destination >> source;
      --destination;
      --source;

      tables.merge(destination, source);
      cout << tables.max_table_size << endl;
   }

   return 0;
}
