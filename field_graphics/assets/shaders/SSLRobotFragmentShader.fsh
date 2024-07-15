#version 410 core

in vec4 fragColor;
in vec3 relativeCoords;

uniform float radius = 8.5;
uniform float threashold = 5.5;

const float TAG_CENTER_RAD_DIST = 6.5;
const float TAG_RAD = 2.5;
const mat4 colors = mat4( //TODO isso precisa ser um uniform mas qualquer uniform adicional no shader simplesmente quebra absolutamente tudo
    1,0.3411,0.2,1, // Rosa Neon, sim eu sou muito esperto
    0,1,0,1,        // Verde
    0,0,1,1,        // Azul
    0,0,0,0
);

out vec4 color;

void main(){
    color = fragColor;
    if(length(relativeCoords.xy) > radius || relativeCoords.y > threashold){
        color.a = 0 ;
    }
    else if(length(relativeCoords.xy) <= TAG_RAD){
        color = colors[2];
    }
    else if(length(vec2(TAG_CENTER_RAD_DIST,TAG_CENTER_RAD_DIST)-relativeCoords.xy) <= TAG_RAD){
        color = colors[0];
    }

}