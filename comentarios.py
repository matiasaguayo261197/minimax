# -------------------------------------------------------------------------
# 1. PREPARANDO LAS HERRAMIENTAS (IMPORTS)
# Python viene con "cajas de herramientas" cerradas. Con 'import' las abrimos.
# -------------------------------------------------------------------------

import random  # Trae herramientas para generar cosas al azar (como tirar dados).
import os      # Trae herramientas del Sistema Operativo (Operating System), servirá para limpiar la pantalla.
import time    # Trae herramientas para controlar el tiempo (ej: pausar el juego 1 segundo).

# -------------------------------------------------------------------------
# 2. DEFINIENDO LOS PERSONAJES (VARIABLES)
# -------------------------------------------------------------------------

gato = 'G'     # Creamos una caja llamada "gato" y le guardamos la letra 'G'.
raton = 'R'    # Creamos una caja llamada "raton" y le guardamos la letra 'R'.

# -------------------------------------------------------------------------
# 3. FABRICANDO EL TABLERO DE JUEGO
# -------------------------------------------------------------------------

def crear_mapa(alto, ancho):
    # DEFINICIÓN: Le enseñamos a la PC a "crear_mapa". Pide dos números: alto y ancho.
    
    mapa = [] 
    # Crea una lista vacía (una caja que puede contener muchas cosas dentro). 
    # Aquí guardaremos todas las filas de nuestro tablero.
    
    for piso in range(alto):
        # ITERADOR: 'range(alto)' genera una lista de números (ej: si alto es 3, genera 0, 1, 2).
        # El 'for' significa "repite el código de abajo esta cantidad de veces".
        # 'piso' es el nombre temporal que le damos a la repetición actual. 
        # Itera para construir el mapa piso por piso (fila por fila).
        
        fila = ['.'] * ancho
        # Crea una nueva caja llamada "fila". 
        # Toma un punto '.', que representa el suelo vacío, y el símbolo '*' lo multiplica. 
        # Si el ancho es 5, esto crea instantáneamente una lista de 5 puntos: ['.', '.', '.', '.', '.']
        
        mapa.append(fila)
        # La palabra '.append' significa "agregar al final". 
        # Toma la 'fila' completa que acabamos de crear y la mete dentro de la caja grande 'mapa'.
        
    return mapa 
    # RETORNO: Una vez que el 'for' termina de dar vueltas y el mapa está completo, 
    # 'return' escupe el resultado final hacia afuera para que el juego pueda usarlo. 
    # Retorna un "tablero" (una lista llena de otras listas).

# -------------------------------------------------------------------------
# 4. MOSTRANDO EL TABLERO EN LA PANTALLA
# -------------------------------------------------------------------------

def mostrar_mapa(tablero):
    # DEFINICIÓN: Le enseñamos a la PC a imprimir el mapa en la pantalla. 
    # Recibe como ingrediente el 'tablero' que creamos en el paso anterior.
    
    for fila in tablero:
        # ITERADOR: Toma el tablero grande y saca la primera 'fila'. 
        # Ejecuta la línea de abajo, luego vuelve arriba para sacar la segunda 'fila', y así sucesivamente.
        # Itera sobre el tablero para poder imprimirlo línea por línea.
        
        print(' '.join(fila))
        # 'print' es la orden para mostrar texto en la pantalla.
        # '.join' es un pegamento. Toma la lista ['.', '.', '.'] y une cada elemento usando
        # lo que hay entre las comillas (un espacio vacío ' '). 
        # El resultado visual en pantalla será: . . .

