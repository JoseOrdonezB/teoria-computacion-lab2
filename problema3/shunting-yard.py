def expandir_clases(expr):
    resultado = ''
    i = 0
    while i < len(expr):
        if expr[i] == '\\':
            if i + 1 < len(expr):
                resultado += expr[i:i+2]
                i += 2
        elif expr[i] == '[':
            i += 1
            contenido = ''
            while i < len(expr) and expr[i] != ']':
                contenido += expr[i]
                i += 1
            if i < len(expr) and contenido:
                resultado += '(' + '|'.join(contenido) + ')'
                i += 1
            else:
                raise ValueError("Clase de caracteres sin cerrar o vacía")
        else:
            resultado += expr[i]
            i += 1
    return resultado

def insertar_concatenaciones(expr):
    resultado = ''
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
            if ((c1 not in {'(', '|'} and c2 not in {'*', '+', '?', '|', ')'})
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
            if i + 1 < len(expr):
                resultado += expr[i:i+2]
                i += 2
            else:
                raise ValueError("Escape incompleto")
        elif expr[i] == '+':
            if resultado and resultado[-1] == ')':
                count = 0
                j = len(resultado) - 1
                while j >= 0:
                    if resultado[j] == ')':
                        count += 1
                    elif resultado[j] == '(':
                        count -= 1
                        if count == 0:
                            break
                    j -= 1
                grupo = resultado[j:]
                resultado += '.' + grupo + '*'
            else:
                prev = resultado.rstrip('.')[-1]
                resultado += '.' + prev + '*'
            i += 1
        elif expr[i] == '?':
            if resultado and resultado[-1] == ')':
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

        if c == ' ':
            i += 1
            continue

        if c == '\\':
            if i + 1 < len(regex):
                salida.append('\\' + regex[i + 1])
                i += 2
            else:
                raise ValueError("Secuencia de escape incompleta")
        elif c.isalnum() or c in {'ε', '@', '.', '{', '}'}:
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
                i += 1
            else:
                raise ValueError("Falta paréntesis de apertura")
        elif c in operadores:
            while (pila and pila[-1] in operadores and
                   precedencia[c] <= precedencia[pila[-1]]):
                salida.append(pila.pop())
            pila.append(c)
            i += 1
        else:
            raise ValueError(f"Carácter no reconocido: '{c}'")

    while pila:
        top = pila.pop()
        if top in {'(', ')'}:
            raise ValueError("Paréntesis desbalanceados.")
        salida.append(top)

    return salida

def procesar_archivo(nombre_archivo):
    print(f"📂 Abriendo archivo: {nombre_archivo}")
    with open(nombre_archivo, 'r') as archivo:
        lineas = archivo.readlines()

    for i, linea in enumerate(lineas):
        original = linea.strip()
        if not original:
            print(f"Línea vacía #{i+1}, se omite.")
            continue

        print(f"\nProcesando expresión [{i+1}]: {original}")
        try:
            clase_expandida = expandir_clases(original)
            print(f"Expandida clase de caracteres: {clase_expandida}")

            con_concat = insertar_concatenaciones(clase_expandida)
            print(f"Con concatenaciones explícitas: {con_concat}")

            expandida = expandir_operadores(con_concat)
            print(f"Después de expandir operadores: {expandida}")

            postfijo = shunting_yard(expandida)
            print(f"✅ Expresión en postfijo: {' '.join(postfijo)}")
        except Exception as e:
            print(f"❌ Error al procesar la expresión #{i+1}: {e}")

    print("\n🎉 ¡Procesamiento finalizado!")

# Ejecutar el procesamiento del archivo
procesar_archivo("problema3/input.txt")