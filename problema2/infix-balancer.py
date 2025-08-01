def balanceador_infix(expression):
    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}
    steps = []

    for char in expression:
        if char in '([{':
            stack.append(char)
        elif char in ')]}':
            if not stack or stack[-1] != pairs[char]:
                steps.append(f"Pila: {stack} → ERROR con '{char}'")
                return False, steps
            stack.pop()
        steps.append(f"Pila: {stack}")

    if not stack:
        return True, steps
    else:
        steps.append(f"Pila: {stack} → ERROR: quedan símbolos sin cerrar")
        return False, steps


def procesador_archivo(file_path):
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            expression = line.strip()
            print(f"\nLínea {line_number}: '{expression}'")
            balanced, steps = balanceador_infix(expression)
            print("Secuencia de la pila:")
            for step in steps:
                print(step)
            print("Resultado:", "Balanceada ✅" if balanced else "Desbalanceada ❌")


# Archivo de prueba
file_path = 'expresiones.txt'
procesador_archivo(file_path)
