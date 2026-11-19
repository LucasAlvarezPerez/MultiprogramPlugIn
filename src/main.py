from pathlib import Path
from dotenv import load_dotenv
from harness import SecurityHarness
from agent import Agent

load_dotenv()

def cargar_tarea() -> str: 
    """Lee el objetivo diario desde TAREA_ACTUAL.md en la raíz del proyecto"""
    ruta_tarea = Path(__file__).parent.parent 
    if not ruta_tarea.exists():
        raise FileNotFoundError("No se encontró TAREA_ACTUAL.md en la raíz")
    return ruta_tarea.read_text(encoding="utf-8")

def main(): 
    print("[0] Incializando motor multiagente...")
    
    harness = SecurityHarness()
    config_dir = Path(__file__).parent.parent
    
    # 1. Instanciamos al orquestador y sus trabajadores
    orquestador = Agent(config_dir, harness)
    
    equipo = {
        "backend": Agent(config_dir, harness),
        "frontend": Agent(config_dir, harness),
        "tester": Agent(config_dir, harness),
        "runner": Agent(config_dir, harness),
        "documentator": Agent(config_dir, harness)
    }
    
    tarea_objetivo = cargar_tarea()
    historial_contexto = f"OBJETIVO DEL USUARIO: \n{tarea_objetivo}\n"
    
    max_turnos = 10 # Freno de emergencia para evitar bucles infinitos
    turno = 1
    
    # 2. Loop jerárquico
    while turno <= max_turnos: 
        print(f"\n [TURNO {turno}/{max_turnos}] El orquestador está evaluando... ")
        
        decision_raw = orquestador.ejecutar(historial_contexto)
        
        try:
            decision = json.loads(decision_raw)
        except json.JSONDecodeError:
            print("[ERROR] El orquestador no devolvió un JSON válido. Reintentnado")
            historial_contexto += "\n[SISTEMA] Error del formato. Responde estrictamente con JSON"
            truno += 1; 
            continue
        
        agente_elegido = decision.get("siguiente_agente")
        instruccion = decision.get("instruccion")
        
        # 3. Condicion de parada decidida por el orquestado 
        if agente_elegido == "FINALIZAR":
            print(f"\n [ORQUESTADOR] Tarea completada: {instruccion}")
            break
        
        # 4. Delegación dinámica
        if agente_elegido in equipo: 
            print(f"[ORQUESTADOR] Delegando a [{agente_elegido.upper()}]: {instruccion}")
            resultado_trabajador = equipo[agente_elegido].ejecutar(
                f"Contexto previo: \n {historial_contexto}\n\n Tu tarea específica ahora: \n {instruccion}"
            )
            
            # Añadimos lo que hizo el trabajador a la memoria para que el orquestador lo evalúe en el siguiente turno 
            historial_contexto += f"\n--- Reporte de {agente_elegido.upper()} --- \n{resultado_trabajador}\n "
        else:
            historial_contexto += f"\n[SISTEMA]: El agente '{agente_elegido}' no existe. Usa {list(equipo.kyes())} o FINALIZAR"
            
        turno += 1
    if  turno > max_turnos: 
        print("\n [ABORTADO] Se alcanzó el límite de iteraciones del Orquestador.")
        
if __name__ == "__main__":
    main()
    
    