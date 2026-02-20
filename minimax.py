import random
import os
import time

gato = 'G'
raton = 'R'

def crear_mapa(alto, ancho):
    mapa = []
    for piso in range(alto):
        fila = ['.'] * ancho
        mapa.append(fila)
    return mapa 

def mostrar_mapa(tablero):
    for fila in tablero:
        print(' '.join(fila))


def movimientos_permitidos(mapa, y, x):
    alto = len(mapa)
    ancho = len(mapa[0])
    if 0 <= y < alto and 0 <= x < ancho:
        return True
    else:
        return False

def obtener_movimientos_posibles(mapa, y, x):
    movimientos = []
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dy, dx in direcciones:
        nueva_y = y + dy
        nueva_x = x + dx
        if movimientos_permitidos(mapa, nueva_y, nueva_x):
            movimientos.append([nueva_y, nueva_x])
    return movimientos

def actualizar_tablero(tablero, pos_gato, pos_raton):
    for filas in range(len(tablero)):
        for columnas in range(len(tablero[0])):
            tablero[filas][columnas] = '.'
            
    tablero[pos_gato[0]][pos_gato[1]] = gato
    tablero[pos_raton[0]][pos_raton[1]] = raton

def mover_raton_al_azar(tablero, pos_raton):
    opciones = obtener_movimientos_posibles(tablero, pos_raton[0], pos_raton[1])
    if len(opciones) > 0:
        nueva_pos = random.choice(opciones)
        pos_raton = nueva_pos
    return pos_raton

# --- LA INTELIGENCIA DEL GATO (NUEVO) ---

def calcular_distancia(y1, x1, y2, x2):
    # Calcula cuántos pasos hay entre dos puntos usando matemática básica
    distancia_y = abs(y1 - y2)
    distancia_x = abs(x1 - x2)
    return distancia_y + distancia_x

def minimax(mapa, pos_gato_simulada, pos_raton_simulada, profundidad, es_turno_gato):
    # 1. Condiciones para dejar de imaginar el futuro
    if pos_gato_simulada == pos_raton_simulada:
        return 1000  # El gato gana, puntaje máximo
        
    if profundidad == 0:
        # Si ya pensó muchos pasos adelante, evalúa qué tan cerca está
        distancia = calcular_distancia(pos_gato_simulada[0], pos_gato_simulada[1], pos_raton_simulada[0], pos_raton_simulada[1])
        # Queremos que la distancia sea pequeña, así que le ponemos un signo menos (ej: -2 es mejor que -10)
        return -distancia 

    # 2. El turno del Gato (Maximizar su puntaje)
    if es_turno_gato == True:
        mejor_puntaje = -9999 # Un número muy bajo para empezar
        opciones = obtener_movimientos_posibles(mapa, pos_gato_simulada[0], pos_gato_simulada[1])
        
        for opcion in opciones:
            puntaje = minimax(mapa, opcion, pos_raton_simulada, profundidad - 1, False)
            if puntaje > mejor_puntaje:
                mejor_puntaje = puntaje
        return mejor_puntaje

    # 3. El turno del Ratón (Minimizar el puntaje del gato escapando)
    else:
        peor_puntaje = 9999 # Un número muy alto para empezar
        opciones = obtener_movimientos_posibles(mapa, pos_raton_simulada[0], pos_raton_simulada[1])
        
        for opcion in opciones:
            puntaje = minimax(mapa, pos_gato_simulada, opcion, profundidad - 1, True)
            if puntaje < peor_puntaje:
                peor_puntaje = puntaje
        return peor_puntaje

def mover_gato_inteligente(mapa, pos_gato, pos_raton):
    mejor_puntaje = -9999
    mejor_movimiento = pos_gato
    opciones = obtener_movimientos_posibles(mapa, pos_gato[0], pos_gato[1])
    
    for opcion in opciones:
        # El gato simula qué pasaría si hace este movimiento (mirando 3 pasos al futuro)
        puntaje = minimax(mapa, opcion, pos_raton, 3, False)
        if puntaje > mejor_puntaje:
            mejor_puntaje = puntaje
            mejor_movimiento = opcion
            
    return mejor_movimiento

# --- INICIO DEL JUEGO: EL LABERINTO ---

tablero = crear_mapa(8, 8)
pos_gato = [0, 0]
pos_raton = [7, 7]

turnos_jugados = 0
max_turnos = 20 # Condición de finalización

actualizar_tablero(tablero, pos_gato, pos_raton)

# Bucle principal del juego
while turnos_jugados < max_turnos:
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'--- TURNO {turnos_jugados + 1} ---')
    
    # 1. Turno del Gato (Inteligente)
    pos_gato = mover_gato_inteligente(tablero, pos_gato, pos_raton)
    
    # Comprobamos si el gato atrapó al ratón antes de que el ratón huya
    if pos_gato == pos_raton:
        actualizar_tablero(tablero, pos_gato, pos_raton)
        mostrar_mapa(tablero)
        print("¡GAME OVER! El gato atrapó al astuto ratón.")
        break # Termina el bucle
        
    # 2. Turno del Ratón (Aleatorio)
    pos_raton = mover_raton_al_azar(tablero, pos_raton)
    
    # Comprobamos si el ratón se suicidó chocando con el gato
    if pos_gato == pos_raton:
        actualizar_tablero(tablero, pos_gato, pos_raton)
        mostrar_mapa(tablero)
        print("¡GAME OVER! El ratón caminó directo hacia el gato.")
        break

    # 3. Dibujar y esperar
    actualizar_tablero(tablero, pos_gato, pos_raton)
    mostrar_mapa(tablero)
    time.sleep(0.5)
    
    turnos_jugados = turnos_jugados + 1

# Si el bucle termina porque se acabaron los turnos
if turnos_jugados == max_turnos:
    print("¡EL RATÓN ESCAPÓ! Sobrevivió los 20 turnos.")