## Guia informal para parcialmente entender o que está acontecendo aqui:   


Isso aqui é um guia _temporário_ pra quem mais estiver trabalhando no desenvolvimento da interface puder mexer com a renderização do campo sem precisar entrar nas maluquices de renderização gráfica.

Para a renderização do campo, é empregada a API do OpenGL, que é contraintuitiva e, em geral, muito difícil de mexer. A função de todo esse módulo aqui é previnir que quem estiver trabalhando na interface tenha que fazer calls diretas pro OpenGL.

Assim, o módulo `field_graphics` têm como principal função abstrair toda a lógica de alocação de memória e comunicação com a GPU pra um formato mais usável. 
***
## Índice:
- [Objetos base:](https://github.com/project-neon/NeonSoccerGUI/blob/main/main_window/field_graphics/README.md#objetos-base)
  - [FieldView](https://github.com/project-neon/NeonSoccerGUI/blob/main/main_window/field_graphics/README.md#fieldview)
  - [RenderingContext](https://github.com/project-neon/NeonSoccerGUI/blob/main/main_window/field_graphics/README.md#renderingcontext)
  - [FieldGraphics](https://github.com/project-neon/NeonSoccerGUI/blob/main/main_window/field_graphics/README.md#renderable)
- [Criando um mesh renderizável](https://github.com/project-neon/NeonSoccerGUI/blob/main/main_window/field_graphics/README.md#criando-um-mesh-renderiz%C3%A1vel)
***
## Objetos base:

Esse framework implementa 3 principais classes de base: `field_view`, `Renderable` e `RenderingContext`.

### FieldView:
Um QWidget em que a cena é renderizada, quando inicializado ele automaticamente cria uma instância da classe `RenderingContext` com o nome `context`. Como a classe FieldView é uma sublasse de `QWidget`, então toda operação que se pode normalmente se fazer com um QWidget se pode fazer com uma instância dessa classe.

### RenderingContext:
Classe responsável por lidar com aspectos "globais" da renderização da cena, como a posição da câmera, essa classe têm um vetor de nome `objects`, que são objetos de tipo `Renderable`, estes representam os objetos que serão renderizados na cena.

`RenderingContext.set_transformations(self, x=0, y=0, z=0, scale=0, rotation=0)`:  
Seta as transformações *globais* do contexto, isso é, todos os objetos serão afetados por essas transformações.

`RenderingContext.draw(self,sim_time)`:  
Chama o método draw de cada objeto no contexto, renderizando a cena como um todo, note que este método não binda um framebuffer ao contexto local, logo o contexto de OpenGL precisa ser setado *ANTES* desse método ser chamado, coisa que o `field_view` já faz automaticamente. A variável sim_time é a variável que os shaders vão usar como referência de tempo.

### Renderable:
Representa um objeto renderizável na cena, isso pode ser qualquer coisa, um robô, um obstáculo, as faixas no campo etc. Cada objeto `Renderable` lida com sua própria lógica de renderização.  

`Renderable.draw(self, tx, ty, scale, rotation, aspect_ratio, sim_time)`:  
Renderiza o objeto no Framebuffer que está atualmente bindado à thread, para bindar o framebuffer de um determinado widget use a função `make_current` do widget.
As variáveis tx e ty representam o deslocamento da câmera, scale representa o zoom da câmera e rotation representa o ângulo da câmera, essas variáveis são traduções de escopo _global_ que são passadas pelo `RenderingContext` o qual esse objeto faz parte.  

`Renderable.set_transformations(self, x=0, y=0, z=0, scale=0, rotation=0)`:  
Seta as transformações *locais* do objeto, a localização do objeto na cena final também depende da posição da câmera.

Note que embora a cena seja isometricamte projetada num campo 2D ainda há uma variável z, que aplica uma transformação z em todos os vértices do objeto, isso vai ser explicado mais adiante.
***
## Criando um mesh renderizável:  

Um objeto renderizável na cena é representável por uma instância da classe `Renderable`, essa classe têm alguns componentes que afetam a sua renderização.  

É importante entender a lógica de renderização de objetos, o OpenGL é um framework 3d o qual estamos usando pra renderizar uma cena 2d, mas o terceiro componente ainda existe. O OpenGL sempre decide quais fragmentos vai desenhar com base nas coordenadas do fragmento, todo fragmento na cena _precisa_ estar contido num cubo com centro na origem, bordas em -1 e 1 respectivamente. A transformação de coordenadas no sistema usado pro sistema do OpenGL é feita no Vertex Shader com base nos parâmetros de tradução local e global que afetam o objeto, por exemplo uma escala de 0,1 vai fazer objetos que estão em x=2 aparecerem na tela.  

A maioria dos atributos são ou globais ou locais para cada forma, mas há um terceiro tipo de atributo que é diferente para cada _vértice_ do objeto, existem dois atributos desse tipo na classe Renderable, o primeiro é o que armazena as coordenadas relativas do vértice para formar o modelo, e o segundo é a cor do vértice. Esse segundo é mais contraintuitivo, mas como o OpenGL aceita atributos ou por forma ou por vértice, para termos mais de uma cor para o mesmo objeto esse é o único jeito.  
Outra coisa importante é que o OpenGL renderiza _triângulos_, ou seja, são 3 coordenadas por vértice e 3 vértices por triângulo, idealmente qualquer modelo deveria ter um tamanho de array de vértices como algum multiplo de 9.

Por exemplo, você pode definir um quadrado como 2 triângulos, logo uma array que representa um quadrado teria um tamanho de 18.

Como a cor de cada vértices são 3 floats, a array contendo todas as cores terá o mesmo tamanho da array contendo todos os vértices. (Note que as cores são especificadas num range de floats entre 0 e 1, não entre 0 e 255)

Tanto a array das coordenadas como a das cores são de tipo np.array pois o OpenGL não aceita vetores como variáveis, quando ela for inicializada é importante especificar o tipo como `np.float32`.

O OpenGL precisa de shaders, que são programas que instruem a placa de vídeo como renderizar o objeto, no momento eu já fiz 2 shaders que devem servir de base pra maioria das renderizações, só é necessário compilar eles.

Um exemplo de como criar um quadrado renderizável:

```python
import numpy as np
from main_window.field_graphics.rendering import render_manager
from main_window.field_graphics.rendering.render_manager import Renderable

# Note que esse código só pode rodar DEPOIS da inicialização do OpenGL
vertices = [-1,-1,0, 1,-1,0, -1,1,0, 1,1,0, -1,1,0, 1,-1,0] #6 Vértices -> 2 Triângulos
vertices = np.asarray(vertices,dtype=np.float32)
colors = [1,0,0 , 0,1,0 , 0,0,1, 1,1,0, 0,0,1, 0,1,0] #6 Vértices -> 6 cores
colors = np.asarray(colors,dtype=np.float32)

# Carrega os shaders:
vsh = open("main_window/field_graphics/shaders/VertexShader.vsh").read()
fsh = open("main_window/field_graphics/shaders/FragmentShader.fsh").read()
shader_program = render_manager.compileShaderProgram(vsh,fsh) # <- Compila os shaders

# Inicializa o modelo:
model = Renderable(vertices,colors,shader_program)

```

Colocando esse `model` em um contexto de renderização temos o seguinte resultado:

![Screenshot_1729](https://github.com/project-neon/NeonSoccerGUI/assets/59067466/9f127bdc-6547-46f5-8566-fa46f1a7c9cb)  
🌈?

Uma curiosidade do OpenGL é que, como nossos vértices têm cores diferentes pro mesmo triângulo, ele automaticamente interpola os valores do VertexShader pro FragmentShader, criando esse degradê.

Isso é só um exemplo, pra evitar código muito verbose você pode (e eu recomendo) colocar todas essas calls numa subclasse de Renderable, é exatamente isso que a classe `Robot` em `field_objects` faz.
