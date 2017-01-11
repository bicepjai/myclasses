#include <stdio.h>
#include <cstring>
#include <iostream>
#include <string>
#include <cassert>
// #include <ctime>
#include <vector>
#include <algorithm>
#include <tuple>
#include <set>
#include <iterator>
#include <limits>

typedef unsigned long long ull;
typedef long long ll;

using namespace std;

long long eval(long long a, long long b, char op) {
   if (op == '*') {
      return a * b;
   } else if (op == '+') {
      return a + b;
   } else if (op == '-') {
      return a - b;
   } else {
      assert(0);
   }
}

pair<ll, ll> get_min_max_value(const string exp,
                               ll** max_table, ll** min_table,
                               int start_, int end_)
{
   // default values
   ll minv = numeric_limits<int>::max();
   ll maxv = numeric_limits<int>::min();

   // the loop to iterate thru the operands
   // we are using the table index for the operand
   for (int operand_index = start_; operand_index < end_; operand_index++)
   {
      // op_index for the operator in the expression
      int op_index = (operand_index * 2) + 1;
      // 2 parts considered which has already been calculated
      // and are available in the table
      cout << "(" << start_ << "," << operand_index << ")" << endl;
      cout << "(" << operand_index + 1 << "," << end_ << ")" << endl;
      cout << "op: " << exp[op_index] << endl;

      ll a = eval(max_table[start_][operand_index],
                  max_table[operand_index + 1][end_],
                  exp[op_index]);
      ll b = eval(min_table[start_][operand_index],
                  min_table[operand_index + 1][end_],
                  exp[op_index]);
      ll c = eval(min_table[start_][operand_index],
                  max_table[operand_index + 1][end_],
                  exp[op_index]);
      ll d = eval(max_table[start_][operand_index],
                  min_table[operand_index + 1][end_],
                  exp[op_index]);

      cout << "abcd: " << a << " " << b << " " << c << " " << d << endl;
      minv = min(minv, min(min(min(a, b), c), d));
      maxv = max(maxv, max(max(max(a, b), c), d));
   }

   cout << "-------------------------" << endl;
   return make_pair(minv, maxv);
}

long long get_maximum_value(const string exp) {
   // all the arrays deals with size n
   // which is number of digits in the expression
   ll n = (exp.length() + 1) / 2;

   // creating 2d array for min and max table
   ll **max_table = new ll*[n];
   for (size_t i = 0; i < n; i++) {
      max_table[i] = new ll[n];
      memset(max_table[i], 0, sizeof(ll) * n);
   }

   ll **min_table = new ll*[n];
   for (size_t i = 0; i < n; i++) {
      min_table[i] = new ll[n];
      memset(min_table[i], 0, sizeof(ll) * n);
   }

   // setting the diagnol elements of the table to
   // numbers form expression meaning they are both maximum and minimum
   // since there are no evaluations and just one element
   for (size_t exp_i = 0; exp_i < exp.length(); exp_i += 2)
   {
      // cout << exp_i / 2 << " " << exp[exp_i] - '0' << endl;
      max_table[exp_i / 2][exp_i / 2] = ll(exp[exp_i] - '0');
      min_table[exp_i / 2][exp_i / 2] = ll(exp[exp_i] - '0');
   }

   // this loop sets the size of the expression operands
   // considered for evaluation, the loop iterates thru the
   // operands in the expression so it loops till size n
   // and starts at 1 since size 0 is already filled
   for (size_t exp_operand_size = 1; exp_operand_size < n; exp_operand_size++)
   {
      cout << "=====================================";

      ll n = (exp.length() + 1) / 2;
      cout << endl << "max_table" << endl;
      for (size_t i = 0; i < n; i++) {
         for (size_t j = 0; j < n; j++)
            cout << max_table[i][j] << "\t";
         cout << endl;
      }


      cout << endl << "min_table" << endl;
      for (size_t i = 0; i < n; i++) {
         for (size_t j = 0; j < n; j++)
            cout << min_table[i][j] << "\t";
         cout << endl;
      }

      // walking thru each operand in the expression, index used here
      // index to tables. since we are using iterating thru different
      // exp_operand_size, loop ends with n - exp_operand_size
      for (size_t exp_operand_start = 0; exp_operand_start < n - exp_operand_size; exp_operand_start++)
      {
         // setting the end point
         size_t exp_operand_end = exp_operand_start + exp_operand_size;

         cout << "exp_operand_start: " << exp_operand_start << " ; exp_end: " << exp_operand_end << endl;

         pair<ll, ll> min_max = get_min_max_value(
                                   exp, max_table, min_table,
                                   exp_operand_start, exp_operand_end);

         // setting DP table with solved sub problems
         min_table[exp_operand_start][exp_operand_end] = get<0>(min_max);
         max_table[exp_operand_start][exp_operand_end] = get<1>(min_max);
      }

      cout << endl << "max_table" << endl;
      for (size_t i = 0; i < n; i++) {
         for (size_t j = 0; j < n; j++)
            cout << max_table[i][j] << "\t";
         cout << endl;
      }


      cout << endl << "min_table" << endl;
      for (size_t i = 0; i < n; i++) {
         for (size_t j = 0; j < n; j++)
            cout << min_table[i][j] << "\t";
         cout << endl;
      }
   }

   // answer will be in the first row
   // and last column of max_table
   return max_table[0][n - 1];
}

int main() {
   string s;
   // cin >> s;
   s = "5-8+7*4-8+9";
   cout << get_maximum_value(s) << '\n';
}
