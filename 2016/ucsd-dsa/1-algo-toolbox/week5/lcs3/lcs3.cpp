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

typedef unsigned long long ull;
typedef long long ll;

using namespace std;


int lcs2(vector<int> seq_a, vector<int> seq_b) {

   int rows = seq_a.size()+1;
   int cols = seq_b.size()+1;
   int distance_map[rows][cols];

   // seq_b compared against empty vector
   // populating first extra col in the table
   for (int c = 0; c < cols; c++) distance_map[0][c] = 0;

   // seq_a compared against empty vector
   // populating first extra row in the table
   for (int r = 0; r < cols; r++) distance_map[r][0] = 0;

   // we can also do the above in the loop saying its 0 when
   // r == c ,note we have set distance_map[0][0] = 0

   // note that the loops start with 1 since the first row and col
   // are setup against the empty vector
   for (int r = 1; r < rows; r++)
   {
      for (int c = 1; c < cols; c++)
      {
         // if the current comparison is successful
         // we take the last best total update and add 1 meaning
         // we have a match here, 1 + diagnol element
         if (seq_a[r] == seq_b[c])
         {
            distance_map[r][c] = distance_map[r - 1][c - 1] + 1;
         }
         // this is the important part of the algorithm which might be confusing
         // understand the edit distance and this is just a very slight tweak
         // when the items are different, we just choose the maximum number of
         // top and left which means selecting the most-recent most-matched updates
         // draw the table and try this lecture for more practice
         // https://www.youtube.com/watch?v=NnD96abizww
         else {
            distance_map[r][c] = max(distance_map[r][c - 1],
                                     distance_map[r - 1][c]);
         }
      }
   }

   // cout << "distance_map" << endl;
   // for (int r = 0; r < rows; r++)
   // {
   //    for (int c = 0; c < cols; c++)
   //       cout << distance_map[r][c] << "\t";
   //    cout << endl;
   // }
   // cout << endl;

   return distance_map[rows - 1][cols - 1];
}

int main() {

   size_t an;
   std::cin >> an;
   vector<int> a(an);
   for (size_t i = 0; i < an; i++) {
      std::cin >> a[i];
   }
   size_t bn;
   std::cin >> bn;
   vector<int> b(bn);
   for (size_t i = 0; i < bn; i++) {
      std::cin >> b[i];
   }

   std::cout << lcs2(a, b) << std::endl;

   // size_t cn;
   // std::cin >> cn;
   // vector<int> c(cn);
   // for (size_t i = 0; i < cn; i++) {
   //    std::cin >> c[i];
   // }
   // std::cout << lcs3(a, b, c) << std::endl;

   return 0;
}
