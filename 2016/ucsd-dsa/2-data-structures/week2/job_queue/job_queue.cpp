#include <iostream>
#include <cassert>
#include <vector>
#include <algorithm>
#include <tuple>
#include <map>
#include <set>
#include <iterator>
#include <climits>
#include <stack>
#include <queue>
#include <functional>

typedef unsigned long long ull;
typedef long long ll;

using namespace std;

bool PQCompare(pair<ll, ll> a, pair<ll, ll> b)
{
   if (a.second == b.second)
      return a.first > b.first;
   else
      return a.second > b.second;
}
priority_queue<pair<ll, ll>, std::vector<pair<ll, ll>>, decltype(&PQCompare) > pq(PQCompare);

class JobQueue {
private:
   ll num_workers_;
   vector<ll> jobs_;

   vector<ll> assigned_workers_;
   vector<long long> start_times_;



   void WriteResponse() const {
      for (ll i = 0; i < jobs_.size(); ++i) {
         cout << assigned_workers_[i] << " " << start_times_[i] << "\n";
      }
   }

   void ReadData() {
      ll m;
      cin >> num_workers_ >> m;
      jobs_.resize(m);
      for (ll i = 0; i < m; ++i)
         cin >> jobs_[i];
   }

   void AssignJobs() {
      // TODO: replace this code with a faster algorithm.
      assigned_workers_.resize(jobs_.size());
      start_times_.resize(jobs_.size());

      // vector<long long> next_free_time(num_workers_, 0);
      // for (ll i = 0; i < jobs_.size(); ++i) {
      //    ll duration = jobs_[i];
      //    ll next_worker = 0;
      //    for (ll j = 0; j < num_workers_; ++j) {
      //       if (next_free_time[j] < next_free_time[next_worker])
      //          next_worker = j;
      //    }
      //    assigned_workers_[i] = next_worker;
      //    start_times_[i] = next_free_time[next_worker];
      //    next_free_time[next_worker] += duration;
      // }

      ll jobs_processed_initally = 0;

      if (jobs_.size() > num_workers_)
      {
         jobs_processed_initally = num_workers_;
      }
      else
      {
         jobs_processed_initally = jobs_.size();
      }

      for (ll i = 0; i < jobs_processed_initally; ++i)
      {
         assigned_workers_[i] = i;
         start_times_[i] = 0;
         pq.push(make_pair(i, jobs_[i]));
      }

      // cout << "jobs_processed_initally: " << jobs_processed_initally << endl;
      // vector<pair<ll, ll>> pqv(pq.size());
      // copy(&(pq.top()), &(pq.top()) + pq.size(), &pqv[0]);
      // for (pair<ll, ll> ele : pqv)
      //    cout << "(" << ele.first << "," << ele.second << ") ";
      // cout << endl;


      for (ll i = jobs_processed_initally; i < jobs_.size(); ++i) {
         ll duration = jobs_[i];

         // getting worker that finished first
         // this priority queue returns worker with lower index
         // if 2 workers ends at the same time.
         pair<ll, ll> worker_endtime =  pq.top();
         pq.pop();
         ll worker = worker_endtime.first;
         ll end_time = worker_endtime.second;

         assigned_workers_[i] = worker;
         start_times_[i] = end_time;
         pq.push(make_pair(worker, end_time + duration));
      }

   }

public:
   void Solve() {
      ReadData();
      AssignJobs();
      WriteResponse();
   }
};

int main() {
   std::ios_base::sync_with_stdio(false);
   JobQueue job_queue;
   job_queue.Solve();
   return 0;
}
