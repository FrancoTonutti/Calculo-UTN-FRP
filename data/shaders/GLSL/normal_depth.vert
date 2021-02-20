#version 130

// Uniform inputs
uniform mat4 p3d_ModelViewProjectionMatrix;
uniform mat4 p3d_ModelViewMatrixInverseTranspose;

uniform mat4 p3d_ViewMatrixInverse;
uniform mat4 trans_model_to_world;

// Vertex inputs
in vec4 p3d_Vertex;
in vec2 p3d_MultiTexCoord0;
in vec3 p3d_Normal;
in mat4 p3d_ModelMatrix;

// Output to fragment shader
//out vec2 texcoord;
out vec4 l_position;
out vec4 l_color;


//out vec4 out_Color;

void main() {
  //gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
  //texcoord = p3d_MultiTexCoord0;



  vec4 position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
  vec3 color = vec3(p3d_ModelViewMatrixInverseTranspose * vec4(p3d_Normal, 0));

  //color.a = 0;


  l_color=vec4(color,0);
  l_color = normalize(l_color);
  l_color.a = 1;
  l_position=position;
  //l_color = vec4(p3d_Normal, 0);

  gl_Position = l_position;

  vec3 position2 = vec3(trans_model_to_world*p3d_Vertex);
  vec3 cam_pos = p3d_ViewMatrixInverse[3].xyz;

  vec3 radius = cam_pos-position2;


  float depth = 5/length(radius)+0.1;
  //l_color.a = depth;

  //out_Color = l_color;
}