def movimientos_permitidos(tablero, y, x):
    # DEFINICIÓN: Le enseñamos a la PC a ser el "guardia". 
    # Necesita el 'tablero', y la posición vertical 'y' (fila) y horizontal 'x' (columna) que queremos revisar.

    alto = len(tablero)
    # VARIABLE Y OPERADOR: Creamos una caja llamada 'alto'. 
    # 'len()' viene de "length" (longitud). Cuenta cuántas filas tiene el tablero.
    # Si el tablero tiene 5 filas, 'len(tablero)' se convierte en un 5, y se guarda en 'alto'.

    ancho = len(tablero[0])
    # SINTAXIS CLAVE: Creamos la caja 'ancho'. 
    # 'tablero[0]' agarra específicamente la primera fila del mapa. 
    # Luego, 'len()' cuenta cuántos cuadritos hay en esa sola fila para saber el ancho total.

    if 0 <= y < alto and 0 <= x < ancho:
        # LÓGICA MATEMÁTICA: La pregunta del guardia.
        # '0 <= y < alto': Verifica que la fila 'y' no sea negativa (0 o más) y que sea menor al 'alto' máximo.
        # 'and': Significa "Y además". Ambas condiciones deben cumplirse.
        # '0 <= x < ancho': Verifica que la columna 'x' esté dentro de los límites de izquierda a derecha.
        
        return True
        # RETORNO: Si la posición está dentro del mapa, el guardia responde 'True' (Verdadero / "Es seguro").
        
    else:
        # CONDICIONAL: Significa "Si lo de arriba NO se cumplió..." (es decir, la posición se sale del mapa).
        
        return False
        # RETORNO: El guardia responde 'False' (Falso / "Peligro, te caes del mapa").

def obtener_movimientos_posibles(tablero, y, x):
    # DEFINICIÓN: Le pedimos a la PC que nos dé todas las opciones válidas para caminar.
    # Necesita saber cómo es el 'tablero' y dónde estamos parados ahora ('y', 'x').

    movimientos = []
    # VARIABLE: Creamos una lista vacía `[]` llamada 'movimientos'. 
    # Aquí iremos guardando los pasos seguros que encontremos. Empieza vacía.

    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    # LÓGICA ESPACIAL: Creamos una lista con los 4 movimientos posibles en un mapa 2D.
    # (-1, 0) -> Restar 1 a 'y' (Subir), no cambiar 'x'.
    # (1, 0)  -> Sumar 1 a 'y' (Bajar), no cambiar 'x'.
    # (0, -1) -> No cambiar 'y', restar 1 a 'x' (Ir a la izquierda).
    # (0, 1)  -> No cambiar 'y', sumar 1 a 'x' (Ir a la derecha).

    for dy, dx in direcciones:
        # ITERADOR MULTIPLE: 'for' revisa la lista de direcciones una por una.
        # 'dy' (delta y / cambio en y) agarra el primer número del par.
        # 'dx' (delta x / cambio en x) agarra el segundo número del par.
        
        nueva_y = y + dy
        # MATEMÁTICA: Calcula cómo quedaría la fila si damos ese paso.
        
        nueva_x = x + dx
        # MATEMÁTICA: Calcula cómo quedaría la columna si damos ese paso.
        
        if movimientos_permitidos(tablero, nueva_y, nueva_x):
            # LLAMADA AL GUARDIA: Usamos la función de arriba. 
            # Le pasamos la 'nueva_y' y 'nueva_x' simuladas. 
            # Si el guardia responde 'True' (Verdadero), entramos a la siguiente línea.
            
            movimientos.append([nueva_y, nueva_x])
            # ACCIÓN: Como el guardia dijo que es seguro, '.append()' agarra ese nuevo 
            # par de coordenadas y lo guarda dentro de nuestra lista de 'movimientos'.

    return movimientos
    # RETORNO: Una vez que el 'for' terminó de revisar las 4 direcciones, 
    # la función nos entrega la lista final con las coordenadas seguras a las que podemos ir.

