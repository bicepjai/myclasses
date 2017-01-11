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

// Splay tree implementation

// Vertex of a splay tree
struct Vertex {
   int key;
   // Sum of all the keys in the subtree - remember to update
   // it after each operation that changes the tree.
   long long sum;
   Vertex* left;
   Vertex* right;
   Vertex* parent;

   Vertex(int key, long long sum, Vertex* left, Vertex* right, Vertex* parent)
      : key(key), sum(sum), left(left), right(right), parent(parent) {}
};

// -------------------------------------------------------------------------------
ll height(Vertex* root)
{
   if (root == NULL) return 0;
   return (max(height(root->left), height(root->right)) + 1);
}

ll _print_t(Vertex *tree, ll is_left, ll offset, ll depth, char s[20][255])
{
   char b[20];
   ll width = 5;
   // ll width = 25;

   if (!tree) return 0;

   sprintf(b, "(%lld)", tree->key);
   // sprintf(b, "(%lld)[%d]", tree->key, tree->sum);

   ll left  = _print_t(tree->left,  1, offset,                depth + 1, s);
   ll right = _print_t(tree->right, 0, offset + left + width, depth + 1, s);

#ifdef COMPACT
   for (ll i = 0; i < width; i++)
      s[depth][offset + left + i] = b[i];

   if (depth && is_left) {

      for (ll i = 0; i < width + right; i++)
         s[depth - 1][offset + left + width / 2 + i] = '-';

      s[depth - 1][offset + left + width / 2] = '.';

   } else if (depth && !is_left) {

      for (ll i = 0; i < left + width; i++)
         s[depth - 1][offset - width / 2 + i] = '-';

      s[depth - 1][offset + left + width / 2] = '.';
   }
#else
   for (ll i = 0; i < width; i++)
      s[2 * depth][offset + left + i] = b[i];

   if (depth && is_left) {

      for (ll i = 0; i < width + right; i++)
         s[2 * depth - 1][offset + left + width / 2 + i] = '-';

      s[2 * depth - 1][offset + left + width / 2] = '+';
      s[2 * depth - 1][offset + left + width + right + width / 2] = '+';

   } else if (depth && !is_left) {

      for (ll i = 0; i < left + width; i++)
         s[2 * depth - 1][offset - width / 2 + i] = '-';

      s[2 * depth - 1][offset + left + width / 2] = '+';
      s[2 * depth - 1][offset - width / 2 - 1] = '+';
   }
#endif

   return left + width + right;
}

void print_t(Vertex *tree)
{
   char s[20][255];
   for (ll i = 0; i < 20; i++)
      sprintf(s[i], "%80s", " ");

   _print_t(tree, 0, 0, 0, s);

   for (ll i = 0; i < 2 * height(tree); i++)
      printf("%s\n", s[i]);
}
// -------------------------------------------------------------------------------

void update(Vertex* v) {
   if (v == NULL) return;
   v->sum = v->key + (v->left != NULL ? v->left->sum : 0ll) + (v->right != NULL ? v->right->sum : 0ll);
   if (v->left != NULL) {
      v->left->parent = v;
   }
   if (v->right != NULL) {
      v->right->parent = v;
   }
}

void small_rotation(Vertex* v) {
   Vertex* parent = v->parent;
   if (parent == NULL) {
      return;
   }
   Vertex* grandparent = v->parent->parent;
   if (parent->left == v) {
      Vertex* m = v->right;
      v->right = parent;
      parent->left = m;
   } else {
      Vertex* m = v->left;
      v->left = parent;
      parent->right = m;
   }
   update(parent);
   update(v);
   v->parent = grandparent;
   if (grandparent != NULL) {
      if (grandparent->left == parent) {
         grandparent->left = v;
      } else {
         grandparent->right = v;
      }
   }
}

void big_rotation(Vertex* v) {
   if (v->parent->left == v && v->parent->parent->left == v->parent) {
      // Zig-zig
      small_rotation(v->parent);
      small_rotation(v);
   } else if (v->parent->right == v && v->parent->parent->right == v->parent) {
      // Zig-zig
      small_rotation(v->parent);
      small_rotation(v);
   } else {
      // Zig-zag
      small_rotation(v);
      small_rotation(v);
   }
}

// Makes splay of the given vertex and makes
// it the new root.
void splay(Vertex*& root, Vertex* v) {
   if (v == NULL) return;
   while (v->parent != NULL) {
      if (v->parent->parent == NULL) {
         small_rotation(v);
         break;
      }
      big_rotation(v);
   }
   root = v;
}

