#version 410 core

in vec4 fragColor;
in vec3 relativeCoords;

uniform float radius = 1;

out vec4 color;

void main(){
    color = fragColor;
    if(length(relativeCoords) > radius){
        color.a = 0.0F;
    }
}