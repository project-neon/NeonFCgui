#version 410 core

in vec2 textureCoords;

uniform sampler2D text;

out vec4 color;

void main(){
    color = texture(text,textureCoords.xy);

}