// Searches for the given key in the tree with the given root
// and calls splay for the deepest visited node after that.
// If found, returns a pointer to the node with the given key.
// Otherwise, returns a pointer to the node with the smallest
// bigger key (next value in the order).
// If the key is bigger than all keys in the tree,
// returns NULL.
Vertex* find(Vertex*& root, int key) {
   Vertex* v = root;
   Vertex* last = root;
   Vertex* next = NULL;
   while (v != NULL) {
      if (v->key >= key && (next == NULL || v->key < next->key)) {
         next = v;
      }
      last = v;
      if (v->key == key) {
         break;
      }
      if (v->key < key) {
         v = v->right;
      } else {
         v = v->left;
      }
   }
   splay(root, last);
   return next;
}

void split(Vertex* root, int key, Vertex*& left, Vertex*& right) {
   right = find(root, key);
   splay(root, right);
   if (right == NULL) {
      left = root;
      return;
   }
   left = right->left;
   right->left = NULL;
   if (left != NULL) {
      left->parent = NULL;
   }
   update(left);
   update(right);
}

Vertex* merge(Vertex* left, Vertex* right) {
   if (left == NULL) return right;
   if (right == NULL) return left;
   Vertex* min_right = right;
   while (min_right->left != NULL) {
      min_right = min_right->left;
   }
   splay(right, min_right);
   right->left = left;
   update(right);
   return right;
}

// Code that uses splay tree to solve the problem

Vertex* root = NULL;

void insert(int x) {
   Vertex* left = NULL;
   Vertex* right = NULL;
   Vertex* new_vertex = NULL;
   // cout << "iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii" << endl;
   // if (root)
   //    cout << "root-> " <<  root->key << endl;
   // print_t(root);

   Vertex* found = find(root, x);
   if (found != NULL && found->key == x) {
      return;
   }

   split(root, x, left, right);
   if (right == NULL || right->key != x) {
      new_vertex = new Vertex(x, x, NULL, NULL, NULL);
   }
   root = merge(merge(left, new_vertex), right);


   // if (root)
   //    cout << "root-> " <<  root->key << endl;
   // print_t(root);
   // cout << "iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii" << endl;
}

void inorder_print(Vertex* root)
{
   if (root == NULL)
      return;
   if (root->left)
      inorder_print(root->left);

   cout << root->key << " ";

   if (root->right)
      inorder_print(root->right);
}

void preorder_print(Vertex* root)
{
   if (root == NULL)
      return;

   cout << root->key << " ";

   if (root->left)
      preorder_print(root->left);

   if (root->right)
      preorder_print(root->right);
}

void postorder_print(Vertex* root)
{
   if (root == NULL)
      return;

   if (root->left)
      postorder_print(root->left);

   if (root->right)
      postorder_print(root->right);

   cout << root->key << " ";
}

void erase(int x) {
   // Implement erase yourself
   Vertex* left = NULL;
   Vertex* right = NULL;
   Vertex* current = NULL;

   // cout << "---------------------------------" << endl;
   // if (root)
   //    cout << "root-> " <<  root->key << endl;
   // print_t(root);

   Vertex* found = find(root, x);
   if (found != NULL && found->key == x) {
      // cout << "found-> " << x << endl;
      splay(root, found);
      // cout << "splayed root-> " << root->key << endl;
      // print_t(root);

      if (root) {
         // cout << endl;
         // inorder_print(root);
         // cout << endl;
         // preorder_print(root);
         // cout << endl;
         // postorder_print(root);
         // cout << endl;

         // cout << "root->left-> ";
         // if (root->left) {
         //    cout <<  root->left->key << endl;

         //    cout << "root->left->parent-> ";
         //    if (root->left->parent)
         //       cout <<  root->left->parent->key << endl;
         // }
         // else
         //    cout << endl;

         // cout << "root->right-> ";
         // if (root->right) {
         //    cout << root->right->key << endl;

         //    cout << "root->right->parent-> ";
         //    if (root->right->parent)
         //       cout <<  root->right->parent->key << endl;
         // }
         // else
         //    cout << endl;

         root = merge(root->left, root->right);
         if (root)
            root->parent = NULL;
      }
   }

   // if (root)
   //    cout << "root-> " <<  root->key << endl;
   // print_t(root);
   // cout << "---------------------------------" << endl;

}

bool find(int x) {
   // Implement find yourself
   bool ret = false;

   // cout << "-?????????????????????????-" << endl;
   // if (root)
   //    cout << "root-> " <<  root->key << endl;
   // print_t(root);

   if (root == NULL) {
      return ret;
   }

   Vertex* found = find(root, x);

   if (found != NULL && found->key == x) {
      ret = true;
   }

   // if (root)
   //    cout << "root-> " <<  root->key << endl;

   // print_t(root);
   // cout << "-?????????????????????????-" << endl;

   return ret;
}

