#version 410 core

in vec4 fragColor;
in vec2 textureCoords;

uniform sampler2D txt;

out vec4 color;

void main(){
    color = texture(txt,textureCoords);
    color.rgb = fragColor.rgb;
    color.a *= fragColor.a;
    color = clamp(color,0,1);
}