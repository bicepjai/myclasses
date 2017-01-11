
#include "RayTracer.h"
using namespace glm;
using namespace std;

// RAY

Ray::Ray()
{
	origin = vec4(0,0,0,0);
	direction = vec4(0,0,-1,0);
}

Ray::Ray(vec4 o, vec4 d)
{
	origin 		= o;
	direction 	= d;
}

string Ray::toString()
{
	return(" o: " + to_string(origin) + "d: " + to_string(direction));
}

// CAMERA

Camera::Camera() {
  eye = vec4(0.0,0.0,5.0,0) ; // Initial eye position, also for resets
  up = vec4(0.0,1.0,0.0,0) ; // Initial up position, also for resets
  center = vec4(0.0,0.0,0.0,0) ; // Center look at point 
  fovy = 90.0 ; // For field of view

}

Camera::Camera (vec4 v1, vec4 v2, vec4 v3, double fovy) {
	eye = v1;
	center = v2;
	up = v3;
	fovy = fovy;
}

void Camera::setDetails (vec4 v1, vec4 v2, vec4 v3, double fov) {
	eye = v1;
	center = v2;
	up = v3;
	fovy = fov;
}

void Camera::printDetails () {
	cout << "\n==> Camera Info: \n";
	cout << "eye: " << to_string(eye) << "\n";
	cout << "center: " << to_string(center) << "\n";
	cout << "up: " << to_string(up) << "\n";
	cout << "fovy: " << fovy << "\n";
}


Ray Camera::rayThruPixel(int width, int height, int pixel_in_width, int pixel_in_height) {
	vec4 w = normalize(eye - center);
	vec4 u = normalize(crossVec4(up, w));
	vec4 v = crossVec4(w, u);

	double a = tan(radians(fovy/2)) * ((double)width/(double)height) * (pixel_in_width + 0.5 - width/2) / (width/2);
	double b = tan(radians(fovy/2)) * (height/2 - pixel_in_height - 0.5) / (height/2);

	Ray ray(eye, normalize(a*u + b*v - w));
	return (ray);
}

// COLOR 

Color::Color() {}


Color::Color(double r, double g, double b) {
	dRed=r; dGreen=g; dBlue=b;
	update255();
}

void Color::update255() {
	red=int(255*dRed); green=int(255*dGreen); blue=int(255*dBlue);
}

double Color::getReddouble() {
	return dRed;
}

double Color::getBluedouble() {
	return dBlue;
}

double Color::getGreendouble() {
	return dGreen;
}

bool Color::isColorAvailable() {
	if (red == 0 && green == 0 && blue == 0) {
		return false;
	} else {
		return true;
	}
}

// string Color::toString() {
// 	return ("r: " + std::to_string(red) + " g:" + std::to_string(green) + " b:" + std::to_string(blue));
// }
string Color::toString() {
	return ("(" + std::to_string(red) + "," + std::to_string(green) + "," + std::to_string(blue) + ")");
}

// OBJECT 

Object::Object () {
	ambient = Color(0.2,0.2,0.2);
	transform = mat4(1.0);
	test_color = Color(0,0,0);
}

// LIGHTS

Light::Light (vec4 p, Color c, light_type_en t)  {
	position = p;
	color = c;
	type = t;
}

void Light::setDetails (vec4 p, Color c, light_type_en t)  {
	position = p;
	color = c;
	type = t;
}

void Light::printDetails () {
	cout << "\n==> Light Info: \n";
	cout << "position: " << to_string(position) << "\n";
	cout << "color: " << color.toString() << "\n";
	if(type == point){
		cout << "type: point\n";		
	} else 	if(type == directional){
		cout << "type: directional\n";		
	} else {
		cout << "type: unknown\n";		
	}
}

// SCENE 
Scene::Scene() {
}

void Scene::addLights(Light* light)  {
	lights.push_back(light);
}

void Scene::addObjects(Object* object) {
	objects.push_back(object);
}

void Scene::setAttenuationConstants(int c, int l, int q) {
	constant = c;
	linear = l;
	quadratic = q;
}

void Scene::printDetails() {
	cout << "\n==> Scene Info: \n";
	for(std::vector<Light*>::iterator light = lights.begin(); light != lights.end(); ++light) {
	    (*light)->printDetails();
	}
	for(std::vector<Object*>::iterator object = objects.begin(); object != objects.end(); ++object) {
	    (*object)->printDetails();
	}
	cout << "attenuation:constant: " << constant << "\n";
	cout << "attenuation:linear: " << linear << "\n";
	cout << "attenuation:quadratic: " << quadratic << "\n";
}

// RAY TRACER

RayTracer::RayTracer (Scene sce, int d) {
	scene = sce;
	maxdepth = d;
}

