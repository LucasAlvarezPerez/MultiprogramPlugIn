# Extension de programación Multi-Agentes
Este proyecto está pensado para programar y facilitar el uso de multiagentes para la programación en CLI (terminal) en herramientas como Antigravity CLI o ClaudeCode CLI. 

## Beneficios de la programación multi-agente
Hoy en día, la programación con IA no es ningun misterio que se "come el mercado". Sin emabrgo, el factor humano es lo que hace que nuestro producto pase un "control de calidad" y cumpla unos estándares que la IA a veces parece pasar por alto u olvidar si no se los recordamos. 

La programación multi-agentes debe servir como herramienta para facilitar el trabajo al programador en tareas que antes eran tediosas, repetitivas e interminables como es **debuggear**, **picar código** o **encontrar errores**. 

## Tecnologías Empleadas
Para este proyecto se utiliza principalmente una estructura de archivos Python para lanzar los agentes y declarar todas sus necesidades, archivos .yaml para definir todos los agentes del proyecto,  junto con archivos de texto plano o markdown para definir todas las necesidades, y cuestiones relevantes de la documentación del proyecto. 

  - **Lenguajes**: Python, YAML, Markdown

## Estrucutra del proyecto
Este proyecto es altamente desacoplado, por lo tanto se emplean varios archvos con funcionalidades únicas y muy bien definidas. 

En la carpeta ``src``: 
    - ``agent.py``: Define la clase genérica que debe cumplir todo agente que implementemos. Al instanciarse una clase Agente, se lee uno de los .yaml en \config\agents\ y determina todas las habilidades, alcance y herramientas tiene. 
    - ``harness.py``: Determina si la ruta a la que intenta acceder un agente es válida. Principlamente revisa si está dentro del proyecto que estamos editando. 
    - ``main.py``: Punto de entrada desde el que se lanza el proceso agéntico, leerá las variables de entorno .env y la tarea que debe realizar. Instancia los objetos agente, gestiona el paso de mensajes entre agentes y controla el bucle de corrección y tests 
    - ``tools.py``: Contiene acciones atómicas que interactúan con el sistema operativo: leer, escribir, ejecución y operaciones con Git/GitHub.
En la carpeta ```docs``:
    - ``DECISIONES.md``: Define todas las decisiones relevantes y determinantes en la ejecución del proyecto para guiar al usuario sobre el enfoque de la aplicación
    - ``USO.md`` : Guía detallada de uso de la aplicación. En ella se incluyen datos como la Integración al proyecto, la configuración y su empleo. 

## Uso del proyecto
Para correr el proyecto con todas sus funcionalidades predeterminadas sin configurar nada, los pasos quie debemos seguir son los siguientes. 

  1) Configurar el .env con las variables necesarias para definir las claves API que empleamos 
  2) Definir la tarea que debe realizar el agente
  3) Ejecutar el ``main.py`` y esperar el resultado. 