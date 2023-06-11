import math

import numpy as np
from sty import Style, RgbFg
from sty import fg, bg, ef, rs

#pesos de mi función booleana
t1 = (-1, -1, -1, 1)
t2 = (-1, 1, -1, -1)
t3 = (1, -1, 0, -1)
t4 = (-1, -1, 1, 1)
    
def tuplas(tupla):
    a = tupla[0]
    b = tupla[1]
    c = tupla[2]
    d = tupla[3]

    devolver = ((not a) and (not b) and (not c) and d) or ((not a) and b and (not c) and (not d)) or( a and (not b) and (not d)) or ((not a) and (not b) and c and d)

    return devolver

    
def sig(z):
    sig = 1/(1 + math.exp(-z))
    return sig

def forward(entrada):
    entrada_array = np.asarray(entrada)
   
    w1 = -0.5
    T1 = sig(w1 + np.sum((entrada_array*np.asarray(t1))))
    #print(f"T1: {T1}")
    
    w2 = -0.5
    T2 = sig(w2 + np.sum((entrada_array*np.asarray(t2))))
    #print(f"T2: {T2}")
    
    w3 = -0.4
    T3 = sig(w3 + np.sum((entrada_array*np.asarray(t3))))
    #print(f"T3: {T3}")
    
    w4 = -1.2
    T4 = sig(w4 + np.sum((entrada_array*np.asarray(t4))))
    #print(f"T4: {T4}")

    wf = -0.5
    f = sig(wf + np.sum(np.asarray((T1, T2, T3, T4)) * np.asarray((w1, w2, w3, w4))))
    return f#valor entero

#lalmar forward para las tuplas
'''def llamarForw():
    for i in range (15):
        m = format(i, '04b')
        print(bg.blue + f"{int(m[0])} {int(m[1])} {int(m[2])} {int(m[3])}" + bg.rs)
        print(f"f: {forward((int(m[0]), int(m[1]), int(m[2]), int(m[3])))} ")
        print("\n")
   
'''

VECTOR_BITS = []
VECTOR_SALIDA = []
#lalmar forward para las tuplas
def llamarTuplas():
    global VECTOR_BITS
    global VECTOR_SALIDA
    
    for i in range (16):
        m = format(i, '04b')
        print(bg.blue + f"{int(m[0])} {int(m[1])} {int(m[2])} {int(m[3])}" + bg.rs)
        #print(f"tuplas: {tuplas((int(m[0]), int(m[1]), int(m[2]), int(m[3])))} ")
        
        #print(f"f: {forward((int(m[0]), int(m[1]), int(m[2]), int(m[3])))} ")
        print(forward((int(m[0]), int(m[1]), int(m[2]), int(m[3]))))


###################### PARTE 2 ##################
from tensorflow import keras
from tensorflow.keras import layers

'''model = keras.Seuential (
    [
        keras.Input(shape=(?)),
        layers.Dense(?,activation="sigmoid"),
     ]  
)
'''

def main():
    #llamarForw()
    llamarTuplas()

    
if __name__ == "__main__":
    main()