Color RayTracer::traceThisRay(Ray ray) {
	primary_ray = ray;
	IntersectInfo primary_intersect_info = tracePrimaryRayIntersection();
	if(primary_intersect_info.hit_any_object) {
		Color rayColor = traceRays(primary_intersect_info);
		return(	primary_intersect_info.object->ambient + 
				primary_intersect_info.object->emission +
				rayColor );
	}
	else {
		return(Color(0,0,0));
	}
}

RayTracer::IntersectInfo RayTracer::tracePrimaryRayIntersection() {
	IntersectInfo intersect_info = rayIntersectObjectInfo(primary_ray);
	return intersect_info;
}

Color RayTracer::traceRays(IntersectInfo intersected_info) {
	Color final_color(0,0,0);
	
	IntersectInfo updated_info = updateShadowInfo(intersected_info);
	if(!updated_info.in_shadow) {

		vec4 normal_world_cord = updated_info.object->getNormal(updated_info.object_point);
		vec4 halfvec = normalize(updated_info.light_ray.direction + updated_info.ray_that_hit.direction) ;
		final_color = final_color + computeLight(
					updated_info.light_ray.direction, normal_world_cord, halfvec, 
					updated_info.inlight->color, 
					updated_info.object->diffuse, 
					updated_info.object->specular, 
					updated_info.object->shininess);
		//cout << " illuminate object: " << updated_info.object->test_name << "col: " << final_color.toString() << endl;
		if(refl_inter_info.object->isSpecularAvailable())
		final_color = final_color + traceReflectedRays(updated_info, maxdepth);
	}
	return (final_color);
}


Color RayTracer::traceReflectedRays(IntersectInfo intersect_info, int depth) {

	if (depth < 0) {
		cout << " at depth:"<< depth << " wtf "<< "\n";
		return(Color(0,0,0));
	} else {
		// Ray ray_t(intersect_info.object->inv_transform * intersect_info.ray_that_hit.origin, intersect_info.object->inv_transform * intersect_info.ray_that_hit.direction);
		Ray ray_t = intersect_info.ray_that_hit;
		Ray reflected = intersect_info.object->getReflectedRay(ray_t, intersect_info.object_point);
		
		// reflected = Ray(	intersect_info.object->transform * reflected.origin, 
								// intersect_info.object->inv_transform * reflected.direction);

		reflected.origin = intersect_info.world_point;
		IntersectInfo refl_inter_info = rayIntersectObjectInfo(reflected);

		Color refl_color(0,0,0);
		IntersectInfo shadow_test_info = updateShadowInfo(refl_inter_info);
		if(!shadow_test_info.in_shadow) {
			cout << " at depth:"<< depth << " ray from " << intersect_info.object->test_name << " hit: "<< refl_inter_info.object->test_name << endl;

			vec4 normal_world_cord = refl_inter_info.object->getNormal(refl_inter_info.object_point);
			vec4 halfvec = normalize (shadow_test_info.ray_that_hit.direction + intersect_info.ray_that_hit.direction) ;
			refl_color = computeLight(
					shadow_test_info.light_ray.direction, normal_world_cord, halfvec, 
					shadow_test_info.inlight->color, 
					shadow_test_info.object->diffuse, 
					shadow_test_info.object->specular, 
					shadow_test_info.object->shininess);
			cout << " at_depth:"<< depth << " ray_from:" << intersect_info.object->test_name << " color:" <<  refl_color.toString() << "\n";

			return (refl_color + traceReflectedRays(refl_inter_info, depth - 1));
		}			
	}
	return(Color(0,0,0));
}

RayTracer::IntersectInfo RayTracer::updateShadowInfo(IntersectInfo intersect_info) {
	IntersectInfo updated_info = intersect_info;
	for(std::vector<Light*>::iterator light = scene.lights.begin(); light != scene.lights.end(); ++light) {

		vec4 light_direction;
		if ((*light)->type == point) {
			light_direction = normalize((*light)->position - intersect_info.world_point);
		} else if ((*light)->type == directional) {
		 	light_direction = normalize((*light)->position); // position is direction
		}
		light_direction.w = 0;
		intersect_info.world_point.w = 1;

		Ray ray((intersect_info.world_point) + EPSILON * light_direction, light_direction);
		IntersectInfo hit_info = rayIntersectObjectInfo(ray);

		updated_info.light_ray = ray;
		updated_info.inlight = (*light);
		updated_info.in_shadow = hit_info.hit_any_object;

 	// 	if(updated_info.in_shadow) {
		// 	cout << intersect_info.in_shadow << " ray from " << intersect_info.object->test_name << " hit: "<< hit_info.object->test_name << "\n";		
		// }
		return updated_info;
	}
	return updated_info;
}

