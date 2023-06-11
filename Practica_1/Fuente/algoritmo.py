import globals

import time

import math
import random
import copy
from auxiliares import *
from string import punctuation

from tablero import Tablero

#Evaluo la selección de 4 casillas que le envio por parámetros y le doy una puntuación acorde
def evaluar_seleccion(seleccion,pieza):
    
    puntuacion = 0
    if seleccion.count(pieza) == 4:#si hay 4 del mismo valor que la pieza (1 (jugador) o 2 (IA) dependiendo de quien utiliza la funcion)
        puntuacion += 100
    elif seleccion.count(pieza) == 3 and seleccion.count(0) == 1: #si hay 3 piezas y 1 es vacío
        puntuacion += 10
    elif seleccion.count(pieza) == 2 and seleccion.count(0) == 2: #si hay 2 piezas y 1 es vacío
        puntuacion += 5

    # pieza_del_oponente es el adversario del que entre en esta función
    pieza_del_oponente = PIEZA_JUGADOR
    if pieza == PIEZA_JUGADOR:
        pieza_del_oponente = PIEZA_AI
    if seleccion.count(pieza_del_oponente) == 3 and seleccion.count(0) == 1:
        puntuacion -= 75
    
    return puntuacion

#funcion que nos da una puntuacion dependiendo de cuantas piezas del mismo valor hay seguidas
def verPuntuacion_de_este_tablero(tablero,pieza): # 1 = jugador , 2 = IA
    puntuacion = 0

    #PREFERENCIA POR EL CENTRO
    columna_centro = tablero.getAncho()//2
    filas_de_la_columna_del_centro = getColumnaCompleta(tablero,columna_centro)
    piezas_centro = filas_de_la_columna_del_centro.count(pieza) #cantidad de estas piezas iguales en la columna del centro
    puntuacion += piezas_centro * 6

    #HORIZONTAL
    for r in range(tablero.getAlto()):
        fila_array = getFilaCompleta(tablero,r) 
        for c in range(tablero.getAncho() - 3): # el "-3" es porque lo último que voy a procesar son los últimos 4 de esa fila
            seleccion = fila_array[c:c+4] #selecciono 4 de esa fila
            puntuacion += evaluar_seleccion(seleccion,pieza)
    
    #VERTICAL
    for c in range(tablero.getAncho()):
        col_array = getColumnaCompleta(tablero,c) 
        for r in range(tablero.getAlto() - 3): 
            seleccion = col_array[r:r+4] #selecciono 4 de esa columna
            puntuacion += evaluar_seleccion(seleccion,pieza)
    #DIAGONAL POSITIVO
    for r in range(tablero.getAlto() - 3):
        for c in range(tablero.getAncho() - 3):
            seleccion = [tablero.getCelda(r+i,c+i) for i in range(4)] 
            puntuacion += evaluar_seleccion(seleccion,pieza)
    #DIAGONAL NEGATIVO
    for r in range(tablero.getAlto() - 3):
        for c in range(tablero.getAncho() - 3):
            seleccion = [tablero.getCelda(r+3-i,c+i) for i in range(4)] 
            puntuacion += evaluar_seleccion(seleccion,pieza)

    return puntuacion

