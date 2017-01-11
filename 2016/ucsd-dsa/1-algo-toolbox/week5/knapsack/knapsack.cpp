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

int optimal_weight(int W, const vector<int> &w) {
   //write your code here
   int current_weight = 0;
   for (size_t i = 0; i < w.size(); ++i) {
      if (current_weight + w[i] <= W) {
         current_weight += w[i];
      }
   }
   return current_weight;
}

// ll calls_made = 0;

ll MaxWeight(vector<ll> weights, ll item, ll remaining_weight)
{
   // calls_made++;
   if (item == 0)
   {
      // cout << "item: 0 "<< endl;
      if (weights[item] <= remaining_weight)
         return weights[item];
      else
         return 0;
   }

   // cout << "without_item: " << weights[item] << endl;
   ll without_item = MaxWeight(weights, item - 1, remaining_weight);
   if (weights[item] > remaining_weight) {
      return without_item;
   }
   else {
      // cout << "with_item: " << weights[item] << endl;
      ll with_item = weights[item] + MaxWeight(weights, item - 1, remaining_weight - weights[item]);
      return max(without_item, with_item);
   }
}

ll DpMaxWeight(vector<ll> weights, ll item, ll remaining_weight, map<pair<ll, ll>, ll> &item_weight_map)
{
   // cout << "pair: " << item << "," << remaining_weight << " ";
   auto iter = item_weight_map.find(make_pair(item, remaining_weight));
   if (iter != item_weight_map.end())
   {
      // cout << "from map"<< endl;
      return item_weight_map[make_pair(item, remaining_weight)];
   }
   else {
      // cout << "call made"<< endl;
      // calls_made++;
      if (item == 0)
      {
         // cout << "item: 0 "<< endl;
         if (weights[item] <= remaining_weight) {
            item_weight_map.insert( make_pair(
                                       make_pair(item, remaining_weight),
                                       weights[item]));
            return weights[item];
         }
         else
            return 0;
      }
      // cout << "without_item: " << weights[item] << endl;
      ll without_item = DpMaxWeight(weights, item - 1, remaining_weight, item_weight_map);
      if (weights[item] > remaining_weight) {
         item_weight_map.insert( make_pair(
                                    make_pair(item, remaining_weight),
                                    without_item));
         return without_item;
      }
      else {
         // cout << "with_item: " << weights[item] << endl;
         ll with_item = weights[item] + DpMaxWeight(weights, item - 1, remaining_weight - weights[item], item_weight_map);
         item_weight_map.insert( make_pair(
                                    make_pair(item, remaining_weight),
                                    max(without_item, with_item)));
         return max(without_item, with_item);
      }
   }
}

// Returns the maximum value that can be put in a knapsack of capacity W
ll knapSackLecture(ll W, vector<ll> wt)
{
   ll n = wt.size();
   ll K[n + 1][W + 1];

   // Build table K[][] in bottom up manner
   for (ll i = 0; i <= n; i++)
   {
      for (ll w = 0; w <= W; w++)
      {
         if (i == 0 || w == 0)
            K[i][w] = 0;
         else if (wt[i - 1] <= w)
            K[i][w] = max(wt[i - 1] + K[i - 1][w - wt[i - 1]],  K[i - 1][w]);
         else
            K[i][w] = K[i - 1][w];
      }
   }
   for (ll i = 0; i <= n; i++) {
      for (ll w = 0; w <= W; w++)
         cout << "\t" << K[i][w] << " ";
      cout << endl;
   }

   return K[n][W];
}

int main() {
   ll n, W;
   cin >> W >> n;
   vector<ll> w(n);
   for (size_t i = 0; i < n; i++) {
      cin >> w[i];
   }
   // cout << optimal_weight(W, w) << '\n';
   // cout << MaxWeight(w, w.size()-1, W) << '\n';
   // cout << "MaxWeight calls_made: " << calls_made << endl;
   // calls_made = 0;

   // map<pair<ll, ll>, ll> item_weight_map;
   // cout << DpMaxWeight(w, w.size() - 1, W, item_weight_map) << '\n';
   // cout << "DpMaxWeight calls_made: " << calls_made << endl;

   // cout << knapSackLecture(W, w) << '\n';

   // cout << "DpMaxWeight calls_made: " << calls_made << endl;

}
