#version 410 core

in vec4 fragColor;
in vec3 relativeCoords;

uniform float radius = 1;
uniform float threashold = 1;

out vec4 color;

void main(){
    color = fragColor;
    if(length(relativeCoords.xy) > radius || relativeCoords.y > threashold){
        color.a = 0;
    }
}