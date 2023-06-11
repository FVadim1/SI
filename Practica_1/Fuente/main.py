import sys, pygame
from turtle import position
from tablero import *
from algoritmo import *
from pygame.locals import *
import time

import globals

#import sys
#sys.stdout = open('output.txt','wt')

MARGEN=20
ROJO=(255, 0, 0)
AZUL=(0, 0, 255)
AMARILLO=(255, 255, 0)
NEGRO=(0,0,0)
BLANCO=(255, 255, 255)
TAM=60

PROFUNDIDAD_MINIMAX = 3
PROFUNDIDAD_ALFABETA = 3

def main():
    pygame.init() 
    
    reloj=pygame.time.Clock()
    screen=pygame.display.set_mode([700, 620])
    pygame.display.set_caption("Practica 1")
    
    game_over=False
    tablero=Tablero(None)
    col=-1
    once = True
    
    once_columna = False
    
    while not game_over:
        for event in pygame.event.get(): 
            if event.type==pygame.QUIT:             
                game_over=True
            
            if globals.JUGADOR_VS_MAQUINA == True: # JUGADOR VS MAQUINA
                if event.type==pygame.MOUSEBUTTONDOWN:                
                    pos=pygame.mouse.get_pos()  
                    colDestino=(pos[0]-(2*MARGEN))//(TAM+MARGEN)             
                    #comprobar que es una posición válida
                    fila=buscaPrimeraVacia(tablero, colDestino)
                    if fila!=-1: #Si donde he hecho click está vacío setteo la celda                   
                        tablero.setCelda(fila, colDestino, 1)
                    if tablero.cuatroEnRaya()==1: #Compruebo si he ganado
                        game_over=True
                        print ("gana persona")
                        print('\033[91m' + 'Tablero Ganador persona:' + '\033[0m')
                        print(tablero)               
                    else: 
                        #Para el añadido de la memoria de que sean diferentes si tienen misma puntuación
                        if globals.MEMORIA_DIFERENTES:
                            globals.COLUMNAS_IGUALES.clear()
                        
                        #col,row,minimax_score = miniMax(tablero,PROFUNDIDAD_MINIMAX,True) #Descomentar esto para que sea minimax
                        col,row,minimax_score =  AlfaBeta(tablero,PROFUNDIDAD_ALFABETA,True, -math.inf, math.inf) 

                        tablero.setCelda(row,col,2)   
                
                        if tablero.cuatroEnRaya()==2:
                            game_over=True
                            print ("gana maquina")
                            print('\033[91m' + 'Tablero Ganador maquina:' + '\033[0m')
                            print(tablero)
                        print("entro")
        
        if globals.JUGADOR_VS_MAQUINA == False:     
            if once: #para que se dibuje el mapa al principio
                once = False
                dibujarTablero(tablero,reloj,screen)

            #col1,row1,minimax_score1 =  AlfaBeta(tablero,3,True, -math.inf, math.inf) 
            col1,row1,minimax_score2 =  miniMax(tablero,3,True)
            
            #PARA TESTEO COLOCANDO EN COLUMNAS SUCESIVAS
            if once_columna:
                tablero.setCelda(6, 7, 1)
                once_columna = False
            else:
                tablero.setCelda(row1, col1, 1)
            
            print(tablero)
            if tablero.cuatroEnRaya()==1: #Compruebo si he ganado
                game_over=True
                print ("gana maquina 1")
                print('\033[91m' + 'Tablero Ganador maquina 1:' + '\033[0m')
                print(tablero)
            else:
                pygame.time.wait(100)
                #col2,row2,minimax_score2 =  miniMax(tablero,PROFUNDIDAD_ALFABETA,True)
                col2,row2,minimax_score2 =  AlfaBeta(tablero,3,True, -math.inf, math.inf) 

                tablero.setCelda(row2, col2, 2)
                print(tablero)
                if tablero.cuatroEnRaya()==2: #Compruebo si he ganado
                    game_over=True
                    print ("gana maquina 2")
                    print('\033[91m' + 'Tablero Ganador maquina 2:' + '\033[0m')
                    print(tablero)   
        
        #código de dibujo        
        #limpiar pantalla
        dibujarTablero(tablero,reloj,screen)
        
        if game_over==True: #retardo cuando gana
            pygame.time.delay(3500)
    
    pygame.quit()
 
 
def dibujarTablero(tablero,reloj,screen):
    screen.fill(NEGRO)
    pygame.draw.rect(screen, AZUL, [MARGEN, MARGEN, 660, 580],0)
    for fil in range(tablero.getAlto()):
        for col in range(tablero.getAncho()):
            if tablero.getCelda(fil, col)==0: 
                pygame.draw.ellipse(screen, BLANCO, [(TAM+MARGEN)*col+2*MARGEN, (TAM+MARGEN)*fil+2*MARGEN, TAM, TAM], 0)
            elif tablero.getCelda(fil, col)==1: 
                pygame.draw.ellipse(screen, ROJO, [(TAM+MARGEN)*col+2*MARGEN, (TAM+MARGEN)*fil+2*MARGEN, TAM, TAM], 0)
            else:
                pygame.draw.ellipse(screen, AMARILLO, [(TAM+MARGEN)*col+2*MARGEN, (TAM+MARGEN)*fil+2*MARGEN, TAM, TAM], 0)                
                    
    for col in range(tablero.getAncho()):
        pygame.draw.rect(screen, BLANCO, [(TAM+MARGEN)*col+2*MARGEN, 10, TAM, 10],0)
        
    #actualizar pantalla
    pygame.display.flip()
    reloj.tick(40)
 
 
if __name__=="__main__":
    
    main()
 
