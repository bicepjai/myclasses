#include <iostream>
#include <algorithm>
#include <climits>
#include <vector>
#include <tuple>

typedef unsigned long long ull;
typedef long long ll;

using namespace std;

struct Segment {
  ull start, end;
};

bool sortBySegmentEnd(Segment i, Segment j) {
   return (i.end < j.end) ;
}

vector<ull> OptimalPoints(vector<Segment> &segments) {

   sort(segments.begin(), segments.end(), sortBySegmentEnd);
   vector<ull> points;
   ull current_end = segments[0].end;
   // cout << "--------------------------" << endl;
   size_t i;
   for (i = 1; i < segments.size(); i++)
   {
      // cout << endl;
      // cout << segments[i].start << " " <<  segments[i].end;
      if(current_end >= segments[i].start && current_end <= segments[i].end)
      {
         // cout << "*   " << current_end;
         continue;
      }
      points.push_back(current_end);
      current_end = segments[i].end;
   }
   points.push_back(current_end);

   // cout << endl << "--------------------------" << endl;

  return points;
}

int main() {

   // ull start_s = 0;
   // ull stop_s = 0;

   // while (true) {
   //    ull n = (rand() % 100)+1;
   //    vector<Segment> segments(n);
   //    cout << n << " \n";
   //    ull range = 1000000000;
   //    for(ull i=0;i<n;i++){
   //       ull start = (rand() % range);
   //       ull end   = start + (rand() % int(start-range));
   //       segments[i].start = start;
   //       segments[i].end = end;
   //    }

   //    start_s = clock();
   //    vector<ull> points = OptimalPoints(segments);
   //    stop_s = clock();

   //    for (size_t i = 0; i < segments.size(); ++i) {
   //       std::cout << segments[i].start << " " <<  segments[i].end << endl;
   //    }
   //    cout << "OptimalPoints: " ;
   //    for (size_t i = 0; i < points.size(); ++i) {
   //       std::cout << points[i] << " ";
   //    }
   //    cout << "\n time: " << (stop_s - start_s) / double(CLOCKS_PER_SEC) * 1000 << " ms" << endl;

   //    cout << "====================\n";
   //    // getchar();
   // }

  ull n;
  std::cin >> n;
  vector<Segment> segments(n);
  for (size_t i = 0; i < segments.size(); ++i) {
    std::cin >> segments[i].start >> segments[i].end;
  }
  vector<ull> points = OptimalPoints(segments);
  std::cout << points.size() << "\n";
  for (size_t i = 0; i < points.size(); ++i) {
    std::cout << points[i] << " ";
  }
  std::cout << endl;
}
