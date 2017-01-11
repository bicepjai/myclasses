#include <iostream>
#include <cassert>
// #include <ctime>
#include <vector>
#include <algorithm>
#include <tuple>
#include <map>
#include <set>
#include <iterator>
#include <limits>

typedef unsigned long long ull;
typedef long long ll;

using namespace std;

struct Segment {
   ll start, end;
};

bool sortBySegmentStart(Segment i, Segment j) {
   return (i.start < j.start) ;
}

vector<ll> FastCountSegments(vector<Segment> segments, vector<ll> points) {
   ll SEGMENT_START = 0;
   ll SEGMENT_END = 2;
   ll POINT = 1;

   vector<ll> counts;
   map<ll,ll> count_map;
   vector<pair<ll,ll>> all_points;

   for (size_t i = 0; i < segments.size(); i++)
   {
      all_points.push_back(make_pair(segments[i].start,SEGMENT_START));
      all_points.push_back(make_pair(segments[i].end,SEGMENT_END));
   }
   for (size_t i = 0; i < points.size(); i++)
   {
      all_points.push_back(make_pair(points[i],POINT));
   }

   // when it has pairs c++ sorts 1st element followed by 2nd
   sort(all_points.begin(), all_points.end());
   ll count = 0;
   for (size_t i = 0; i < all_points.size(); i++)
   {
      if(all_points[i].second == SEGMENT_START) {
         count++;
         // cout << "SEGMENT_START " << all_points[i].first << " cnt: " << count << endl;
      }

      if(all_points[i].second == POINT) {
         // cout << "POINT " << all_points[i].first << " cnt: " << count << endl;
         count_map.insert(make_pair(all_points[i].first, count));
      }

      if(all_points[i].second == SEGMENT_END) {
         count--;
         // cout << "SEGMENT_END " << all_points[i].first << " cnt: " << count << endl;
      }

   }

   for (size_t i = 0; i < points.size(); i++)
   {
      counts.push_back(count_map[points[i]]);
   }

   return counts;
}

vector<ll> NotFastEnufCountSegments(vector<Segment> segments, vector<ll> points) {
   vector<ll> cnt(points.size());
   sort(segments.begin(), segments.end(), sortBySegmentStart);
   for (size_t i = 0; i < points.size(); i++) {
      size_t j = 0;
      while(j < segments.size()) {
         if(points[i] >= segments[j].start && points[i] <= segments[j].end)
            cnt[i]++;
         if(segments[j].start > points[i]) break;
         j++;
      }
   }
   return cnt;
}

vector<ll> NaiveCountSegments(vector<Segment> segments, vector<ll> points) {
   vector<ll> cnt(points.size());
   for (size_t i = 0; i < points.size(); i++) {
      for (size_t j = 0; j < segments.size(); j++) {
         cnt[i] += segments[j].start <= points[i] && points[i] <= segments[j].end;
      }
   }
   return cnt;
}

int main() {

   // ull start_s = 0;
   // ull stop_s = 0;

   // while (true) {
   //    ll s = (rand() % 10)+1;
   //    ll p = (rand() % 10)+1;
   //    vector<Segment> segments(s);
   //    cout << "s: " << s << " p: "<< p << " \n";
   //    ll range = 100;

   //    for(size_t i=0;i<s;i++) {
   //       ll start = ((rand()%2 == 0) ? 1 : -1)*(rand() % 20);
   //       ll end   = start + (rand() % ll(start-range));
   //       segments[i].start = start;
   //       segments[i].end = end;
   //    }

   //    cout << "segments" << endl;
   //    for (size_t i = 0; i < segments.size(); ++i)
   //       cout << segments[i].start << " " <<  segments[i].end << endl;

   //    vector<ll> points(p);
   //    for(size_t i=0;i<p;i++) {
   //       points[i] = ((rand()%2 == 0) ? 1 : -1)*(rand() % range);
   //    }

   //    cout << "points" << endl;
   //    for (size_t i = 0; i < points.size(); ++i)
   //       std::cout << points[i] << " ";
   //    cout << endl;

   //    start_s = clock();
   //    vector<ll> res2 = NotFastEnufCountSegments(segments, points);
   //    stop_s = clock();

   //    cout << "\n NotFastEnufCountSegments time: " << (stop_s - start_s) / double(CLOCKS_PER_SEC) * 1000 << " ms" << endl;

   //    for (size_t i = 0; i < res2.size(); i++) cout << res2[i] << ' ';
   //    cout << endl;

   //    start_s = clock();
   //    vector<ll> res1 = FastCountSegments(segments, points);
   //    stop_s = clock();

   //    cout << "\n FastCountSegments time: " << (stop_s - start_s) / double(CLOCKS_PER_SEC) * 1000 << " ms" << endl;
   //    for (size_t i = 0; i < res1.size(); i++) cout << res1[i] << ' ';
   //    cout << endl;

   //    if (res1 == res2) {
   //       cout << "OK" << endl;
   //    }
   //    else {
   //       cout << "Wrong answer " << endl;
   //       getchar();
   //       // break;
   //    }

   //    cout << "====================\n";
   //    // getchar();
   // }


   ll s, p;
   std::cin >> s;
   std::cin >> p;

   vector<Segment> segments(s);
   for (size_t i = 0; i < s; ++i) {
      std::cin >> segments[i].start >> segments[i].end;
   }

   vector<ll> points(p);
   for (size_t i = 0; i < p; ++i) {
      std::cin >> points[i];
   }

   vector<ll> cnt = FastCountSegments(segments, points);
   for (size_t i = 0; i < cnt.size(); i++) {
      std::cout << cnt[i] << ' ';
   }
}
