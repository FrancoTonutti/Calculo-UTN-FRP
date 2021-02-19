#version 400

uniform sampler2D p3d_Texture0;
uniform vec2 resolution;

//in vec3 p3d_Normal;
in vec4 l_color;
uniform mat4 p3d_ViewMatrix;
// Input from vertex shader
in vec2 texcoord;

// Const
const ivec2 next_x = ivec2(1, 0);
const ivec2 next_y = ivec2(0, 1);
const vec4 zero = vec4(0.5,0.5,0.5, 0.5);


layout(location = 0, index = 0) out vec4 MyFragColor;

void main() {
  vec2 uv = gl_FragCoord.xy / resolution;
  uv.y = 1-uv.y;
  vec4 colores = texture2D(p3d_Texture0, uv.xy);

  ivec2 coord0 = ivec2(gl_FragCoord);
  //coord0.y = int(resolution.y) - coord0.y;

  ivec2 coord1 = coord0 + next_x;
  ivec2 coord2 = coord0 - next_x;
  ivec2 coord3 = coord0 + next_y;
  ivec2 coord4 = coord0 - next_y;

  vec4 color0 = (texelFetch(p3d_Texture0, coord0, 0));
  vec4 color1 = (texelFetch(p3d_Texture0, coord1, 0));
  vec4 color2 = (texelFetch(p3d_Texture0, coord2, 0));
  vec4 color3 = (texelFetch(p3d_Texture0, coord3, 0));
  vec4 color4 = (texelFetch(p3d_Texture0, coord4, 0));

  vec3 normal0 = vec3(color0-zero)*2;
  vec3 normal1 = vec3(color1-zero)*2;
  vec3 normal2 = vec3(color2-zero)*2;
  vec3 normal3 = vec3(color3-zero)*2;
  vec3 normal4 = vec3(color4-zero)*2;

  float cos_1 = dot(normal0, normal1);
  float cos_2 = dot(normal0, normal2);
  float cos_3 = dot(normal0, normal3);
  float cos_4 = dot(normal0, normal4);

  vec3 camera_vec = vec3(0,0,-1);
  float cos_camera0 = dot(camera_vec, normal0)/2+0.5;
  float cos_camera1 = dot(camera_vec, normal1)/2+0.5;
  float cos_camera2 = dot(camera_vec, normal2)/2+0.5;
  float cos_camera3 = dot(camera_vec, normal3)/2+0.5;
  float cos_camera4 = dot(camera_vec, normal4)/2+0.5;

  float test = (color0.a -0.5)*2;

  float fix_cos_1 =1- max(sign(cos_camera0 - cos_camera1), 0.0);
  float fix_cos_2 =1- max(sign(cos_camera0 - cos_camera2), 0.0);
  float fix_cos_3 =1- max(sign(cos_camera0 - cos_camera3), 0.0);
  float fix_cos_4 =1- max(sign(cos_camera0 - cos_camera4), 0.0);

  if (cos_camera1<cos_camera0) cos_1=1;
  if (cos_camera2<cos_camera0) cos_2=1;
  if (cos_camera3<cos_camera0) cos_3=1;
  if (cos_camera4<cos_camera0) cos_4=1;

  if (color0.a>color1.a+0.01) cos_1=0;
  if (color0.a>color2.a+0.01) cos_2=0;
  if (color0.a>color3.a+0.01) cos_3=0;
  if (color0.a>color4.a+0.01) cos_4=0;

  float mx = min(cos_1,min(cos_2,min(cos_3,cos_4)));
  float draw = 1 - max(sign(mx - 0.90), 0.0);
  if (test < 0.1) draw = 0;

  vec4 colorb=vec4(0,0,0,1);
  //vec4 colorb=tex2D(tex_1, l_texcoord0);


  MyFragColor = colorb*draw;
  //MyFragColor = color0;
}