def actualizar_tablero(tablero, pos_gato, pos_raton):
    # DEFINICIÓN: Le enseñamos a la PC a "dibujar" el estado actual del juego.
    # Necesita el lienzo ('tablero') y las coordenadas exactas donde están el gato y el ratón.

    for filas in range(len(tablero)):
        # ITERADOR PRINCIPAL: Toma la cantidad de filas (el alto) y empieza a recorrerlas una por una.
        # Es como decirle al pintor: "Empieza por la fila de arriba y ve bajando".

        for columnas in range(len(tablero[0])):
            # ITERADOR ANIDADO (Un bucle dentro de otro bucle): 
            # Mientras el pintor está en una 'fila', este 'for' le dice: 
            # "Ahora camina por cada columna de esta fila, de izquierda a derecha".

            tablero[filas][columnas] = '.'
            # ACCIÓN DE LIMPIEZA: Los corchetes dobles [filas][columnas] son como las 
            # coordenadas de un tablero de ajedrez (ej. A1, B2). 
            # El '=' asigna el valor. En cada cuadrito, el pintor dibuja un punto '.', 
            # borrando cualquier rastro viejo del gato o el ratón.

    tablero[pos_gato[0]][pos_gato[1]] = gato
    # SOBRESCRIBIR: Una vez que todo el tablero está limpio (lleno de '.'), 
    # usamos las coordenadas del gato. 'pos_gato[0]' es su fila (y), 'pos_gato[1]' es su columna (x).
    # En ese cuadrito exacto, pintamos la variable 'gato' (que contenía la letra 'G').

    tablero[pos_raton[0]][pos_raton[1]] = raton
    # SOBRESCRIBIR: Hacemos exactamente lo mismo, pero en las coordenadas del ratón,
    # pintando la variable 'raton' (la letra 'R'). ¡El tablero está listo para mostrarse!

def mover_raton_al_azar(tablero, pos_raton):
    # DEFINICIÓN: Le enseñamos al ratón a moverse. 
    # Necesita mirar el 'tablero' y saber su propia posición ('pos_raton').

    opciones = obtener_movimientos_posibles(tablero, pos_raton[0], pos_raton[1])
    # VARIABLE Y LLAMADA: Usa la "brújula" que creamos en la sesión anterior.
    # Le pasa el tablero y sus coordenadas separadas en 'y' (0) y 'x' (1).
    # Guarda la lista de lugares seguros (por ejemplo: [Arriba, Derecha]) en la caja 'opciones'.

    if len(opciones) > 0:
        # LÓGICA DE SUPERVIVENCIA: 'len(opciones)' cuenta cuántas rutas de escape hay.
        # Pregunta: "¿Tengo más de 0 opciones?". Si la respuesta es sí, entra a la siguiente línea.
        # (Si fuera 0, significaría que el ratón está acorralado y no hace nada).

        nueva_pos = random.choice(opciones)
        # EL DADO: Llama a la herramienta 'random' que trajimos al principio del programa.
        # '.choice()' agarra la lista de 'opciones' y elige una sola al azar, como sacar 
        # un papelito de un sombrero. Guarda esa decisión en la caja 'nueva_pos'.

        pos_raton = nueva_pos
        # ACTUALIZACIÓN: Ahora que tomó una decisión, reemplaza su coordenada vieja ('pos_raton')
        # con la coordenada nueva que acaba de elegir al azar.

    return pos_raton
    # RETORNO: Escupe la posición final del ratón para que el juego sepa dónde quedó.

def calcular_distancia(y1, x1, y2, x2):
    # DEFINICIÓN: El radar. Necesita las coordenadas del punto 1 (y1, x1) y del punto 2 (y2, x2).
    # Esta función implementa la fórmula exacta de la Distancia Manhattan.

    distancia_y = abs(y1 - y2)
    # MATEMÁTICA VERTICAL: Resta la fila 1 menos la fila 2 para saber cuántas "cuadras" 
    # verticales los separan. 
    # El operador 'abs()' (valor absoluto) es crucial aquí: si el gato está en la fila 2 
    # y el ratón en la 5, (2 - 5) da -3. Como no existen las "-3 cuadras", 'abs()' le quita 
    # el signo negativo y lo convierte en un 3 limpio.

    distancia_x = abs(x1 - x2)
    # MATEMÁTICA HORIZONTAL: Hace exactamente lo mismo, pero restando las columnas (x1 - x2)
    # para contar cuántas "cuadras" horizontales los separan.

    return distancia_y + distancia_x
    # RETORNO Y LÓGICA MANHATTAN: Suma los pasos verticales y horizontales. 
    # Al sumarlos, obtenemos exactamente el número de "cuadras" que el gato tendría que 
    # caminar para atrapar al ratón en este mundo de cuadrícula. Devuelve ese número total.