def miniMax(tablero, profundidad, maximizingPlayer): 
    
    columnasSinLlenar = obtenerColumnasSinLlenar(tablero)
    esTerminal = esNodoTerminal(tablero)
    
    if profundidad == 0 or esTerminal:
        if esTerminal:
            if tablero.cuatroEnRaya() == PIEZA_AI:
                return (None,None,1000000)
            elif tablero.cuatroEnRaya() == PIEZA_JUGADOR: 
                return (None,None,-1000000)
            else:
                return (None,None,0) #juego acabado, no hay más pasos posibles
        else:
            return (None,None,verPuntuacion_de_este_tablero(tablero,PIEZA_AI))

    if maximizingPlayer:
        value = -math.inf
        mejorColumna = random.choice(columnasSinLlenar)
        mejorFila = getPrimerCeroEnlaColumna(tablero,mejorColumna)

        for col in columnasSinLlenar:

            fila = getPrimerCeroEnlaColumna(tablero,col)
            aux_tablero = Tablero(tablero)
            aux_tablero.setCelda(fila,col,PIEZA_AI) #fila,col,pieza
            nueva_puntuacion = miniMax(aux_tablero,profundidad-1,False)[2]

            if nueva_puntuacion >= value:
                value = nueva_puntuacion
                mejorColumna = col
                mejorFila = fila
                if globals.MEMORIA_DIFERENTES:   
                    globals.COLUMNAS_IGUALES.append(col)
            else:
                if globals.MEMORIA_DIFERENTES:   
                    if nueva_puntuacion == value:
                        globals.COLUMNAS_IGUALES.append(col)
         
            if globals.MEMORIA_DIFERENTES:       
                if len(globals.COLUMNAS_IGUALES) > 1: 
                    mejorColumna = random.choice(globals.COLUMNAS_IGUALES)
                    mejorFila = getPrimerCeroEnlaColumna(tablero,mejorColumna)
                    globals.COLUMNAS_IGUALES.clear()
   
        return mejorColumna,mejorFila,value
    else: #minimizingPlayer
        value = math.inf
        mejorColumna = random.choice(columnasSinLlenar)
        mejorFila = getPrimerCeroEnlaColumna(tablero,mejorColumna)
        
        for col in columnasSinLlenar:
            fila = getPrimerCeroEnlaColumna(tablero,col)
            aux_tablero = Tablero(tablero)
            aux_tablero.setCelda(fila,col,PIEZA_JUGADOR) 
            nueva_puntuacion = miniMax(aux_tablero,profundidad-1,True)[2]

            if nueva_puntuacion < value:
                value = nueva_puntuacion
                mejorColumna = col
                mejorFila = fila
                if globals.MEMORIA_DIFERENTES:   
                    globals.COLUMNAS_IGUALES.append(col)
            else: #Implementación opcional memoria
                if globals.MEMORIA_DIFERENTES:   
                    if nueva_puntuacion == value:
                        globals.COLUMNAS_IGUALES.append(col)
         
            if globals.MEMORIA_DIFERENTES: #Implementación opcional memoria           
                if len(globals.COLUMNAS_IGUALES) > 1: 
                    mejorColumna = random.choice(globals.COLUMNAS_IGUALES)
                    mejorFila = getPrimerCeroEnlaColumna(tablero,mejorColumna)
                    globals.COLUMNAS_IGUALES.clear()
     
        return mejorColumna,mejorFila,value

def AlfaBeta(tablero : Tablero, profundidad, maximizingPlayer, alfa, beta): 
    
    columnasSinLlenar = obtenerColumnasSinLlenar(tablero)
    esTerminal = esNodoTerminal(tablero)

    if profundidad == 0 or esTerminal:
        if esTerminal:
            if tablero.cuatroEnRaya() == PIEZA_AI:
                return (None,None,1000000) 
            elif tablero.cuatroEnRaya() == PIEZA_JUGADOR: 
                return (None,None,-1000000)
            else:
                return (None,None,0) 
        else:
            return (None,None,verPuntuacion_de_este_tablero(tablero,PIEZA_AI))
    
    if maximizingPlayer:
        value = -math.inf
        mejorColumna = random.choice(columnasSinLlenar)
        mejorFila = getPrimerCeroEnlaColumna(tablero,mejorColumna)
        
        for col in columnasSinLlenar: 
            
            fila = getPrimerCeroEnlaColumna(tablero,col)
            aux_tablero = Tablero(tablero)
            aux_tablero.setCelda(fila,col,PIEZA_AI)
            nueva_puntuacion = AlfaBeta(aux_tablero,profundidad-1,False, alfa, beta)[2]

            if nueva_puntuacion > value: 
                value = nueva_puntuacion
                mejorColumna = col
                mejorFila = fila

            # PODA ALFA BETA 
            alfa = max(alfa,value)
            if alfa >= beta:
                break
                  
        return mejorColumna,mejorFila,value
    else: #minimizingPlayer  
        value = math.inf
        mejorColumna = random.choice(columnasSinLlenar)
        mejorFila = getPrimerCeroEnlaColumna(tablero,mejorColumna)
        
        for col in columnasSinLlenar:
            
            fila = getPrimerCeroEnlaColumna(tablero,col)
            aux_tablero = Tablero(tablero)
            aux_tablero.setCelda(fila,col,PIEZA_JUGADOR)
            nueva_puntuacion = AlfaBeta(aux_tablero,profundidad-1,True, alfa, beta)[2]

            if nueva_puntuacion < value:
                value = nueva_puntuacion
                mejorColumna = col
                mejorFila = fila
            
            # PODA ALFA BETA 
            beta = min(beta,value)
            if alfa >= beta:
                break
    
        return mejorColumna,mejorFila,value



