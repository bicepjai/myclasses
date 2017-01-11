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

struct Request {
   Request(int arrival_time, int process_time):
      arrival_time(arrival_time),
      process_time(process_time)
   {}

   int arrival_time;
   int process_time;
};

struct Response {
   Response(bool dropped, int start_time):
      dropped(dropped),
      start_time(start_time)
   {}

   bool dropped;
   int start_time;
};

class Buffer {
public:
   Buffer(int size):
      size_(size),
      finish_time_()
   {}

   Response Process(const Request &request) {
      // write your code here
      Response response = Response(false, -2);

      // buffer(queue) is empty
      if (finish_time_.empty())
      {
         // cout << "queue empty -> ";
         response.start_time = request.arrival_time;
         finish_time_.push(request.arrival_time + request.process_time);
      }
      // buffer(queue) is not full
      else if (finish_time_.size() < size_)
      {
         // cout << "queue not full -> ";
         // the front of the queue with packet that has finish time
         // less than next packet arrival time, means the processing is over
         // and we can discard the packet
         if (finish_time_.front() <= request.arrival_time)
         {
            // cout << "popped -> ";
            finish_time_.pop();
         }

         //--------------------------------
         // packet arrives before the last packet finish time
         if (request.arrival_time <= finish_time_.back())
         {
            // cout << "arrived b4 ";
            response.start_time = finish_time_.back();
            finish_time_.push(finish_time_.back() + request.process_time);
         }
         // packet arrives after the last packet finish time
         else
         {
            // cout << "arrived after ";
            response.start_time = request.arrival_time;
            finish_time_.push(request.arrival_time + request.process_time);
         }
         //--------------------------------
      }
      // buffer(queue) is full
      else
      {
         // the front of the queue with packet that has finish time
         // less than next packet arrival time, means the processing is over
         // and we can discard the packet
         // cout << "queue full -> ";
         if (finish_time_.front() <= request.arrival_time)
         {
            // cout << "popped -> ";
            finish_time_.pop();

            // if we pop one, then we can process the packet
            // in a similar fashion as when the queue was not full
            //--------------------------------
            // packet arrives before the last packet finish time
            if (request.arrival_time <= finish_time_.back())
            {
               // cout << "arrived b4 ";
               response.start_time = finish_time_.back();
               finish_time_.push(finish_time_.back() + request.process_time);
            }
            // packet arrives after the last packet finish time
            else
            {
               // cout << "arrived after ";
               response.start_time = request.arrival_time;
               finish_time_.push(request.arrival_time + request.process_time);
            }
            //--------------------------------
         }
         // if its greater we have to discard the packet
         else
         {
            // cout << "dropped";
            response.dropped = true;
         }
      }
      // cout << endl;
      return response;
   }

private:
   int size_;
   std::queue <int> finish_time_;
};

std::vector <Request> ReadRequests() {
   std::vector <Request> requests;
   int count;
   std::cin >> count;
   for (int i = 0; i < count; ++i) {
      int arrival_time, process_time;
      std::cin >> arrival_time >> process_time;
      requests.push_back(Request(arrival_time, process_time));
   }
   return requests;
}

std::vector <Response> ProcessRequests(const std::vector <Request> &requests, Buffer *buffer) {
   std::vector <Response> responses;
   for (int i = 0; i < requests.size(); ++i)
      responses.push_back(buffer->Process(requests[i]));
   return responses;
}

void PrintResponses(const std::vector <Response> &responses) {
   for (int i = 0; i < responses.size(); ++i)
      std::cout << (responses[i].dropped ? -1 : responses[i].start_time) << std::endl;
}

int main() {
   int size;
   std::cin >> size;
   std::vector <Request> requests = ReadRequests();

   Buffer buffer(size);
   std::vector <Response> responses = ProcessRequests(requests, &buffer);

   PrintResponses(responses);
   return 0;
}
