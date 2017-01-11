// Readfile definitions 

#ifndef READFILE_H
#define READFILE_H

#include "variables.h" 
#include "Transform.h"

void matransform (stack<mat4> &transfstack, float * values) ;
void rightmultiply (const mat4 & M, stack<mat4> &transfstack) ;
bool readvals (stringstream &s, const int numvals, float * values) ;
bool readstring(stringstream &s, string &str);
void readfile (char * filename) ;

#endif