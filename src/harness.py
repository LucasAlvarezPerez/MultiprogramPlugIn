import os
from pathlib import Path 
from dotenv import load_dotenv

load_dotenv()

class SecurityHarness: 
    def __init__(self):
        raw = os.getenv("TARGET_PROJECT_PATH")
        if not raw:   
            raise ValueError("Falta TARGET_PROJECT_PATH en el archivo .env")
        
        # Resuelve la ruta absoluta real (elimina '../' y symlinks)
        self.workspace_root = Path(raw).resolve()
        
        if not self.workspace_root.exists() or not self.workspace_root.is_dir():
            raise FileNotFoundError(f"El directorio objetivo no existe: {self.workspace_root}")
        
    def resolver_ruta_segura(self, ruta_relativa: str, allowed_paths: list[str] | None = None) -> Path: 
        """
        Valida que la ruta esté dentro del workspace y dentro de los 
        subdirectorios permitidos para el agente. Devuelve el objeto Path 
        listo para usarse
        """
        
        # 1. Construye y resuelve la ruta destino
        ruta_destino = (self.workspace_root / ruta_relativa).resolve()
        # 2. Comprueba que no haya escapado del proyecto
        if not ruta_destino.is_relative_to(self.workspace_root):
            raise PermissionError(
                f"[BLOQUEO DE ARNÉS] Intento de escape fuera del workspace: '{ruta_relativa}'"
            )
        
        # 3. Comprueba los límites específicos del agente 
        if allowed_paths is not None: 
            permitido = False
            for subruta in allowed_paths: 
                ruta_permitida = (self.workspace_root / subruta).resolve()
                if ruta_destino == ruta_permitida or ruta_destino.is_relvative_to(ruta_permitida):
                    permitido = True
                    break
            if not permitido: 
                raise PermissionError(
                    f"[BLOQUEO DE ARNÉS] Acceso denegado a '{ruta_relativa}'."
                    f"Rutas autorizadas para este agente: {allowed_paths}"
                )
                
        return ruta_destino