def minimax(mapa, pos_gato_simulada, pos_raton_simulada, profundidad, es_turno_gato):
    # DEFINICIÓN: La máquina de imaginar futuros. Necesita saber: cómo es el mapa, 
    # dónde están imaginando estar el gato y el ratón, la 'profundidad' (cuántos pasos al 
    # futuro le quedan por imaginar) y de quién es el turno ('es_turno_gato').

    # =========================================================================
    # EL CASO BASE (EL FRENO DE EMERGENCIA)
    # Aquí le decimos a la función cuándo DEBE dejar de llamarse a sí misma.
    # =========================================================================

    if pos_gato_simulada == pos_raton_simulada:
        # OPERADOR '==': A diferencia de un solo '=' que sirve para guardar cosas en cajas, 
        # el doble '==' es una PREGUNTA: "¿La coordenada del gato es exactamente igual a 
        # la del ratón en esta imaginación?".
        
        return 1000  
        # RETORNO Y CASO BASE 1: Si la respuesta es sí, el gato atrapó a su presa. 
        # La función se detiene por completo (frena la recursividad) y devuelve '1000' 
        # (un premio gigante) para indicar que este futuro imaginario es el mejor posible.
        
    if profundidad == 0:
        # OPERADOR '==': Pregunta "¿Se me acabó la energía para imaginar?". 
        # 'profundidad' es como el tanque de gasolina. Si llega a 0, debe parar.
        
        distancia = calcular_distancia(pos_gato_simulada[0], pos_gato_simulada[1], pos_raton_simulada[0], pos_raton_simulada[1])
        # VARIABLE: Usa nuestro radar (Distancia Manhattan) para ver qué tan cerca quedó.
        
        return -distancia 
        # RETORNO Y CASO BASE 2: Frena la recursividad. Devuelve la distancia con un 
        # signo negativo '-'. ¿Por qué? Porque el gato siempre buscará el número MÁS ALTO. 
        # Matemáticamente, -2 (estar a 2 pasos) es un número MAYOR que -10 (estar a 10 pasos).

    # =========================================================================
    # LA RECURSIVIDAD (EL SUEÑO DENTRO DEL SUEÑO)
    # Si no hemos chocado con los frenos de emergencia, seguimos imaginando.
    # =========================================================================

    # 2. El turno del Gato (Maximizar su puntaje)
    if es_turno_gato == True:
        # LÓGICA: ¿Es el turno de imaginar del gato? ('True' es Verdadero).
        
        mejor_puntaje = -9999 
        # VARIABLE: El gato quiere el puntaje máximo. Prepara una caja con un número 
        # absurdamente bajo (-9999). Así, el primer puntaje real que consiga (ej: -5) 
        # será matemáticamente mayor y reemplazará a este.
        
        opciones = obtener_movimientos_posibles(mapa, pos_gato_simulada[0], pos_gato_simulada[1])
        # VARIABLE: Saca la lista de todos los caminos seguros hacia donde puede ir el gato.
        
        for opcion in opciones:
            # ITERADOR: Toma cada camino posible (opcion) y lo pone a prueba, uno por uno.
            
            # --- ¡AQUÍ ESTÁ LA RECURSIVIDAD! ---
            puntaje = minimax(mapa, opcion, pos_raton_simulada, profundidad - 1, False)
            # LA MAGIA: La función 'minimax' se llama a SÍ MISMA desde adentro.
            # Le pasa el nuevo mapa simulado ('opcion' es donde se acaba de mover el gato).
            # Le resta 1 a la 'profundidad' (gasta un litro de gasolina de imaginación).
            # Le pasa 'False' (Falso) a 'es_turno_gato' para decirle a la imaginación: 
            # "En mi siguiente sueño, le toca mover al ratón".
            
            if puntaje > mejor_puntaje:
                # OPERADOR '>': Pregunta "¿El puntaje de este sueño futuro es MAYOR que 
                # mi récord actual ('mejor_puntaje')?".
                
                mejor_puntaje = puntaje
                # OPERADOR '=': Si es mayor, guarda ese nuevo récord en la caja.
                
        return mejor_puntaje
        # RETORNO: Tras evaluar todos los caminos y todos sus sub-sueños, entrega el número más alto.

    # 3. El turno del Ratón (Minimizar el puntaje del gato escapando)
    else:
        # LÓGICA 'else': Si no es el turno del gato, obligatoriamente le toca al ratón.
        
        peor_puntaje = 9999 
        # VARIABLE: El ratón es el "aguafiestas" del gato. Él quiere que el gato saque el 
        # puntaje MÁS BAJO posible. Empieza su caja con un número altísimo para ir bajándolo.
        
        opciones = obtener_movimientos_posibles(mapa, pos_raton_simulada[0], pos_raton_simulada[1])
        # VARIABLE: Obtiene los caminos por donde puede huir el ratón.
        
        for opcion in opciones:
            # ITERADOR: Prueba cada ruta de escape.
            
            # --- ¡AQUÍ ESTÁ LA RECURSIVIDAD OTRA VEZ! ---
            puntaje = minimax(mapa, pos_gato_simulada, opcion, profundidad - 1, True)
            # Se llama a sí misma. Ahora mueve al ratón ('opcion'), gasta gasolina ('profundidad - 1')
            # y le pasa 'True' (Verdadero) para que en el próximo sueño le vuelva a tocar al gato.
            
            if puntaje < peor_puntaje:
                # OPERADOR '<': Pregunta "¿Este camino le da al gato un puntaje MENOR 
                # (peor para el gato, mejor para el ratón) que mi récord actual?".
                
                peor_puntaje = puntaje
                # OPERADOR '=': Si es menor, guarda el récord para arruinarle el plan al gato.
                
        return peor_puntaje
        # RETORNO: Entrega el número más bajo que logró forzar al gato a tener.