RayTracer::IntersectInfo RayTracer::rayIntersectObjectInfo(Ray ray) {

	bool hit_any_object = false;
	double min_distance = std::numeric_limits<double>::max();
	Object* intersect_object;
	IntersectInfo intersect_info;
	intersect_info.ray_that_hit = ray;	
	Ray ray_t;

	for(std::vector<Object*>::iterator object = scene.objects.begin(); object != scene.objects.end(); ++object) {
		ray_t = Ray((*object)->inv_transform * ray.origin,(*object)->inv_transform * ray.direction);
		double distance_to_object = (*object)->findIntersection(ray_t);
	    if( distance_to_object > EPSILON && distance_to_object < min_distance) {
	    	intersect_object = (*object);
	    	min_distance = distance_to_object;
	    	hit_any_object = true;
		}
	}

	if(hit_any_object) {
		intersect_info.distance_to_object = min_distance;
		intersect_info.object = intersect_object;
		intersect_info.world_point = (ray.origin + min_distance * ray.direction);		
		intersect_info.object_point= intersect_object->inv_transform * intersect_info.world_point;

	}
   	intersect_info.hit_any_object = hit_any_object;
	return 	intersect_info;
}

Color RayTracer::computeLight (vec4 direction, vec4 normal, vec4 halfvec, 
	Color lightcolor, Color mydiffuse, Color myspecular, double myshininess) {

    double nDotL = dot(normal, direction)  ;         
    Color lambert = mydiffuse * lightcolor * std::max (abs(nDotL), 0.0) ;  

    double nDotH = dot(normal, halfvec) ;
    cout << " nDotH:" << nDotH << " normal:" << to_string(normal) << " halfvec:"<< to_string(halfvec) << endl;
    cout << " shini:"<< myshininess << " specular:" << myspecular.toString() << " lightcolor:" << lightcolor.toString() << endl;
    Color phong = myspecular * lightcolor * std::pow (std::max(abs(nDotH), 0.0), myshininess) ; 
    cout << " lambert:"<< lambert.toString() << " phong: " <<  phong.toString() << endl << endl;
    return (lambert + phong); 
}

// SPHERE

Sphere::Sphere () {
	center = vec4(0,0,0,0);
	radius = 1.0;
	radius_square = radius*radius;
	test_color = Color(0,255,0);
}

Sphere::Sphere (vec4 c, double r) {
	center = c;
	radius = r;
	radius_square = radius*radius;
	test_color = Color(0,255,0);
}

void Sphere::performTransformation (mat4 transf) {
	transform = transf;
	inv_transform = inverse(transform);
}

void Sphere::printDetails() {
	cout << "\n==> Sphere Info: \n";
	cout << "center: " << to_string(center) << "\n";
	cout << "radius: " << radius << "\n";
	cout << "ambient: " << ambient.toString() << "\n";
	cout << "diffuse: " << diffuse.toString() << "\n";
	cout << "specular: " << specular.toString() << "\n";
	cout << "emission: " << emission.toString() << "\n";	
	cout << "shininess: " << shininess << "\n";		
}

vec4 Sphere::getNormal (vec4 point_on_object) {
	vec4 normal_object_cord = normalize(point_on_object - center);
	vec4 normal_world_cord = normalize(transpose(inv_transform) * normal_object_cord);
	return normal_world_cord;
}

Ray Sphere::getReflectedRay (Ray incident_ray, vec4 object_point) {
	//cout << "in getReflectedRay incident_ray " << incident_ray.toString() << "\n";
	vec4 normal = getNormal(object_point);
	double cosI = dot(normal,incident_ray.direction);
	vec4 reflected_direction = -normalize(incident_ray.direction - 2*cosI*normal);
	return (Ray(object_point, reflected_direction));
}

Ray Sphere::getRefractedRay (Ray incident_ray, vec4 object_point) {
	vec4 normal = getNormal(object_point);
	double n = 1;
	double cosI = dot(normal,incident_ray.direction);
	double sinT2 = n * n * (1.0 - cosI*cosI);
	if(sinT2 > 1.0) {
		cout << "Invalid refractions\n";
	}
	vec4 refracted_direction = normalize(n * incident_ray.direction - (n + sqrt(1.0 - sinT2)) * normal);
	return (Ray(object_point, refracted_direction));
}

double Sphere::findIntersection(Ray ray_t) {
	// sphere equation solution	
	double a = dot(ray_t.direction,ray_t.direction); // normalized
	double b = 2 * dot(ray_t.direction, ray_t.origin - center);
	double c = dot(ray_t.origin - center, ray_t.origin - center)- radius_square;
	
	double discriminant = b*b - 4*a*c;
	
	if (discriminant > 0) {
		/// the ray intersects the sphere
		
		// the first root
		double root_1 = ((-1*b - sqrt(discriminant))/(a*2));
		
		if (root_1 > 0) {
			// the first root is the smallest positive root
			return root_1;
		}
		else {
			// the second root is the smallest positive root
			double root_2 = ((-1*b + sqrt(discriminant))/(a*2));
			if (root_2 > 0) {
				return root_2;
			}
		}
	}
	// the ray missed the sphere
	return -1;
}

