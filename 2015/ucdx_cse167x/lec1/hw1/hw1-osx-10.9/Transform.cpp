// Transform.cpp: implementation of the Transform class.


#include "Transform.h"
#include <stdio.h>

//Please implement the following functions:

// Helper rotation function.  
mat3 Transform::rotate(const float degrees, const vec3& axis) {
	mat3 axisSkew = mat3(
   		0, axis.z, -axis.y, // first column 
		-axis.z, 0, axis.x, // second column
		axis.y, -axis.x, 0  // third column
	);
 	return 	(glm::cos(glm::radians(degrees)) * mat3(1.0f)) + 
 			((1-glm::cos(glm::radians(degrees))) * glm::core::function::matrix::outerProduct(axis, axis)) +
 			(glm::sin(glm::radians(degrees)) * axisSkew);
}

// Transforms the camera left around the "crystal ball" interface
void Transform::left(float degrees, vec3& eye, vec3& up) {
	// YOUR CODE FOR HW1 HERE
	eye = eye * Transform::rotate(-degrees, up);
	//printf("Left:Degrees: %.2f; Coordinates: %.2f, %.2f, %.2f; distance: %.2f\n", degrees, eye.x, eye.y, eye.z, sqrt(pow(eye.x, 2) + pow(eye.y, 2) + pow(eye.z, 2)));
}

// Transforms the camera up around the "crystal ball" interface
void Transform::up(float degrees, vec3& eye, vec3& up) {
	// YOUR CODE FOR HW1 HERE
	vec3 axis = glm::normalize(glm::cross(eye,up));
	eye = eye * Transform::rotate(-degrees, axis);
	up = up * Transform::rotate(-degrees, axis);
	//printf("Up:Degrees: %.2f; Coordinates: %.2f, %.2f, %.2f; distance: %.2f\n", degrees, eye.x, eye.y, eye.z, sqrt(pow(eye.x, 2) + pow(eye.y, 2) + pow(eye.z, 2)));
}

// Your implementation of the glm::lookAt matrix
mat4 Transform::lookAt(vec3 eye, vec3 up) {
  	// YOUR CODE FOR HW1 HERE
	vec3 w = glm::normalize(eye);
	vec3 u = glm::normalize(glm::cross(up, w));
	vec3 v = glm::cross(w, u);
	
  	return 	mat4(
  				u.x, v.x, w.x, 0,
  				u.y, v.y, w.y, 0,
  				u.z, v.z, w.z, 0,
  				0  , 0  , 0  , 1
  			) * 
  			mat4(
  				1, 0, 0, 0,
  				0, 1, 0, 0,
  				0, 0, 1, 0,
  				-eye.x, -eye.y, -eye.z, 1
  			);
}

Transform::Transform()
{

}

Transform::~Transform()
{

}