def mover_gato_inteligente(tablero, pos_gato, pos_raton):
    # DEFINICIÓN: Esta función toma la decisión final en el mundo real.
    # Necesita ver el mapa ('tablero') y dónde están parados ambos personajes.
    
    mejor_puntaje = -9999
    # VARIABLE: Prepara una caja para anotar el puntaje récord. 
    # Empieza con un número muy bajo para que sea fácil de superar en el primer intento.
    
    mejor_movimiento = pos_gato
    # VARIABLE: Caja de emergencia por si no encuentra caminos. Dice "me quedo donde estoy".
    
    opciones = obtener_movimientos_posibles(tablero, pos_gato[0], pos_gato[1])
    # LLAMADA: Usa nuestra brújula para sacar la lista de pasos legales (arriba, abajo, etc.).
    
    for opcion in opciones:
        # ITERADOR: "Para cada camino legal posible, voy a probarlo uno por uno".
        
        # LA CONSULTA AL CEREBRO: El gato simula qué pasaría si hace este movimiento.
        # Le pide a 'minimax' que mire 3 pasos al futuro. El 'False' indica que 
        # en esa simulación, el siguiente en moverse será el ratón.
        puntaje = minimax(tablero, opcion, pos_raton, 3, False)
        
        if puntaje > mejor_puntaje:
            # CONDICIONANTE: Pregunta "¿El futuro que acabo de imaginar me da un puntaje 
            # MAYOR (>) que el récord que tengo guardado en mi caja?".
            
            mejor_puntaje = puntaje
            # SOBRESCRITURA: Si es mejor, actualiza su récord con este nuevo número.
            
            mejor_movimiento = opcion
            # SOBRESCRITURA: Anota cuál fue el paso inicial que lo llevó a ese buen futuro.
            
    return mejor_movimiento
    # RETORNO: Tras probar todos los caminos, le entrega al juego la coordenada exacta del mejor paso.


# =========================================================================
# PREPARACIÓN DE LA MESA DE JUEGO
# =========================================================================

tablero = crear_mapa(8, 8)
# Llama a nuestra fábrica para crear una cuadrícula vacía de 8 filas por 8 columnas.