// TRIANGLE

void Triangle::updateSidesAndNormal() {
	edgev2v1 = v2-v1;
	edgev3v2 = v3-v2;
	edgev1v3 = v1-v3;
	normal_to_triangle_plane = normalize(crossVec4(v1-v2, v1-v3));
	dot_v1_normal_to_triangle_plane = dot(v1, normal_to_triangle_plane);

	test_color = Color(255,0,0);
}

Triangle::Triangle () {
	v1 = vec4(0,0,0,0);
	v2 = vec4(0,0,0,0);
	v3 = vec4(0,0,0,0);
	type = standard;
	this->updateSidesAndNormal();
}

Triangle::Triangle (vec4 ve1, vec4 ve2, vec4 ve3, tri_type_en type) {
	v1 = ve1; v2 = ve2; v3 = ve3;
	type = type;
	this->updateSidesAndNormal();	
}

void Triangle::setVns(vec4 ve1, vec4 ve2, vec4 ve3) {
	if(type == trinormal)
	{
		vn1 = ve1; vn2 = ve2; vn3 = ve3;
	}
}

void Triangle::performTransformation (mat4 transf) {
	transform = transf;
	inv_transform = inverse(transform);
	this->updateSidesAndNormal();	
}

void Triangle::printDetails() {
	cout << "\n==> Triangle Info: \n";
	cout << "v1: " << to_string(v1) << "\n";
	cout << "v2: " << to_string(v2) << "\n";
	cout << "v3: " << to_string(v3) << "\n";
	if(type == standard){
		cout << "type: standard\n";		
	} else 	if(type == trinormal){
		cout << "type: trinormal\n";		
	} else {
		cout << "type: unknown\n";		
	}	
	cout << "ambient: " << ambient.toString() << "\n";
	cout << "diffuse: " << diffuse.toString() << "\n";
	cout << "specular: " << specular.toString() << "\n";
	cout << "emission: " << emission.toString() << "\n";	
	cout << "shininess: " << shininess << "\n";		
}

vec4 Triangle::getNormal (vec4 point_on_object) {
	return normal_to_triangle_plane;
}

Ray Triangle::getReflectedRay (Ray incident_ray, vec4 object_point) {
	//cout << "in getReflectedRay incident_ray " << incident_ray.toString() << "\n";
	double cosI = dot(normal_to_triangle_plane,incident_ray.direction);
	vec4 reflected_direction = -normalize(incident_ray.direction - 2*cosI*normal_to_triangle_plane);
	return (Ray(object_point, reflected_direction));
}

Ray Triangle::getRefractedRay (Ray incident_ray, vec4 object_point) {
	double n = 1;
	double cosI = dot(normal_to_triangle_plane,incident_ray.direction);
	double sinT2 = n * n * (1.0 - cosI*cosI);
	if(sinT2 > 1.0) {
		cout << "Invalid refractions\n";
	}
	vec4 refracted_direction = normalize(n * incident_ray.direction - (n + sqrt(1.0 - sinT2)) * normal_to_triangle_plane);
	return (Ray(object_point, refracted_direction));
}

double Triangle::findIntersection(Ray ray_t) {

	double normal_dot_dir = dot(normal_to_triangle_plane, ray_t.direction);
	if(fabs(normal_dot_dir) < EPSILON) return -1;

	double distance_to_plane = ( dot_v1_normal_to_triangle_plane - dot(ray_t.origin, normal_to_triangle_plane))/(dot(ray_t.direction, normal_to_triangle_plane));
	
	if (distance_to_plane < EPSILON) return -2;

	vec4 point_on_plane = ray_t.origin + (distance_to_plane * ray_t.direction);
	vec4 p_origin = point_on_plane - ray_t.origin;

	if(dot(crossVec4(ray_t.origin - v2, ray_t.origin - v3), p_origin) > 0) return -3;	
	if(dot(crossVec4(ray_t.origin - v3, ray_t.origin - v1), p_origin) > 0) return -4;
   if(dot(crossVec4(ray_t.origin - v1, ray_t.origin - v2), p_origin) > 0) return -5;

	return distance_to_plane;
}

vec4 crossVec4(vec4 _v1, vec4 _v2){
    vec3 vec1 = vec3(_v1[0], _v1[1], _v1[2]);
    vec3 vec2 = vec3(_v2[0], _v2[1], _v2[2]);
    vec3 res = cross(vec1, vec2);
    return vec4(res[0], res[1], res[2], 0);
}
