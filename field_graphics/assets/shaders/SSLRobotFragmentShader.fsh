#version 410 core

in vec4 fragColor;
in vec3 relativeCoords;

uniform float radius = 8.5;
uniform float threashold = 5.5;
uniform int id = 0;
uniform int team = 0;

//FIXME pq eu não consigo adicionar uniforms funcionais ao shader?

const vec4 pink = vec4(1,0.0627,0.9411,1); // Rosa Neon, sim eu sou muito esperto
const vec4 green = vec4(0,1,0,1);
const vec4 blue = vec4(0,0,1,1);
const vec4 yellow = vec4(1,1,0,1);

struct Tag {
    vec4 topLeft;
    vec4 topRight;
    vec4 bottomLeft;
    vec4 bottomRight;
};

const Tag[16] tagDict = Tag[16]( //FIXME isso não deveria existir, PQ EU NÃO CONSIGO PASSAR UNIFORMS PRA CA????
    Tag(pink,pink,green,pink), // 0
    Tag(green,pink,green,pink), // 1
    Tag(green,green,green,pink), // 2
    Tag(pink,green,green,pink), // 3
    Tag(pink,pink,pink,green), // 4
    Tag(green,pink,pink,green), // 5
    Tag(green,green,pink,green), // 6 
    Tag(pink,green,pink,green), // 7
    Tag(green,green,green,green), // 8
    Tag(pink,pink,pink,pink), // 9
    Tag(pink,pink,green,green), // 10
    Tag(green,green,pink,pink), // 11
    Tag(green,pink,green,green),// 12
    Tag(green,pink,pink,pink), // 13
    Tag(pink,green,green,green), // 14
    Tag(pink,green,pink,pink) // 15
);

out vec4 color;

void main(){
    color = fragColor;
    if(length(relativeCoords.xy) > radius || relativeCoords.y > threashold){
        color.a = 0;
    }
    else if(length(relativeCoords.xy) <= 2.5){
        color = team == 0 ? blue : yellow;
    }
    else if(length(vec2(-5.4772,3.5)-relativeCoords.xy) <= 2.0){
        color = tagDict[id].topLeft;
    }
    else if(length(vec2(5.4772,3.5)-relativeCoords.xy) <= 2.0){
        color = tagDict[id].topRight;
    }
    else if(length(vec2(-3.5,-5.4772)-relativeCoords.xy) <= 2.0){
        color = tagDict[id].bottomLeft;
    }
    else if(length(vec2(3.5,-5.4772)-relativeCoords.xy) <= 2.0){
        color = tagDict[id].bottomRight;
    }


}