pos_gato = [0, 0]
# Coloca al gato en la esquina superior izquierda (fila 0, columna 0).

pos_raton = [7, 7]
# Coloca al ratón en la esquina inferior derecha (fila 7, columna 7).

turnos_jugados = 1
# Crea el reloj del juego. Empezamos en el turno cero.

max_turnos = 20 
# Condición de finalización: El ratón gana si sobrevive esta cantidad de turnos.

actualizar_tablero(tablero, pos_gato, pos_raton)
# Le damos una primera mano de pintura al mapa para que los personajes aparezcan antes de jugar.


# =========================================================================
# EL MOTOR DEL JUEGO (EL BUCLE PRINCIPAL)
# =========================================================================

while turnos_jugados < max_turnos:
    # EL BUCLE WHILE: Significa "Mientras los turnos jugados sean MENORES a 20, 
    # repite todo este bloque de código sin parar". Es el motor que mantiene vivo el juego.
    
    os.system('cls' if os.name == 'nt' else 'clear')
    # HERRAMIENTA DEL SISTEMA: Borra el texto viejo de la pantalla para crear 
    # un efecto de animación. Usa 'cls' en Windows y 'clear' en Mac/Linux.
    
    print(f'--- TURNO {turnos_jugados + 1} ---')
    # Imprime en la pantalla qué turno es. Le suma 1 solo para que nosotros lo leamos mejor (Turno 1).
    
    # --- 1. Turno del Gato (Inteligente) ---
    pos_gato = mover_gato_inteligente(tablero, pos_gato, pos_raton)
    # El gato ejecuta su paso maestro y sobrescribimos su posición con la nueva coordenada.
    
    if pos_gato == pos_raton:
        # CONDICIONANTE DE VICTORIA: Inmediatamente después de moverse, pregunta si chocaron.
        actualizar_tablero(tablero, pos_gato, pos_raton)
        mostrar_mapa(tablero) # Dibuja la escena del crimen.
        print("¡GAME OVER! El gato atrapó al astuto ratón.")
        break 
        # BOTÓN DE PÁNICO: 'break' destruye el bucle 'while'. El motor se apaga y el juego termina.
        
    # --- 2. Turno del Ratón (Aleatorio) ---
    pos_raton = mover_raton_al_azar(tablero, pos_raton)
    # Si el gato no lo atrapó, el ratón tira los dados, da un paso asustado y se actualiza su posición.
    
    if pos_gato == pos_raton:
        # CONDICIONANTE DE SUICIDIO: Preguntamos si el ratón saltó directo a la boca del gato por error.
        actualizar_tablero(tablero, pos_gato, pos_raton)
        mostrar_mapa(tablero)
        print("¡GAME OVER! El ratón caminó directo hacia el gato.")
        break
        # BOTÓN DE PÁNICO: Destruye el bucle 'while'.

    # --- 3. Dibujar y esperar ---
    actualizar_tablero(tablero, pos_gato, pos_raton)
    mostrar_mapa(tablero)
    # Si nadie murió, pintamos el mapa y lo mostramos en la pantalla para ver el progreso.
    
    time.sleep(0.5)
    # PAUSA DE TIEMPO: Congela la computadora por medio segundo para que nuestros 
    # ojos humanos puedan ver el movimiento. Sin esto, el juego terminaría en 1 milisegundo.
    
    turnos_jugados = turnos_jugados + 1
    # ACTUALIZAR EL RELOJ: Toma el turno actual, le suma 1, y lo guarda. 
    # Cuando llegue a 20, el 'while' de arriba se detendrá solo.

# =========================================================================
# EL FINAL DEL JUEGO (SI EL RATÓN SOBREVIVE)
# =========================================================================

if turnos_jugados == max_turnos:
    # CONDICIÓN FINAL: Si el bucle terminó de forma natural (llegó a 20 sin que un 'break' lo rompiera).
    print("¡EL RATÓN ESCAPÓ! Sobrevivió los 20 turnos.")
    # Imprime el mensaje de victoria del ratón. ¡El programa finaliza!