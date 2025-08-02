import re

def insertar_concatenaciones(expr):
    resultado = ''
    caracteres_binarios = {'*', '+', '?', ')'}
    caracteres_izquierda = {'(', '|'}
    
    i = 0
    while i < len(expr):
        c1 = expr[i]
        resultado += c1

        if c1 == '\\':
            i += 1
            if i < len(expr):
                resultado += expr[i]
        elif i + 1 < len(expr):
            c2 = expr[i + 1]
            if ((c1 not in caracteres_izquierda and c2 not in {'*', '+', '?', '|', ')'})
                or (c1 in {'*', '+', '?'} and c2 not in {'*', '+', '?', '|', ')'})
                or (c1 == ')' and c2 == '(')
                or (c1 == ')' and c2.isalnum())
                or (c1.isalnum() and c2 == '(')):
                resultado += '.'
        i += 1
    return resultado

def expandir_operadores(expr):
    i = 0
    resultado = ''
    while i < len(expr):
        if expr[i] == '\\':
            resultado += expr[i:i+2]
            i += 2
        elif expr[i] == '+':
            prev = resultado.rstrip('.')[-1]
            if prev == ')':
                resultado += '.A*'
            else:
                resultado += '.' + prev + '*'
            i += 1
        elif expr[i] == '?':
            prev = resultado.rstrip('.')[-1]
            if prev == ')':
                resultado += '|ε'
            else:
                resultado += '|ε'
            i += 1
        else:
            resultado += expr[i]
            i += 1
    return resultado

def shunting_yard(regex):
    salida = []
    pila = []

    precedencia = {
        '*': 3,
        '.': 2,
        '|': 1
    }

    operadores = set(precedencia.keys())
    i = 0

    while i < len(regex):
        c = regex[i]
        if c == '\\':
            salida.append('\\' + regex[i+1])
            i += 2
        elif c.isalnum() or c == 'ε':
            salida.append(c)
            i += 1
        elif c == '(':
            pila.append(c)
            i += 1
        elif c == ')':
            while pila and pila[-1] != '(':
                salida.append(pila.pop())
            if pila:
                pila.pop()
            else:
                raise ValueError("Falta parentesis de apertura '('")
            i += 1
        elif c in operadores:
            while (pila and pila[-1] in operadores and
                   precedencia[c] <= precedencia[pila[-1]]):
                salida.append(pila.pop())
            pila.append(c)
            i += 1
        else:
            raise ValueError(f"Carácter no reconocido en la expresión: '{c}'")

    while pila:
        top = pila.pop()
        if top in {'(', ')'}:
            raise ValueError("Parentesis desbalanceados.")
        salida.append(top)

    return salida

def procesar_archivo(nombre_archivo):
    print(f"Abriendo archivo: {nombre_archivo}")
    with open(nombre_archivo, 'r') as archivo:
        lineas = archivo.readlines()

    for i, linea in enumerate(lineas):
        original = linea.strip()
        if not original:
            print(f"Línea vacía #{i+1}, se omite.")
            continue

        print(f"\nProcesando expresión [{i+1}]: {original}")
        try:
            con_concat = insertar_concatenaciones(original)
            print(f"Con concatenaciones explícitas: {con_concat}")

            expandida = expandir_operadores(con_concat)
            print(f"Después de expandir operadores: {expandida}")

            postfijo = shunting_yard(expandida)
            print(f"Expresión en postfijo: {' '.join(postfijo)}")
        except Exception as e:
            print(f"Error al procesar la expresión #{i+1}: {e}")

    print("\n¡Procesamiento finalizado!")

# Ejecutar el procesamiento del archivo
procesar_archivo("problema3/input.txt")