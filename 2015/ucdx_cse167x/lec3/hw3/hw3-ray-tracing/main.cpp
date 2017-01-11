

// Main variables in the program.  
#define MAINPROGRAM 
#include "variables.h" 
#include "readfile.h" // prototypes for readfile.cpp  

#include <thread>
#include <boost/thread.hpp>

using namespace std;
using namespace glm;

static inline void loadbar(unsigned int x, unsigned int n, unsigned int w = 50)
{
    if ( (x != n) && (x % (n/100+1) != 0) ) return;
 
    float ratio  =  x/(float)n;
    int   c      =  ratio * w;
 
    cout << setw(3) << (int)(ratio*100) << "% [";
    for (int x=0; x<c; x++) cout << "=";
    for (int x=c; x<w; x++) cout << " ";
    cout << "]\r" << flush;
}

FIBITMAP *bitmap;

void threadFunction(RayTracer ray_tracer, int w) {
	for(int h=0;h<height;h++)
	{
		Ray ray = camera.rayThruPixel(width, height, w, h);
		Color col = ray_tracer.traceThisRay(ray);
		RGBQUAD color;
		color.rgbRed = col.blue;
		color.rgbGreen =  col.green;
		color.rgbBlue =  col.red;
		FreeImage_SetPixelColor(bitmap,w,h,&color);
	}	
}

int main(int argc,char* argv[]) {
	FreeImage_Initialise();

	readfile(argv[1]);
  	// checking with prints

  	camera.printDetails();
  	scene.printDetails();

	bitmap = FreeImage_Allocate(width, height, 24);

	RayTracer ray_tracer(scene, maxdepth);
	int npixels = width*height;


	// Color spec(.6,.6,.4);
	// Color light(1,1,1);
	// cout << std::pow(std::max(abs(0.283329), 0.0), 20) << endl;
	// cout << (spec * light * std::pow(std::max(abs(0.283329), 0.0), 20)).toString() << "\n";

	for(int w=0;w<width;w++)
	{
		for(int h=0;h<height;h++)
		{
			Ray ray = camera.rayThruPixel(width, height, w, h);
			Color col = ray_tracer.traceThisRay(ray);
			//cout << "<" << w << "," << h << "> (" << col.red << ","<< col.green << ","<< col.blue << ") \n";
			RGBQUAD color;
			color.rgbRed = col.blue;
			color.rgbGreen =  col.green;
			color.rgbBlue =  col.red;
			FreeImage_SetPixelColor(bitmap,w,h,&color);
			loadbar(w*height+h+1,npixels);
		}		
	}

	// boost::thread_group trace_threads;
	// for(int w=0;w<width;w++)
	// {
	// 	trace_threads.create_thread( boost::bind( threadFunction, ray_tracer, w ) );
	// }
	// trace_threads.join_all();

	// vec4 a(1,2,2,1);
	// vec4 b(2,2,2,2);
	// cout << a*b << "\n";

	cout << "\nSaving ray traced image: " << output_filename << "\n";
	FreeImage_FlipVertical(bitmap);
  	FreeImage_Save(FIF_PNG, bitmap, output_filename.c_str(), 0);


  	FreeImage_DeInitialise();
	return 0;
}