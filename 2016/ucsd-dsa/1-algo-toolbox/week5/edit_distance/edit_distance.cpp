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

int EditDistanceDP(const string &str1, const string &str2) {

   int rows = str1.length()+1;
   int cols = str2.length()+1;
   int distance_map[rows][cols];

   // str2 compared against empty string
   // populating first extra col in the table
   for (int c = 0; c < cols; c++) distance_map[0][c] = c;

   // str1 compared against empty string
   // populating first extra row in the table
   for (int r = 0; r < cols; r++) distance_map[r][0] = r;

   // note we have set distance_map[0][0] = 0

   // note that the loops start with 1 since the first row
   // are setup against the empty string
   for (int r = 1; r < rows; r++)
   {
      for (int c = 1; c < cols; c++)
      {
         // if the current comparison is successful
         // we take the last best total update
         // which is the diagnol element  distance_map[r - 1][c - 1]
         if (str1[r] == str2[c])
         {
            distance_map[r][c] = distance_map[r - 1][c - 1];
         }
         // this is the important part of the algorithm which might be confusing
         // draw the table and try this lecture for more information
         // https://www.youtube.com/watch?v=9-8Uj97J85c
         else {
            distance_map[r][c] = 1 + min(distance_map[r - 1][c - 1], // Replace
                                         min(distance_map[r][c - 1], // remove/insert
                                             distance_map[r - 1][c])); // remove/insert
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

   return distance_map[rows-1][cols-1];
}

int main() {
   string str1;
   string str2;
   std::cin >> str1 >> str2;
   std::cout << EditDistanceDP(str1, str2) << std::endl;
   return 0;
}
