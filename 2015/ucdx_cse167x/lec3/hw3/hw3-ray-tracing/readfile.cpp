/*****************************************************************************/
/* This is the program skeleton for homework 2 in CSE167x by Ravi Ramamoorthi */
/* Extends HW 1 to deal with shading, more transforms and multiple objects   */
/*****************************************************************************/

/*****************************************************************************/
// This file is readfile.cpp.  It includes helper functions for matrix 
// transformations for a stack (matransform) and to rightmultiply the 
// top of a stack.  These functions are given to aid in setting up the 
// transformations properly, and to use glm functions in the right way.  
// Their use is optional in your program.  


// The functions readvals and readfile do basic parsing.  You can of course 
// rewrite the parser as you wish, but we think this basic form might be 
// useful to you.  It is a very simple parser.

// Please fill in parts that say YOUR CODE FOR HW 2 HERE. 
// Read the other parts to get a context of what is going on. 

/*****************************************************************************/

#include "readfile.h"


// You may not need to use the following two functions, but it is provided
// here for convenience

// The function below applies the appropriate transform to a 4-vector
void matransform(stack<mat4> &transfstack, double* values) 
{
  mat4 transform = transfstack.top(); 
  vec4 valvec = vec4(values[0],values[1],values[2],values[3]); 
  vec4 newval = transform * valvec; 
  for (int i = 0; i < 4; i++) values[i] = newval[i]; 
}

void rightmultiply(const mat4 & M, stack<mat4> &transfstack) 
{
  mat4 &T = transfstack.top(); 
  T = T * M; 
}

// Function to read the input data values
// Use is optional, but should be very helpful in parsing.  
bool readvals(stringstream &s, const int numvals, double* values) 
{
  for (int i = 0; i < numvals; i++) {
    s >> values[i]; 
    if (s.fail()) {
      cout << "Failed reading value " << i << " will skip\n"; 
      return false;
    }
  }
  return true; 
}

bool readstring(stringstream &s, string &str) 
{
    s >> str; 
    if (s.fail()) {
      cout << "Failed reading string, will skip\n"; 
      return false;
    }
  return true; 
}

