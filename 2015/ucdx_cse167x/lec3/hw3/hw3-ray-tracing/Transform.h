
#ifndef TRANSFORM_H_
#define TRANSFORM_H_

#include "variables.h" 

class Transform  
{
public:
	Transform();
	virtual ~Transform();
	
	static void left(double degrees, vec3& eye, vec3& up);
	static void up(double degrees, vec3& eye, vec3& up);

	static mat4 lookAt(const vec3& eye, const vec3 &center, const vec3& up);
	static mat4 perspective(double fovy, double aspect, double zNear, double zFar);

	static mat3 rotate(const double degrees, const vec3& axis) ;
	static mat4 scale(const double &sx, const double &sy, const double &sz) ; 
	static mat4 translate(const double &tx, const double &ty, const double &tz);
	static vec3 upvector(const vec3 &up, const vec3 &zvec) ; 
};

#endif