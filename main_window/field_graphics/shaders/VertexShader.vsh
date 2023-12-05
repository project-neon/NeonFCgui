#Version 410 core

layout(location = 0) in vec3 vertexPosition_modelspace;
layout(location = 1) in vec3 vertexColor;

uniform float angle;
uniform vec3 coord;

uniform float globalScale;
uniform float globalRotation;
uniform float aspectRatio = 1;
uniform vec3 globalTranslation;

out vec4 fragColor;

vec2 rotate(float angle, vec2 pos) {
        float sin = sin(angle);
        float cos = cos(angle);
        float cX = pos.x; float cY = pos.y;
        float nCX = ((cX * cos) - (cY * sin));
        float nCY = ((cX * sin) + (cY * cos));
        vec2 ret = vec2((nCX) + pos.x,(nCY) + pos.y);
        return ret;
}

void main(){
    vertexPosition_modelspace.xy = rotate(globalRotation+angle,vertexPosition_modelspace.xy) * globalScale;
    vertexPosition_modelspace += globalTranslation + coord;
    gl_Position.xyz = vertexPosition_modelspace.xyz;
    gl_Position.y *= aspectRatio;
    gl_Position.w = 1;
    fragColor = vec4(vertexColor.xyz,0);

}