void readfile(char* filename) 
{
  string str, cmd; 
  ifstream in;
  in.open(filename); 
  if (in.is_open()) {

    // I need to implement a matrix stack to store transforms.  
    // This is done using standard STL Templates 
    stack <mat4> transfstack; 
    transfstack.push(mat4(1.0));  // identity

    getline (in, str); 
    while (in) {
      if ((str.find_first_not_of(" \t\r\n") != string::npos) && (str[0] != '#')) {
        // Ruled out comment and blank lines 

        stringstream s(str);
        s >> cmd; 
        int i; 
        double values[10]; // Position and color for light, colors for others
        // Up to 10 params for cameras.  
        bool validinput; // Validity of input 

        // GENERAL

        if (cmd == "size") {
          validinput = readvals(s,2,values); 
          if (validinput) { 
            width = (int) values[0]; height = (int) values[1];
          }
        } 

        else if (cmd == "maxdepth") {
          validinput = readvals(s,1,values); 
          if (validinput) { 
            maxdepth = (int) values[0];
          } 
        } 

        else if (cmd == "output") {
          string str;
          validinput = readstring(s,str); 
          if (validinput) { 
            output_filename = (string) str;
          } 
        } 

        // CAMERA
        else if (cmd == "camera") {
          validinput = readvals(s,10,values); // 10 values eye cen up fov
          if (validinput) {
            camera.setDetails(vec4(values[0],values[1],values[2],1), 
                              vec4(values[3],values[4],values[5],1), 
                              vec4(values[6],values[7],values[8],1), 
                              values[9]);
          }
        }

        // GEOMETRY

        else if (cmd == "maxverts") {
          validinput = readvals(s,1,values); 
          if (validinput) { 
            maxverts = (int) values[0];
          } 
        } 
        else if (cmd == "maxvertnorms") {
          validinput = readvals(s,1,values); 
          if (validinput) { 
            maxvertnorms = (int) values[0];
          } 
        } 

        else if (cmd == "vertex") {
          validinput = readvals(s,3,values); 
          if (validinput) { 
            vertex_positions.push_back(vec4(values[0], values[1], values[2],1));
          } 
        } 

        else if (cmd == "vertexnormal") {
          validinput = readvals(s,6,values); 
          if (validinput) { 
            vertexnormal_positions.push_back(vec4(values[0], values[1], values[2],1));
            vertexnormal_npositions.push_back(vec4(values[3], values[4], values[5],1));
          } 
        } 

        else if (cmd == "sphere" || cmd == "tri" || cmd == "trinormal") {
            static int triangles = 0;
            static int spheres = 0;
            // Set the object's type and attributes
            if (cmd == "sphere") {
              validinput = readvals(s, 4, values); 
              if (validinput) {
                Sphere *obj = new Sphere(vec4(values[0], values[1], values[2],1), values[3]);
                obj->setAmbientColor(Color(  ambient_backup[0],
                                      ambient_backup[1],
                                      ambient_backup[2]));
                obj->setDiffuseColor(Color(  diffuse_backup[0],
                                      diffuse_backup[1],
                                      diffuse_backup[2]));
                obj->setSpecularColor(Color( specular_backup[0],
                                      specular_backup[1],
                                      specular_backup[2]));
                obj->setEmissionColor(Color( emission_backup[0],
                                      emission_backup[1],
                                      emission_backup[2]));
                obj->setShininess(shininess_backup);

                scene.addObjects(dynamic_cast<Object*>(obj));

                // Set the object's transform
                obj->performTransformation (transfstack.top());               
                string str = "spheres"+ std::to_string (spheres);
                obj->test_name = str;           
                spheres++;                
              }
            } //sphere

            else if (cmd == "tri") {
              validinput = readvals(s, 3, values); 
              if (validinput) {
                Triangle *obj = new Triangle( vertex_positions[values[0]],
                                              vertex_positions[values[1]],
                                              vertex_positions[values[2]], standard);
                obj->setAmbientColor(Color(  ambient_backup[0],
                                      ambient_backup[1],
                                      ambient_backup[2]));
                obj->setDiffuseColor(Color(  diffuse_backup[0],
                                      diffuse_backup[1],
                                      diffuse_backup[2]));
                obj->setSpecularColor(Color( specular_backup[0],
                                      specular_backup[1],
                                      specular_backup[2]));
                obj->setEmissionColor(Color( emission_backup[0],
                                      emission_backup[1],
                                      emission_backup[2]));
                obj->setShininess(shininess_backup);                
                scene.addObjects(dynamic_cast<Object*>(obj));

                // Set the object's transform
                obj->performTransformation (transfstack.top());

                string str = "trianlge"+ std::to_string (triangles);
                obj->test_name = str;
                triangles++;
              }
            } //tri

            else if (cmd == "trinormal") {
              validinput = readvals(s, 6, values); 
              if (validinput) {
                Triangle *obj = new Triangle( vertexnormal_positions[values[0]],
                                              vertexnormal_positions[values[1]],
                                              vertexnormal_positions[values[2]], trinormal);
                obj->setVns(vertexnormal_npositions[values[3]],
                            vertexnormal_npositions[values[4]],
                            vertexnormal_npositions[values[5]]);
                obj->setAmbientColor(Color(  ambient_backup[0],
                                      ambient_backup[1],
                                      ambient_backup[2]));
                obj->setDiffuseColor(Color(  diffuse_backup[0],
                                      diffuse_backup[1],
                                      diffuse_backup[2]));
                obj->setSpecularColor(Color( specular_backup[0],
                                      specular_backup[1],
                                      specular_backup[2]));
                obj->setEmissionColor(Color( emission_backup[0],
                                      emission_backup[1],
                                      emission_backup[2]));
                obj->setShininess(shininess_backup);                
                scene.addObjects(dynamic_cast<Object*>(obj));

                // Set the object's transform
                obj->performTransformation (transfstack.top()); 

              }
            }
        } //trinormal

        // Transformations

        else if (cmd == "translate") {
          validinput = readvals(s,3,values); 
          if (validinput) {
            // Think about how the transformation stack is affected
            // You might want to use helper functions on top of file. 
            // Also keep in mind what order your matrix is!
            rightmultiply(
              Transform::translate(values[0],values[1],values[2]),
              transfstack);
          }
        }
        else if (cmd == "scale") {
          validinput = readvals(s,3,values); 
          if (validinput) {
            // Think about how the transformation stack is affected
            // You might want to use helper functions on top of file.  
            // Also keep in mind what order your matrix is!
            rightmultiply(
              Transform::scale(values[0],values[1],values[2]),
              transfstack);
          }
        }
        else if (cmd == "rotate") {
          validinput = readvals(s,4,values); 
          if (validinput) {
            // values[0..2] are the axis, values[3] is the angle.  
            // You may want to normalize the axis (or in Transform::rotate)
            // See how the stack is affected, as above.  
            // Note that rotate returns a mat3. 
            // Also keep in mind what order your matrix is!
            vec3 axis = glm::normalize(vec3(values[0],values[1],values[2]));
            mat4 R = mat4(Transform::rotate(values[3], axis));
            R[3][3] = 1.0;
            rightmultiply(R, transfstack);
          }
        }

        // I include the basic push/pop code for matrix stacks
        else if (cmd == "pushTransform") {
          transfstack.push(transfstack.top()); 
        } else if (cmd == "popTransform") {
          if (transfstack.size() <= 1) {
            cerr << "Stack has no elements.  Cannot Pop\n"; 
          } else {
            transfstack.pop(); 
          }
        }

        // Process the light,.insert it to database.
        // Lighting Command
        else if (cmd == "directional") {
            validinput = readvals(s, 6, values); // Position/color for lts.
            if (validinput) {
              Light* light = new Light( vec4(values[0],values[1],values[2],1), 
                                        Color(values[3],values[4],values[5]), directional);
              scene.addLights(light);
            }
        }
        else if (cmd == "point") {
            validinput = readvals(s, 6, values); // Position/color for lts.
            if (validinput) {
              Light* light = new Light( vec4(values[0],values[1],values[2],1), 
                                        Color(values[3],values[4],values[5]), point);
              scene.addLights(light);
            }
        }        

        else if (cmd == "attenuation") {
            validinput = readvals(s, 3, values); // Position/color for lts.
            if (validinput) {
              scene.setAttenuationConstants(values[0],values[1],values[2]);          
            }
        }   

        // Material Commands 
        // Ambient, diffuse, specular, shininess properties for each object.
        // Filling this in is pretty straightforward, so I've left it in 
        // the skeleton, also as a hint of how to do the more complex ones.
        // Note that no transforms/stacks are applied to the colors. 

        else if (cmd == "ambient") {
          validinput = readvals(s, 3, values); // colors 
          if (validinput) {
            for (i = 0; i < 3; i++) {
              ambient_backup[i] = values[i]; 
            }           
          }
        }

        else if (cmd == "diffuse") {
          validinput = readvals(s, 3, values); 
          if (validinput) {
            for (i = 0; i < 3; i++) {
              diffuse_backup[i] = values[i]; 
            }            
          }
        } 
        else if (cmd == "specular") {
          validinput = readvals(s, 3, values); 
          if (validinput) {
            for (i = 0; i < 3; i++) {
              specular_backup[i] = values[i]; 
            }            
          }
        } 
        else if (cmd == "emission") {
          validinput = readvals(s, 3, values); 
          if (validinput) {
            for (i = 0; i < 3; i++) {
              emission_backup[i] = values[i]; 
            }            
          }
        } 
        else if (cmd == "shininess") {
          validinput = readvals(s, 1, values);
          shininess_backup = values[0];          
        }

        else {
          cerr << "Unknown Command: " << cmd << " Skipping \n"; 
        }
      }
      getline (in, str); 
    }  // while

  } else {
    cerr << "Unable to Open Input Data File " << filename << "\n"; 
    throw 2; 
  }
}
