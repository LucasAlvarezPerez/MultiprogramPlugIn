import os
import json
import yaml
from pathlib import Path
from harness import SecurityHarness
from tools import Toolkit

class Agent:
    def __init__(self, yaml_path: Path, harness: SecurityHarness):
        # 1. Carga la configuración declarativa desde el YAML
        with open(yaml_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        self.name: str = config["name"]
        self.role: str = config["role"]
        self.system_prompt: str = config["system_prompt"]
        self.allowed_paths: list[str] | None = config.get("allowed_paths")
        allowed_tools_names: list[str] = config.get("allowed_tools", [])

        # 2. Instancia el Toolkit atado a los límites de ruta de este agente
        self._toolkit = Toolkit(harness, self.allowed_paths)

        # 3. Registro dinámico: solo expone los métodos autorizados en el YAML
        self.tools = {}
        for tool_name in allowed_tools_names:
            if hasattr(self._toolkit, tool_name):
                self.tools[tool_name] = getattr(self._toolkit, tool_name)
            else:
                raise ValueError(f"La herramienta '{tool_name}' configurada en {yaml_path.name} no existe en Toolkit.")

    def ejecutar(self, prompt_usuario: str) -> str:
        """Envía el contexto al LLM (o al simulador Mock) y devuelve la respuesta."""
        mock_mode = os.getenv("MOCK_MODE", "true").lower() == "true"

        if mock_mode:
            return self._ejecutar_mock(prompt_usuario)

        # Aquí irá la llamada real al SDK de Gemini (google-genai) con Function Calling
        raise NotImplementedError("Conecta el SDK de Gemini aquí cuando desactives MOCK_MODE.")

    def _ejecutar_mock(self, prompt_usuario: str) -> str:
        """Simula el comportamiento del agente para probar el Loop jerárquico gratis."""
        if "orquestador" in self.name.lower():
            # Simula una decisión distinta según el turno leyendo el historial
            if "Reporte de BACKEND" not in prompt_usuario:
                return json.dumps({
                    "siguiente_agente": "backend",
                    "instruccion": "Crea los modelos de datos iniciales."
                })
            elif "Reporte de TESTER" not in prompt_usuario:
                return json.dumps({
                    "siguiente_agente": "tester",
                    "instruccion": "Verifica que el proyecto compile sin errores."
                })
            else:
                return json.dumps({
                    "siguiente_agente": "FINALIZAR",
                    "instruccion": "Flujo simulado completado con éxito."
                })

        if "tester" in self.name.lower():
            return "ESTADO: APROBADO. Todos los tests simulados pasaron."

        return f"[{self.name}] Tarea simulada completada usando herramientas: {list(self.tools.keys())}"