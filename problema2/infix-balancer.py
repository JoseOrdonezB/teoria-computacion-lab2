def verificar_balanceo(expresion):
    stack = []
    pares = {')': '(', ']': '[', '}': '{'}
    pasos = []
    
    for i, char in enumerate(expresion):
        if char in '([{':
            stack.append(char)
            pasos.append(f"Push '{char}': Stack actual {stack}")
        elif char in ')]}':
            if not stack:
                pasos.append(f"Error en posición {i}: '{char}' no tiene apertura")
                return False, pasos
            top = stack.pop()
            pasos.append(f"Pop '{top}' al encontrar '{char}': Stack actual {stack}")
            if top != pares[char]:
                pasos.append(f"Error en posición {i}: '{char}' no coincide con '{top}'")
                return False, pasos
    
    balanceado = len(stack) == 0
    if not balanceado:
        pasos.append(f"Error: Símbolos sin cerrar: {stack}")
    return balanceado, pasos

def procesar_archivo(nombre_archivo):
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as file:
            lineas = file.readlines()
        
        for i, linea in enumerate(lineas, 1):
            linea = linea.strip()
            if not linea:
                continue
                
            print(f"\nProcesando línea {i}: {linea}")
            balanceado, pasos = verificar_balanceo(linea)
            
            print("Pasos de la pila:")
            for paso in pasos:
                print(f"  {paso}")
            
            resultado = "BIEN balanceada" if balanceado else "MAL balanceada"
            print(f"\nResultado: La expresión está {resultado}")
    
    except FileNotFoundError:
        print(f"Error: El archivo '{nombre_archivo}' no fue encontrado")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Uso: python balanceador.py archivo.txt")
    else:
        print("Iniciando proceso de verificación de balanceo...")
        procesar_archivo(sys.argv[1])