# 🤖 Extensión de Programación Multi-Agente

> Motor multiagente modular pensado para facilitar el desarrollo asistido por IA desde terminal (CLI), compatible con flujos de trabajo en herramientas como **Antigravity CLI** o **Claude Code CLI**.

---

## ✨ Beneficios de la programación multiagente

Hoy en día, la programación con IA está transformando el desarrollo de software. Sin embargo, el **factor humano** sigue siendo indispensable para garantizar que el producto supere el control de calidad y cumpla estándares que la IA puede pasar por alto si no se le recuerdan explícitamente.

El enfoque multiagente sirve como herramienta de apoyo para agilizar tareas tediosas o repetitivas como:
- 🐛 **Debuggear** incidencias complejas.
- 💻 **Generar y refactorizar código** de forma estructurada.
- 🔍 **Detectar errores** antes de integrar cambios.

---

## 🛠️ Tecnologías empleadas

El proyecto combina scripts en Python para la ejecución y orquestación, archivos YAML para la configuración declarativa de cada agente y documentos en Markdown para la definición de tareas y documentación.

- **Lenguaje de programación:** Python
- **Configuración y serialización:** YAML (`.yaml`)
- **Documentación y tareas:** Markdown (`.md`) / Texto plano

---

## 📁 Estructura del proyecto

El diseño es altamente desacoplado, separando responsabilidades claras en cada directorio:

```text
.
├── config/
│   └── agents/          # Definición declarativa (.yaml) de cada rol
├── docs/
│   ├── DECISIONES.md    # Decisiones técnicas y de arquitectura
│   └── USO.md           # Guía detallada de integración y uso
├── src/
│   ├── main.py          # Punto de entrada y bucle de orquestación
│   ├── agent.py         # Clase genérica Agent (carga YAML y ejecuta el LLM)
│   ├── harness.py       # Guardia de seguridad y aislamiento de rutas
│   └── tools.py         # Herramientas atómicas (archivos y Git)
├── .env.example         # Plantilla de variables de entorno
├── requirements.txt     # Dependencias del proyecto
└── TAREA_ACTUAL.md      # Definición de la tarea a resolver
```

### Detalle de módulos

#### 📂 `src/`
- **`main.py`**: Punto de entrada desde el que se lanza el flujo agéntico. Lee las variables de entorno (`.env`) y la tarea actual (`TAREA_ACTUAL.md`), instancia los objetos `Agent`, gestiona el paso de contexto entre agentes y coordina el bucle de ejecución, corrección y pruebas.
- **`agent.py`**: Define la clase genérica `Agent`. Al instanciar un objeto de esta clase, lee su archivo `.yaml` correspondiente en `config/agents/` para determinar su `system_prompt`, permisos, alcance y herramientas permitidas.
- **`harness.py`**: Capa de seguridad (*sandbox* de rutas). Valida que ninguna ruta a la que intente acceder un agente salga del directorio del proyecto objetivo que se está editando.
- **`tools.py`**: Contiene las acciones atómicas que interactúan con el sistema: lectura/escritura de archivos y comandos de control de versiones con **Git**.

#### 📂 `docs/`
- [`DECISIONES.md`](docs/DECISIONES.md): Recoge las decisiones técnicas relevantes y determinantes para guiar al usuario sobre el enfoque de la aplicación.
- [`USO.md`](docs/USO.md): Guía detallada de integración, configuración obligatoria/opcional y ejecución.

---

## 🚀 Uso rápido

Para poner en marcha el proyecto con su configuración base (sin modificar el código fuente), sigue estos pasos:

1. **Instalar dependencias** (recomendado dentro de un entorno virtual):
   ```bash
   pip install -r requirements.txt
   ```
2. **Configurar el entorno**: Crea un archivo `.env` a partir de `.env.example` con la ruta al proyecto objetivo (`TARGET_PROJECT_DIR`) y tus claves de API si usas un proveedor externo.
3. **Definir la tarea**: Escribe el objetivo del día en `TAREA_ACTUAL.md`.
4. **Ejecutar el flujo**:
   ```bash
   python src/main.py
   ```

> 💡 Para instrucciones completas de integración y configuración avanzada, consulta la [Guía de Uso (`docs/USO.md`)](docs/USO.md).
