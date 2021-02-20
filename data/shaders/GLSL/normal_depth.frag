#version 400

//uniform sampler2D p3d_Texture0;
//in vec3 p3d_Normal;
in vec4 l_color;
uniform mat4 p3d_ViewMatrix;
uniform float showborders;
// Input from vertex shader
//in vec2 texcoord;

layout(location = 0, index = 0) out vec4 MyFragColor;
layout(location = 1, index = 0) out vec4 Tex1;
//out vec4 fragColor;

void main() {

  //vec4 color = texture(p3d_Texture0, texcoord);
  //MyFragColor = color.bgra;
  //MyFragColor = vec4(p3d_Normal, 1.0);
  //MyFragColor = vec4(1,0,0 , 1.0);
  vec4 l_color_norm = l_color;
  l_color_norm = l_color_norm/2;
  l_color_norm.rgb = l_color_norm.rgb + vec3(0.5, 0.5, 0.5);
  l_color_norm.a *= 2*showborders;
  MyFragColor = l_color_norm;


  //float depth = (p3d_ViewMatrix[0][2]);
  //MyFragColor = vec4(depth,0,0,1);


  /*
  vec4 l_color_norm = normalize(l_color);
  l_color_norm = l_color_norm/2;
  l_color_norm.rgb = l_color_norm.rgb +0.5;
  l_color_norm.a = 1;

  fragColor = texture(p3d_Texture0, texcoord);
  fragColor.r = 0;
  fragColor.a = 1;
  */
}