long long sum(int from, int to) {
   Vertex* left = NULL;
   Vertex* middle = NULL;
   Vertex* right = NULL;

   // cout << "+++++++++++++++++++++++++++++++++" << endl;
   // if (root)
   //    cout << "root-> " <<  root->key << endl;
   // print_t(root);

   split(root, from, left, middle);
   split(middle, to + 1, middle, right);
   long long ans = 0;

   // Vertex* temp = NULL;

   // cout << "++++ sum-left +++++++++++++++++++++" << endl;
   // temp = left;
   // if (temp) {
   //    cout << "temp->key: " <<  temp->key << endl;
   //    cout << "temp->left-> ";
   //    if (temp->left) {
   //       cout << temp->left->key << endl;

   //       cout << "temp->left->parent-> ";
   //       if (temp->left->parent)
   //          cout <<  temp->left->parent->key << endl;
   //    }
   //    else
   //       cout << endl;

   //    cout << "temp->right-> ";
   //    if (temp->right) {
   //       cout << temp->right->key << endl;

   //       cout << "temp->right->parent-> ";
   //       if (temp->right->parent)
   //          cout <<  temp->right->parent->key << endl;
   //    }
   //    else
   //       cout << endl;
   // }

   // cout << "++++ sum-middle +++++++++++++++++++++" << endl;
   // temp = middle;
   // if (temp) {
   //    cout << "temp->key: " <<  temp->key << endl;
   //    cout << "temp->left-> ";
   //    if (temp->left) {
   //       cout << temp->left->key << endl;

   //       cout << "temp->left->parent-> ";
   //       if (temp->left->parent)
   //          cout <<  temp->left->parent->key << endl;
   //    }
   //    else
   //       cout << endl;

   //    cout << "temp->right-> ";
   //    if (temp->right) {
   //       cout << temp->right->key << endl;

   //       cout << "temp->right->parent-> ";
   //       if (temp->right->parent)
   //          cout <<  temp->right->parent->key << endl;
   //    }
   //    else
   //       cout << endl;
   // }

   // cout << "++++ sum-right +++++++++++++++++++++" << endl;
   // temp = right;
   // if (temp) {
   //    cout << "temp->key: " <<  temp->key << endl;
   //    cout << "temp->left-> ";
   //    if (temp->left) {
   //       cout << temp->left->key << endl;

   //       cout << "temp->left->parent-> ";
   //       if (temp->left->parent)
   //          cout <<  temp->left->parent->key << endl;
   //    }
   //    else
   //       cout << endl;

   //    cout << "temp->right-> ";
   //    if (temp->right) {
   //       cout << temp->right->key << endl;

   //       cout << "temp->right->parent-> ";
   //       if (temp->right->parent)
   //          cout <<  temp->right->parent->key << endl;
   //    }
   //    else
   //       cout << endl;
   // }

   // Complete the implementation of sum
   if (middle != NULL)
   {
      // cout << "middle->key: " << middle->key << endl;
      // cout << "from: " << from <<  " to: "<< to << endl;
      if(middle->key <= to && middle->key >= from)
         ans = middle->sum;
   }

   root = merge(merge(left, middle), right);

   // if (root)
   //    cout << "root-> " <<  root->key << endl;
   // print_t(root);

   // cout << "+++++++++++++++++++++++++++++++++" << endl;

   return ans;
}

const int MODULO = 1000000001;

int main() {
   int n;
   scanf("%d", &n);
   int last_sum_result = 0;
   for (int i = 0; i < n; i++) {
      char buffer[10];
      scanf("%s", buffer);
      char type = buffer[0];
      switch (type) {
      case '+' : {
         int x;
         scanf("%d", &x);
         // cout << "**************** inserting: " << (x + last_sum_result) % MODULO << endl;
         insert((x + last_sum_result) % MODULO);
      } break;
      case '-' : {
         int x;
         scanf("%d", &x);
         // cout << "****************deleting: " << (x + last_sum_result) % MODULO << endl;
         erase((x + last_sum_result) % MODULO);
      } break;
      case '?' : {
         int x;
         scanf("%d", &x);
         // cout << "****************finding: " << (x + last_sum_result) % MODULO << endl;
         printf(find((x + last_sum_result) % MODULO) ? "Found\n" : "Not found\n");
      } break;
      case 's' : {
         int l, r;
         scanf("%d %d", &l, &r);
         // cout << "****************sum from " << (l + last_sum_result) % MODULO << " to " << (r + last_sum_result) % MODULO << endl;
         long long res = sum((l + last_sum_result) % MODULO, (r + last_sum_result) % MODULO);
         printf("%lld\n", res);
         last_sum_result = int(res % MODULO);
      }
      }
   }
   return 0;
}
