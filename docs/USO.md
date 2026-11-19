# Guía de Uso — `multiagent-template`

Este proyecto es una plantilla **plug-and-play** en Python diseñada para ejecutarse en un directorio hermano al proyecto objetivo sobre el que trabajarán los agentes.

---

## 1. Integración

Para integrar el motor multiagente con cualquier repositorio existente, colócalo como **directorio hermano** dentro de tu carpeta de trabajo:

```text
workspaces/
├── proyecto-objetivo/       # Tu repositorio real (destino de los cambios)
└── multiagent-template/     # Esta plantilla multiagente
```

### Pasos de integración inicial

1. **Clona o copia** `multiagent-template/` junto a tu proyecto objetivo.
2. **Crea y activa un entorno virtual** dentro de `multiagent-template/`:
   ```bash
   python -m venv .venv
   ```
   - En Windows (PowerShell):
     ```powershell
     .venv\Scripts\Activate.ps1
     ```
   - En Linux / macOS:
     ```bash
     source .venv/bin/activate
     ```
3. **Instala las dependencias** definidas en `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

---

## 2. Configuraciones Obligatorias

Antes de ejecutar el flujo, debes completar estos tres elementos mínimos:

1. **Archivo `.env` (a partir de `.env.example`):**
   Copia `.env.example` a `.env` y define al menos la ruta al proyecto hermano y el proveedor LLM:
   ```env
   TARGET_PROJECT_DIR=../proyecto-objetivo
   LLM_PROVIDER=mock
   LLM_API_KEY=
   ```
   - `TARGET_PROJECT_DIR`: Ruta relativa (o absoluta) hacia el directorio raíz del proyecto objetivo. `src/harness.py` utilizará esta ruta como límite estricto de seguridad.
   - `LLM_PROVIDER`: Proveedor a utilizar (`mock` para pruebas locales sin coste, o el proveedor real configurado en `src/agent.py`).
   - `LLM_API_KEY`: Clave de API obligatoria cuando `LLM_PROVIDER` sea distinto de `mock`.

2. **Definición de la tarea (`TAREA_ACTUAL.md`):**
   Escribe en `TAREA_ACTUAL.md` el objetivo concreto, contexto y criterios de aceptación que el orquestador y el resto de agentes deben resolver en la ejecución actual.

3. **Roles de agentes (`config/agents/*.yaml`):**
   Asegúrate de que existan y sean válidos los archivos YAML de los agentes en `config/agents/`:
   - `orquestador.yaml`
   - `backend.yaml`
   - `frontend.yaml`
   - `tester.yaml`
   - `releaser.yaml`

---

## 3. Configuraciones Opcionales

Puedes ajustar el comportamiento del sistema sin modificar el código Python en `src/`:

- **Modo simulación (`DRY_RUN` en `.env`):**
  ```env
  DRY_RUN=true
  ```
  Evita escrituras reales en el proyecto objetivo, útil para validar prompts y permisos antes de aplicar cambios.

- **Modelo específico (`LLM_MODEL` en `.env`):**
  ```env
  LLM_MODEL=mock-v1
  ```
  Permite indicar el identificador de modelo que utilizará `src/agent.py`.

- **Personalización de agentes (`config/agents/*.yaml`):**
  En cada archivo YAML puedes ajustar:
  - `system_prompt`: Instrucciones específicas del rol adaptadas al stack de tu proyecto objetivo (por ejemplo, FastAPI, React, Next.js, etc.).
  - `permissions`: Niveles de permiso (`read`, `write`, `execute`).
  - `allowed_tools`: Lista blanca de herramientas permitidas (`list_files`, `read_file`, `write_file`, `git_status`, `git_diff`).

- **Extensión de herramientas o proveedores (`src/`):**
  - Añade nuevas funciones en `src/tools.py` respetando `WorkspaceHarness` (`src/harness.py`).
  - Conecta clientes HTTP de proveedores LLM reales dentro de `src/agent.py`.

---

## 4. Ejecución del proyecto

Con el entorno virtual activo y las configuraciones listas, ejecuta el punto de entrada principal desde la raíz de `multiagent-template/`:

```bash
python src/main.py
```

### Flujo de ejecución

1. `src/main.py` carga las variables de `.env` y el contenido de `TAREA_ACTUAL.md`.
2. Inicializa `WorkspaceHarness` (`src/harness.py`) sobre `TARGET_PROJECT_DIR` para garantizar que ninguna operación salga del proyecto objetivo.
3. Ejecuta secuencialmente los agentes definidos en `config/agents/` (`orquestador` → `backend` → `frontend` → `tester` → `releaser`), propagando el contexto acumulado entre pasos.
4. Muestra por consola el resultado de cada agente y el resumen final del flujo.
