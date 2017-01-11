
#ifndef VARIABLES_H_
#define VARIABLES_H_

#include <iostream>
#include <string>
#include <sstream>
#include <fstream>
#include <vector>
#include <FreeImage.h>

// Basic includes to get this file to work.  
#include <deque>
#include <stack>
#include <iostream>     // std::cout, std::endl
#include <iomanip>      // std::setw

#ifdef MAINPROGRAM 
#define EXTERN 
#else 
#define EXTERN extern 
#endif 

// Include the helper glm library, including matrix transform extensions
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include "glm/ext.hpp"

#include "RayTracer.h"

using namespace std;
using namespace glm;

// glm provides vector, matrix classes like glsl
// Typedefs to make code more readable 
typedef glm::mat3 mat3 ;
typedef glm::mat4 mat4 ; 
typedef glm::vec3 vec3 ; 
typedef glm::vec4 vec4 ; 

const double pi = 3.14159265 ; // For portability across platforms

EXTERN Camera camera;
EXTERN Scene scene;

#ifdef MAINPROGRAM 
  int width = 600, height = 400 ; // width and height
  int maxdepth = 5;
  string output_filename = "ray-traced.png";
#else 
    EXTERN int width, height ; 
    EXTERN int maxdepth;
    EXTERN string output_filename;
#endif 

// For multiple objects, read from a file.  
const int maxobjects = 10 ; 
EXTERN int numobjects ; 
EXTERN int maxverts;
EXTERN int maxvertnorms;

EXTERN vector<vec4> vertex_positions;
EXTERN vector<vec4> vertexnormal_positions;
EXTERN vector<vec4> vertexnormal_npositions;
EXTERN vector<Object*> objects;

EXTERN double ambient_backup[3];
EXTERN double diffuse_backup[3];
EXTERN double specular_backup[3];
EXTERN int shininess_backup;
EXTERN double emission_backup[3];

#endif