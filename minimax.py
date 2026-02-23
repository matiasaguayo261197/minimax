import random  # Para que el ratón tome decisiones al azar.
import os      # Para limpiar la pantalla de la consola.
import time    # Para pausar el juego y que podamos ver la animación.

gato = 'G'     
raton = 'R'   

def crear_mapa(alto, ancho):
    # Crea una lista vacía y la llena de filas con puntos '.'
    mapa = [] 
    for piso in range(alto):
        fila = ['.'] * ancho
        mapa.append(fila)
    return mapa 

def mostrar_mapa(tablero):
    # Imprime el tablero en la pantalla, uniendo los puntos con espacios.
    for fila in tablero:
        print(' '.join(fila))

def actualizar_tablero(tablero, pos_gato, pos_raton):
    # Borra todo dibujando '.' y luego pinta al Gato y al Ratón en sus coordenadas.
    for filas in range(len(tablero)):
        for columnas in range(len(tablero[0])):
            tablero[filas][columnas] = '.'
            
    tablero[pos_gato[0]][pos_gato[1]] = gato
    tablero[pos_raton[0]][pos_raton[1]] = raton


def movimientos_permitidos(tablero, y, x):
    # El guardia: Verifica que las coordenadas no se salgan del mapa (menores a 0 o mayores al límite).
    alto = len(tablero)
    ancho = len(tablero[0])
    if 0 <= y < alto and 0 <= x < ancho:
        return True
    else:
        return False


def obtener_movimientos_posibles(tablero, y, x):
    # La brújula: Revisa Arriba, Abajo, Izquierda, Derecha y devuelve solo los pasos autorizados por el guardia.
    movimientos = []
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dy, dx in direcciones:
        nueva_y = y + dy
        nueva_x = x + dx
        if movimientos_permitidos(tablero, nueva_y, nueva_x):
            movimientos.append([nueva_y, nueva_x])
    return movimientos


def calcular_distancia(y1, x1, y2, x2):
    # El radar (Distancia Manhattan): Suma los pasos verticales y horizontales entre dos puntos.
    distancia_y = abs(y1 - y2)
    distancia_x = abs(x1 - x2)
    return distancia_y + distancia_x


def minimax(mapa, pos_gato_simulada, pos_raton_simulada, profundidad, es_turno_gato):
    # EL CEREBRO: La máquina que imagina futuros mediante recursividad.
    
    if pos_gato_simulada == pos_raton_simulada:
        return 1000  
        
    if profundidad == 0:
        distancia = calcular_distancia(pos_gato_simulada[0], pos_gato_simulada[1], pos_raton_simulada[0], pos_raton_simulada[1])
        return -distancia 


    if es_turno_gato == True:
        mejor_puntaje = -9999 
        opciones = obtener_movimientos_posibles(mapa, pos_gato_simulada[0], pos_gato_simulada[1])
        
        for opcion in opciones:
            puntaje = minimax(mapa, opcion, pos_raton_simulada, profundidad - 1, False)
            if puntaje > mejor_puntaje:
                mejor_puntaje = puntaje
        return mejor_puntaje

    else:
        peor_puntaje = 9999 
        opciones = obtener_movimientos_posibles(mapa, pos_raton_simulada[0], pos_raton_simulada[1])
        
        for opcion in opciones:
            puntaje = minimax(mapa, pos_gato_simulada, opcion, profundidad - 1, True)
            if puntaje < peor_puntaje:
                peor_puntaje = puntaje
        return peor_puntaje

def mover_raton_al_azar(tablero, pos_raton):
    # El ratón elige una opción de escape al azar 
    opciones = obtener_movimientos_posibles(tablero, pos_raton[0], pos_raton[1])
    if len(opciones) > 0:
        nueva_pos = random.choice(opciones)
        pos_raton = nueva_pos
    return pos_raton

def mover_gato_inteligente(tablero, pos_gato, pos_raton):
    # El gato evalúa el mundo real, consulta a su cerebro 3 turnos al futuro, y da el paso ganador.
    mejor_puntaje = -9999
    mejor_movimiento = pos_gato
    opciones = obtener_movimientos_posibles(tablero, pos_gato[0], pos_gato[1])
    
    for opcion in opciones:
        puntaje = minimax(tablero, opcion, pos_raton, 3, False)
        if puntaje > mejor_puntaje:
            mejor_puntaje = puntaje
            mejor_movimiento = opcion
            
    return mejor_movimiento


tablero = crear_mapa(8, 8)
pos_gato = [0, 0]
pos_raton = [7, 7]

turnos_jugados = 0
max_turnos = 20 

actualizar_tablero(tablero, pos_gato, pos_raton)

while turnos_jugados < max_turnos:
    # Limpia la consola para crear el efecto de animación.
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'--- TURNO {turnos_jugados + 1} ---')
    
    # 1. El Gato toma su turno
    pos_gato = mover_gato_inteligente(tablero, pos_gato, pos_raton)
    
    # Verifica victoria del Gato
    if pos_gato == pos_raton:
        actualizar_tablero(tablero, pos_gato, pos_raton)
        mostrar_mapa(tablero)
        print("¡GAME OVER! El gato atrapó al astuto ratón.")
        break 
        
    # 2. El Ratón toma su turno
    pos_raton = mover_raton_al_azar(tablero, pos_raton)
    
    # Verifica si el ratón chocó por accidente
    if pos_gato == pos_raton:
        actualizar_tablero(tablero, pos_gato, pos_raton)
        mostrar_mapa(tablero)
        print("¡GAME OVER! El ratón caminó directo hacia el gato.")
        break

    # 3. Renderiza el turno y espera medio segundo
    actualizar_tablero(tablero, pos_gato, pos_raton)
    mostrar_mapa(tablero)
    time.sleep(0.5)
    
    turnos_jugados = turnos_jugados + 1

# Si sale del bucle intacto, el ratón gana.
if turnos_jugados == max_turnos:
    print("¡EL RATÓN ESCAPÓ! Sobrevivió los 20 turnos.")