

#ifndef RAY_TRACER_H_
#define RAY_TRACER_H_

#include <vector>
#include <limits>
// Include the helper glm library, including matrix transform extensions
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include "glm/ext.hpp"

using namespace glm;
using namespace std;
const double EPSILON = 0.0001;

enum tri_type_en {standard, trinormal} ;
enum light_type_en {point, directional};
vec4 crossVec4(vec4 _v1, vec4 _v2);

class Ray {
public:
	vec4 origin;
	vec4 direction;
	Ray();
	Ray(vec4 origin, vec4 direction);
	string toString();

};

class Camera {
public:
	vec4 eye;
	vec4 center;
	vec4 up;
	double fovy;

	Camera();
	Camera(vec4, vec4, vec4, double);	
	void setDetails(vec4, vec4, vec4, double);
	void printDetails();

	Ray rayThruPixel(int width, int height, int pixel_in_width, int pixel_in_height);
};

class Color 
{
public:
    int  red, green, blue;

	Color();
	Color(double r, double g, double b);

	string toString();
	bool isColorAvailable();
	double getReddouble();
	double getBluedouble();
	double getGreendouble();

	// Overload + operator to add two Color objects.
	Color operator+(Color color)
	{
		return Color (dRed + color.getReddouble(), dGreen + color.getGreendouble(), dBlue + color.getBluedouble());
	}

	Color operator*(Color color)
	{
		return Color (dRed * color.getReddouble(), dGreen * color.getGreendouble(), dBlue * color.getBluedouble());
	}

	Color operator*(double scalar)
	{
		return Color (dRed * scalar, dGreen * scalar, dBlue * scalar);
	}

private:
	double 	dRed, dGreen, dBlue;
	void update255(void);

};


class Light {
public:
	vec4 position;
	Color color;
	light_type_en type;

	Light();
	Light(vec4, Color, light_type_en);

	void setDetails(vec4, Color, light_type_en);
	void setAttenuationConstants(int ,int, int);
	void printDetails();
};

class Object {	
public:
	// lighting stuff
	Color diffuse; 
	Color specular;
	Color emission;
	Color ambient;
	int shininess ;

	Color test_color;
	string test_name;

	mat4 transform;
	mat4 inv_transform;

	Object ();
	
	void setDiffuseColor(Color color) {
		diffuse = color;
	};

	void setSpecularColor(Color color) {
		specular = color;
	};

	void setEmissionColor(Color color) {
		emission = color;
	};

	void setAmbientColor(Color color) {
		ambient = color;
	};

	void setShininess(int s) {
		shininess = s;
	};

	bool isDiffuseAvailable() {
		return diffuse.isColorAvailable();
	}

	bool isSpecularAvailable() {
		return specular.isColorAvailable();
	}

	bool isObjectShinny() {
		return (shininess > 0);
	}

	virtual double findIntersection(Ray ray) = 0;
	virtual void printDetails() {};
	virtual void performTransformation (mat4 trasnf) {};
	virtual vec4 getNormal (vec4 point) = 0;
	virtual Ray getReflectedRay (Ray incident_ray, vec4 object_point) = 0;
	virtual Ray getRefractedRay (Ray incident_ray, vec4 object_point) = 0;
};

class Scene {
public:
	vector<Object*> objects;
	vector<Light*> lights;
	int constant;
	int linear;
	int quadratic;

	Scene ();

	void addLights(Light* light);
	void addObjects(Object* object);

	void setAttenuationConstants(int ,int, int);
	void printDetails();

};

class RayTracer {
public:
	Scene scene;
	int maxdepth;

	RayTracer (Scene, int);

	Color traceThisRay(Ray ray);
private:
	struct IntersectInfo {
		Object* object;
		vec4 object_point;
		vec4 world_point;
		Ray ray_that_hit;
		bool hit_any_object;
		double distance_to_object;

		// in shadow or not
		// if not in shadow, which light
		bool in_shadow;
		Ray light_ray;	
		Light* inlight;
	};

	Ray primary_ray;

	IntersectInfo rayIntersectObjectInfo(Ray ray);
	IntersectInfo tracePrimaryRayIntersection();
	Color traceRays(IntersectInfo);
	Color traceReflectedRays(IntersectInfo , int depth);
	Color computeLight (vec4 direction, vec4 normal, vec4 halfvec, 
		Color lightcolor, Color mydiffuse, Color myspecular, double myshininess);
	//Color computeLight (IntersectInfo );
	IntersectInfo updateShadowInfo(IntersectInfo );
};

class Sphere : public Object {
public:
	vec4 center;
	vec4 center_t;
	double radius;
	double radius_square;

	Sphere ();
	Sphere (vec4, double);

	double findIntersection(Ray ray);
	void printDetails();
	void performTransformation (mat4 trasnf);
	vec4 getNormal (vec4 point);
	Ray getReflectedRay (Ray incident_ray, vec4 object_point);
	Ray getRefractedRay (Ray incident_ray, vec4 object_point);
};

class Triangle : public Object {
public:
	vec4 v1, v2, v3;
	vec4 vn1, vn2, vn3;

	tri_type_en type;

	Triangle ();
	Triangle (vec4, vec4, vec4, tri_type_en);
	
	void setVns(vec4, vec4, vec4);
	double findIntersection(Ray ray);
	void printDetails();
	void performTransformation (mat4 trasnf);
	vec4 getNormal (vec4 point); // dont need point but we will pass it
	Ray getReflectedRay (Ray incident_ray, vec4 object_point);
	Ray getRefractedRay (Ray incident_ray, vec4 object_point);

private:
	vec4 edgev2v1, edgev3v2, edgev1v3;
	vec4 normal_to_triangle_plane;
	double dot_v1_normal_to_triangle_plane;

	void updateSidesAndNormal();
};



#endif