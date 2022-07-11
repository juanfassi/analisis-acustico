from main import np


"""
    Este modulo contiene funciones que nos quedaron sueltas.
    
"""

def find_nearest(array, value):
    """Busca el valor mas cercano de un array dado un valor

    Args:
        array (array): valores objetivo
        value (float): valor de entrada

    Returns:
        float: valor del arreglo "array" mas cercano a "value" 
    """
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]


def reemplazar_ceros(values):
    """Reemplaza los ceros de un arreglo por el minimo valor representado por un float

    Args:
        values (array): arreglo a analizar

    Returns:
        array: copia del arreglo origianal pero con ceros reemplazados
    """
    min_valor = np.finfo(float).eps
    for x in values:
        if x==0:
            x=min_valor
        
    return values


def validar_fraccion_octava(fraccion_octava):
    """Verifica si un entero es igual a 1 o 3. .

    Args:
        fraccion_octava (int): numero entero

    Returns:
        bool: True si el valor ingresado es 1 ó 3. False si es cualquier otro valor
    """
    if fraccion_octava!= 1 and fraccion_octava!=3 : return False
    else : return True
    
def sumar_senoidales(frecuencias,fs,duracion):
    """
    Devuelve el resultado de la suma de n funciones senoidales donde n es la cantidad de frecuncias que se coloquen en el primer arg
    
        Parámetros de entrada:
            frecuencias(array): Frecuencias de las diferentes funciones senoidales
            fs(float): Frecuencia de muestreo
            duracion(float): Duración (en segundos) de la señal

        Parámetros de salida:
            suma(array): Resultado de la suma de amplitud de las señales
            t(array): eje temporal
    """
    suma = np.zeros(duracion*fs,dtype=float)
    t=np.linspace(0,duracion,duracion*fs)
    
    for f in frecuencias:
        suma+=np.sin(2*np.pi*f*t)
    
    return suma,t    