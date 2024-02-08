#version 410 core

layout(location = 0) in vec3 vertexPosition_modelspace;
layout(location = 1) in vec3 vertexColor;

uniform float angle = 0;
uniform float alpha = 1;
uniform vec3 coord;

uniform float globalScale = 1;
uniform float globalRotation;
uniform float aspectRatio = 1;
uniform vec3 globalTranslation;

out vec4 fragColor;
out vec3 relativeCoords;

vec2 rotate(float theta, vec2 point) {
        float sin = sin(-theta); float cos = cos(-theta);
        float nx = point.x * cos - point.y * sin;
        float ny = point.x * sin + point.y * cos;
        return vec2(nx,ny);
}

void main(){
    relativeCoords = vertexPosition_modelspace.xyz;
    relativeCoords.xy = rotate(angle,relativeCoords.xy);
    gl_Position.xyz = relativeCoords + coord.xyz;
    gl_Position.xyz += globalTranslation.xyz;
    gl_Position.xy = rotate(globalRotation,gl_Position.xy)* max(globalScale,0);
    gl_Position.y *= aspectRatio;
    gl_Position.w = 1;
    fragColor = vec4(vertexColor.rgb,alpha);

}