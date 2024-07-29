## Guia informal para parcialmente entender o que está acontecendo aqui:   


Isso aqui é um guia _temporário_ pra quem mais estiver trabalhando no desenvolvimento da interface puder mexer com a renderização do campo sem precisar entrar nas maluquices de renderização gráfica.

Para a renderização do campo, é empregada a API do OpenGL, que é contraintuitiva e, em geral, muito difícil de mexer. A função de todo esse módulo aqui é previnir que quem estiver trabalhando na interface tenha que fazer calls diretas pro OpenGL.

Assim, o módulo `field_graphics` têm como principal função abstrair toda a lógica de alocação de memória e comunicação com a GPU pra um formato mais usável. 
***
## Índice:
- [Objetos base:](https://github.com/project-neon/NeonSoccerGUI/blob/main/field_graphics/README.md#objetos-base)
  - [FieldView](https://github.com/project-neon/NeonSoccerGUI/blob/main/field_graphics/README.md#fieldview)
  - [RenderingContext](https://github.com/project-neon/NeonSoccerGUI/blob/main/field_graphics/README.md#renderingcontext)
  - [Renderable](https://github.com/project-neon/NeonSoccerGUI/blob/main/field_graphics/README.md#renderable)
- [Tecnicalidades do OpenGL](https://github.com/project-neon/NeonSoccerGUI/tree/main/field_graphics#tecnicalidades-do-opengl)
- [Criando um mesh renderizável](https://github.com/project-neon/NeonSoccerGUI/blob/main/field_graphics/README.md#criando-um-mesh-renderiz%C3%A1vel)
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
Um modelo no OpenGL é, por natureza, um conjunto de triângulos, cada triângulo com 3 vértices e cada vértice com 3 coordenadas (x,y,z), assim o inicializador do objeto considera cada 9 floats como um triângulo.  
Os 3 argumentos necessários para inicializar um Renderable são `vertices` que são as coordenadas já mencionadas, `colors` que são as cores de cada _vértice_, isso pode ser meio confuso, mas cada vértice em cada triângulo têm sua própria cor, assim cada triângulo têm 3 variáveis de cor, para que um triângulo seja monocromático é necessário dar a mesma cor para seus 3 vértices, eu sei que isso parece não fazer nenhum sentido mas existe um motivo por eu ter feito o shader aceitar as coisas desse jeito e isso vai ser discutido mais adiante, como são 3 variáveis por cor e 3 cores por triângulo, a array `colors` deve ter o mesmo tamanho que a array `vertices`.
O ultimo argumento é o `shader_program`, que são os shaders compilados que o objeto vai usar, existem shaders pré feitos que é só puxar pra usar, isso também será discutido adiante.
Uma nota é importante é que, sabe lá deus o motivo, o PyOpenGL não aceita arrays padrão do python, assim é necessário converter para uma array do numpy com dtype setado para o binder aceitar.
Para fazer um triângulo verde:
```python
vertices = [-1,0,0 , 1,0,0 , 0,1,0]
colors = [0,1,0 , 0,1,0 , 0,1,0]
vertices = np.asarray(vertices, dtype=np.float32)
colors = np.asarray(colors, dtype=np.float32)
model = Renderable(vertices, colors, pre_compiled_shader_program)
```

`Renderable.draw(self, tx, ty, scale, rotation, aspect_ratio, sim_time)`:  
Renderiza o objeto no Framebuffer que está atualmente bindado à thread, para bindar o framebuffer de um determinado widget use a função `make_current` do widget.
As variáveis tx e ty representam o deslocamento da câmera, scale representa o zoom da câmera e rotation representa o ângulo da câmera, essas variáveis são traduções de escopo _global_ que são passadas pelo `RenderingContext` o qual esse objeto faz parte. Variáveis de rotação e tradução local são comunicadas ao shader pelos seus respectivos objetos.

`Renderable.set_transformations(self, x=0, y=0, z=0, scale=0, rotation=0)`:  
Seta as transformações *locais* do objeto, a localização do objeto na cena final também depende da posição da câmera.

Note que embora a cena seja isometricamte projetada num campo 2D ainda há uma variável z, que aplica uma transformação z em todos os vértices do objeto, isso vai ser explicado mais adiante.
***
## Tecnicalidades do OpenGL:  
### Shaders e shader programs:
Shaders são programas que rodam na GPU do computador com instruções de como renderizar a cena, eles são escritos em GLSL que é uma língua de programação com sintaxe similar ao C.  
Existem muitos tipos de shaders, mas nós só precisamos de dois para renderizar uma cena, o Vertex Shader e o Fragment Shader.  
**Vertex Shader**  
Sua função mais importante é definir onde o vértice está na cena com base na informação que recebe (traduções, rotação, zoom da câmera etc.), como o nome sugere, esse shader roda uma vez para cada vértice do objeto sendo renderizado.  

**Fragment Shader**  
O Fragment Shader roda depois do Vertex Shader na pipeline, então o Vertex Shader pode passar algumas informações para o Fragment Shader, a principal função do fragment shader é definir a cor, transparência e profundidade do fragmento (píxel). O Fragment Shader roda uma vez por píxel visível do objeto sendo renderizado.  
Como os robôs precisam ter cores diferentes no mesmo objeto por conta de suas tags, o Vertex Shader passa a cor individual de cada vértice pro Fragment Shader, que usa essa variável pra definir a sua cor final.  

Uma tecnicalidade importante é que cada triângulo tem 3 vértices mas normalmente ele vai ter muito mais fragmentos pra serem renderizados, um cubo com 6 vértices terá potencialmente centenas de fragmentos, assim, quando passamos uma variável do Vertex Shader para o Fragment Shader, essas variáveis passam por um processo de interpolação, assim o valor final para cada fragmento depende de sua proximidade com cada vértice. Vamos supor por exemplo que eu esteja renderizando um triângulo que passa uma variável de tipo `float` para o Fragment Shader, e que cada vértice passasse uma float diferente (1,2 e 3) respectivamente. A float que cada fragmento receberia seria um resultado interpolado dependendo da sua proximidade com cada vértice:

![Interpolação](https://github.com/project-neon/NeonSoccerGUI/assets/59067466/69b69c93-4505-4266-9d3b-bbe82a1a82f8)

### A componente Z:  
O OpenGL é uma biblioteca de renderização 3D que estamos usando pra fazer uma renderização 2D, mas isso não significa que a componente z não é importante, no nosso caso, podemos nos aproveitar do buffer de profundidade do OpenGL para usar a componente Z como um filtro de prioridade, isso é, a coordenada Z define quais objetos são renderizados por cima e quais são renderizados por baixo.
O OpenGL renderiza fragmentos que têm suas coordenadas contidas em um cubo com limites em `[-1,-1,-1]` e `[1,1,1]`, tudo fora desse range é descartado, assim, a coordenada da componente Z de cada vértice deve estar entre -1 e 1. Algo importante de notar é que no OpenGL, o Z positivo tende a levar o objeto **pra frente**, ou seja, um vértice em `.-5` será renderizado por cima de um vértice em `.5`, como cada vértice têm sua coordenada Z podemos fazer com que certas partes de um modelo sejam renderizadas por cima de outras partes, isso é importante no caso do robô, que precisa ter suas tags renderizadas por cima do quadrado que compõe seu corpo principal.

***
## Fazendo um modelo .json
### Como converter
Modelos .json são convertidos para objetos `Renderable` com a função `modelFromJSON` em `render_manager`. Essa função só têm um argumento, que é a string do .json a ser interpretado.   
Importante mencionar que essa função retorna um _array_ de modelos, ou seja, cada .json pode ter mais de um objeto Renderable representado.   

### Hierarquia do modelo json
O arquivo .json deve ser estruturado da seguinte forma:
```json
{
  "objects": [
    {
      "shader": {
        "vertex": "vertex_shader_path",
        "fragment": "fragment_shader_path",
        "uniforms": []
      },
      "vertices": [
        {"x": -0.5,"y": 0,"z": 0,"r": 1,"g": 0,"b": 0},
        {"x": 0,"y": 1,"z": 0,"r": 0,"g": 1,"b": 0},
        {"x": 0.5,"y": 0,"z": 0,"r": 0,"g": 0,"b": 1}
      ]
    }
  ]
}
```
Basicamente, dentro do objeto json principal há uma array `objects`, cada elemento dessa array vai representar um `Renderable`, dentro de cada elemento dessa array têm 2 elementos:   
- `shader`: Representa dados sobe o shader que o objeto vai usar, `vertex` e `fragment` são as paths dentro do repositório do vertex e fragment shader do objeto, enquanto `uniforms` representa os uniforms que devem ser setados assim que o shader for carregado, essa parte será explicada no final do módulo.   
- `vertices`: Representa os vértices do objeto, cada vértice tem 6 componentes, `x`,`y`,`z` são suas coordenadas e `r`,`g`,`b` suas cores respectivas. Podem ser colocados quantos vértices forem necessários no modelo, só é necessário lembrar que cada sequência de 3 vértices será considerada 1 triângulo.

### Setando uniforms
Para pré setar um uniform de um shader é necessário se saber as seguintes informações:
- O nome do uniform no shader
- O tipo de uniform (atualmente o interpretador só aceita tipos `int`,`float`,`vec2`,`vec3`,`vec4`. Espero eu que ninguém precise mandar matrízes pro shader).  
Os valores que você quer setar para o Uniform.
Cada um desses elementos são representados com os respectivos valores em cada elemento do array: `type`, `name`, `v0, v1, v2, v3`. O valor type é uma string contendo um dos valores acima, será sempre o mesmo tipo que está no shader, o valor `name` é uma string que é o nome da variável dentro do shader. Os valores `v0, v1, ...` são os valores que o uniform será setado, você pode não precisar usar todos dependendo do tipo de variável que está sendo definida, por exemplo se você está dando um valor para uma `float`, então só é necessário definir o `v0`, agora se você está usando um `vec3`, serão necessários definir o `v0`,`v1` e `v2`.   
Importante notar que os vetores aceitam floats como argumentos.

Atualmente só existe um exemplo notável desse sistema, que é o modelo `ball.json`, onde há um uniform definido o raio do círculo:
```json
"uniforms": [
          {
            "type": "float",
            "name": "radius",
            "v0": 0.5
          }
        ]
```
A variável têm nome radius pois, no shader em que ela está sendo usada (`CircleFragmentShader`), esse é o nome do uniform. 
```GLSL
#version 410 core

in vec4 fragColor;
in vec3 relativeCoords;

uniform float radius = 1; // <- Variável que representa o raio da circunferência

out vec4 color;

void main(){
    color = fragColor;
    if(length(relativeCoords) > radius){
        color.a = 0;
        // Compara o valor radius com o vetor que representa a distância do fragmento da origem do objeto
        // se esse valor for maior que o raio, o alpha do fragmento é setado para 0, fazendo com que um
        // círculo praticamente perfeito seja renderizado
    }
}
```

***
## Criando um mesh renderizável:  

Um objeto renderizável na cena é representável por uma instância da classe `Renderable`, essa classe têm alguns componentes que afetam a sua renderização.  

É importante entender a lógica de renderização de objetos, o OpenGL é um framework 3d o qual estamos usando pra renderizar uma cena 2d, mas o terceiro componente ainda existe. O OpenGL sempre decide quais fragmentos vai desenhar com base nas coordenadas do fragmento, todo fragmento na cena _precisa_ estar contido num cubo com centro na origem, bordas em -1 e 1 respectivamente. A transformação de coordenadas no sistema usado pro sistema do OpenGL é feita no Vertex Shader com base nos parâmetros de tradução local e global que afetam o objeto, por exemplo uma escala de 0,1 vai fazer objetos que estão em x=2 aparecerem na tela.  

A maioria dos atributos são ou globais ou locais para cada forma, mas há um terceiro tipo de atributo que é diferente para cada _vértice_ do objeto, existem dois atributos desse tipo na classe Renderable, o primeiro é o que armazena as coordenadas relativas do vértice para formar o modelo, e o segundo é a cor do vértice. Esse segundo é mais contraintuitivo, mas como o OpenGL aceita atributos ou por forma ou por vértice, para um objeto ter mais de uma cor esse é o único jeito.  
Outra coisa importante é que o OpenGL renderiza _triângulos_, ou seja, são 3 coordenadas por vértice e 3 vértices por triângulo, idealmente qualquer modelo deveria ter um tamanho de array de vértices como algum multiplo de 9.

Por exemplo, você pode definir um quadrado como 2 triângulos, logo uma array que representa um quadrado teria um tamanho de 18.


![Vertices](https://github.com/project-neon/NeonSoccerGUI/assets/59067466/f56e0424-2b76-49d4-b8e3-ac4d4db5c073)


Como a cor de cada vértices são 3 floats, a array contendo todas as cores terá o mesmo tamanho da array contendo todos os vértices. (Note que as cores são especificadas num range de floats entre 0 e 1, não entre 0 e 255)

Tanto a array das coordenadas como a das cores são de tipo np.array pois o OpenGL não aceita vetores como variáveis, quando ela for inicializada é importante especificar o tipo como `np.float32`.

O OpenGL precisa de shaders, que são programas que instruem a placa de vídeo como renderizar o objeto, no momento eu já fiz 2 shaders que devem servir de base pra maioria das renderizações, só é necessário compilar eles.

Um exemplo de como criar um quadrado renderizável:

```python
import numpy as np
from field_graphics.rendering import render_manager
from field_graphics.rendering import RenderableMesh

# Note que esse código só pode rodar DEPOIS da inicialização do OpenGL
vertices = [-1, -1, 0, 1, -1, 0, -1, 1, 0, 1, 1, 0, -1, 1, 0, 1, -1, 0]  # 6 Vértices -> 2 Triângulos
vertices = np.asarray(vertices, dtype=np.float32)
colors = [1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0]  # 6 Vértices -> 6 cores
colors = np.asarray(colors, dtype=np.float32)

# Carrega os shaders:
vsh = open("field_graphics/shaders/VertexShader.vsh").read()
fsh = open("field_graphics/shaders/FragmentShader.fsh").read()
shader_program = render_manager.compileShaderProgram(vsh, fsh)  # <- Compila os shaders

# Inicializa o modelo:
model = RenderableMesh(vertices, colors, shader_program)

```

Colocando esse `model` em um contexto de renderização temos o seguinte resultado:

![Screenshot_1729](https://github.com/project-neon/NeonSoccerGUI/assets/59067466/9f127bdc-6547-46f5-8566-fa46f1a7c9cb)  
🌈?

Uma curiosidade do OpenGL é que, como nossos vértices têm cores diferentes pro mesmo triângulo, ele automaticamente interpola os valores do VertexShader pro FragmentShader, criando esse degradê.

Isso é só um exemplo, pra evitar código muito verbose você pode (e eu recomendo) colocar todas essas calls numa subclasse de Renderable, é exatamente isso que a classe `Robot` em `field_objects` faz.
