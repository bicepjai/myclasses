#include <iostream>
#include <vector>
#include <algorithm>
#include <tuple>
typedef unsigned long long ull;
typedef long long ll;

using namespace std;

bool sortByValuePerWeight(tuple<double, double> i, tuple<double, double> j) {
   return (get<0>(i)/get<1>(i)) > (get<0>(j)/get<1>(j)) ;
}

double GetOptimalValue(int capacity, vector<tuple<double, double>> weights_values) {

   sort(weights_values.begin(), weights_values.end(), sortByValuePerWeight);

   // for(auto i : weights_values)
   //    cout << get<0>(i) << "," << get<1>(i) << "(" << (get<0>(i)/get<1>(i)) << ")" << " | ";
   // cout << endl;

   double total_value = 0.0;
   double C = (double)capacity;
   double weight_of_item_selected = 0;
   tuple<double, double> max_vw;
   vector<tuple<double, double>>::iterator vw_iter;
   vw_iter = weights_values.begin();

   while(vw_iter < weights_values.end()){
      if(C <= 0) break;
      max_vw = *vw_iter;
      // cout << get<0>(max_vw) << " " << get<1>(max_vw) << endl;
      weight_of_item_selected = min(C, get<1>(max_vw));
      // cout << "weight_of_item_selected: " << weight_of_item_selected << endl;
      total_value += (weight_of_item_selected * (get<0>(max_vw)/get<1>(max_vw)));
      // cout << "total_value: " << total_value << endl;
      C -= weight_of_item_selected;
      // cout << "C: " << C << endl;
      vw_iter++;

   }

  return total_value;
}

int main() {

   // ull start_s = 0;
   // ull stop_s = 0;
   // vector<tuple<double, double>> weights_values;
   // while (true) {
   //    ull n = (rand() % 20);
   //    if(n==0) continue;
   //    ull C = rand() % 100;
   //    weights_values.clear();
   //    cout << n << " " << C << " \n";
   //    for(int i=0;i<n;i++){
   //       ull v = (rand() % 2000) ;
   //       ull w = (rand() % 200);
   //       weights_values.push_back(make_tuple((double)v,(double)w));
   //    }
   //    start_s = clock();
   //    double res1 = GetOptimalValue(C, weights_values);
   //    stop_s = clock();
   //    cout << "GetOptimalValue:" << res1 << " time: " << (stop_s - start_s) / double(CLOCKS_PER_SEC) * 1000 << " ms" << endl;

   //    cout << "====================\n";
   //    // getchar();
   // }


   ull n;
   ull capacity;
   std::cin >> n >> capacity;
   // vector<int> values(n);
   // vector<int> weights(n);
   vector<tuple<double, double>> weights_values;
   for (int i = 0; i < n; i++) {
      // std::cin >> values[i] >> weights[i];
      ull v,w;
      std::cin >> v >> w;
      weights_values.push_back(make_tuple((double)v,(double)w));
   }

   // double optimal_value = GetOptimalValue(capacity, weights, values);
   double optimal_value = GetOptimalValue(capacity, weights_values);

   std::cout.precision(10);
   std::cout << optimal_value << std::endl;
   return 0;
}
