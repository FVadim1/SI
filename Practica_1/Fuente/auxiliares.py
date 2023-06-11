
PIEZA_JUGADOR = 1
PIEZA_AI = 2

#obtiene una fila completa a partir de num_fila
def getFilaCompleta(tablero,num_fila): 
    fila_completa = []
    if num_fila < tablero.getAlto():
        for c in range(tablero.getAncho()):
            fila_completa.append(tablero.getCelda(num_fila,c))
        
    return fila_completa
 
#obtiene una columna completa a partir de num_col   
def getColumnaCompleta(tablero,num_col):
    col_completa = []
    if num_col < tablero.getAncho():
        for r in range(tablero.getAlto()):
            col_completa.append(tablero.getCelda(r,num_col))
        
    return col_completa

#Obtengo todas las columnas sin llenar
def obtenerColumnasSinLlenar(tab): 
    playable_locations = []
    for col in range(tab.getAncho()): #recorro todas las columnas
        if columnaSinLlenar(tab,col):
            playable_locations.append(col)
    return playable_locations

def columnaSinLlenar(tab,col): 
    return tab.getCelda(0, col) == 0

#saca la primera posicion de la columna, más arriba que sea un 0
def getPrimerCeroEnlaColumna(tab,col): #umpoco diferente al del video
    row = tab.getAlto() - 1
    for r in range(tab.getAlto()):
        if tab.getCelda(r,col) != 0:
            row = r-1
            break #sin el break sigue iterando y no da el resultado correcto
    return row

#devuelve TRUE si el siguiente nodo es el nodo ganador o ya no se puede hacer ningun movimiento
def esNodoTerminal(tablero):
    return tablero.cuatroEnRaya() == PIEZA_AI or tablero.cuatroEnRaya() == PIEZA_JUGADOR or len(obtenerColumnasSinLlenar(tablero)) == 0

# busca en col la primera celda vacía
def buscaPrimeraVacia(tablero, col):  
    if tablero.getCelda(0,col) != 0:
        i=-1
    i=0
    while i<tablero.getAlto() and tablero.getCelda(i,col)==0:          
        i=i+1      
    i=i-1
   
    return i