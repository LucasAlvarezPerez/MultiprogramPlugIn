import subprocess
from harness import SecurityHarness

class Toolkit:
    def __init__(self, harness: SecurityHarness, allowed_paths: list[str] | None = None):
        self.harness = harness
        self.allowed_paths = allowed_paths
        
    def leer_archivo(self, ruta_relativa: str) -> str: 
        """ Lee el contenido de un archivo dentro del proyecto objetivo: """
        try: 
            ruta_segura = self.harness.resolver_ruta_segura(ruta_relativa, self.allowed_paths)
            if not ruta_segura.exists():
                return f"Error: El archivo '{ruta_relativa}' no existe."
            return ruta_segura.read_text(encoding="utf-8")
        
        except PermissionError as e: 
            return str(e)
        
        
    def escribir_archivo(self, ruta_relativa: str, contenido: str) -> str:
        """Crea o sobreescribe un archivo entero de las rutas permitidas del agente. """
        try: 
            ruta_segura = self.harness.resolver_ruta_segura(ruta_relativa, self.allowed_paths)
            # Crea carpetas intermedias si no existen
            ruta_segura.parent.mkdir(parents=True, exist_ok=True)
            ruta_segura.write_text(contenido, encoding="utf-8")
            return f"Exito: Archivo '{ruta_relativa}' guardado correctamente"
        except PermissionError as e: 
            return str(e)
    
    def ejecutar_comando(self, comando: str) -> str: 
        """Ejecuta un comando en la terminal dentro de la raíz del proyecto"""
        try: 
            resultado = subprocess.run(
                comando, 
                shell=True, 
                cwd = self.harness.workspace_root, 
                capture_output=True, 
                text=True,
                timeout=30
            )
            salida = resultado.stdout if resultado.returncode == 0 else resultado.stderr
            return f"Código de salida: {resultado.returncode}\n Salida: \n {salida}"
        except subprocess.TimeoutExpired:
            return "Error: El comando excedió el tiempo límite de 30 segundos."
        
    def git_status(self) -> str: 
        """Comprueba el estado de Git en el proyecto Objetivo"""
        return self.ejecutar_comando("git status --short")
    
    def git_commit(self, mensaje: str) -> str:
        self.ejecutar_comando("git add . ")
        return self.ejecutar_comando(f"git commit -m {mensaje}")