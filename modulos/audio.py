
from main import np,signal,plt,graficar
import others #me tira error si importo others desde main. Aun no lo solucioné

"""
    Este modulo contiene funciones referidas al manejo de informacion en forma de audio.
    
"""

def leq(data,fs,len):
    """
    Calcula el NPS equivalente relativo a un audio en dB SPL.

    Args:
        data (array): señal en dB
        fs (int): frecuencia de muestreo
        len (float): _description_

    Returns:
        float: NPS equivalente relativo a un audio en Pa
    """
    pre_sum_valores=10**(data/10)
    pre_sum_valor=np.sum(pre_sum_valores)    
    return 10*np.log10(pre_sum_valor*(1/((fs*len))))


def pa_to_nps(señal_Pa):
    """Convierte señal de audio en Pa hacia NPS

    Args:
        senal_Pa (1darray): señal en Pa a convertir a NPS

    Returns:
        1darray: señal original con unidades de NPS
    """
    min_valor = np.finfo(float).eps

    señal_Pa_cuadrado=señal_Pa**2

    sin_ceros=np.where(señal_Pa_cuadrado == 0,min_valor,señal_Pa_cuadrado)
    
    return (10*np.log10(((sin_ceros/(20e-6**2)))))


def bandas_pa_to_nps(bandas_pa):
    """
    convierte bandas de octava o tercio de octava desde Pa hacia dB SPL

    Args:
        bandas_pa (ndarray): arreglo en donde cada elemento es un 
                                    arreglo que contiene una señal correspondiente
                                     a una banda de octava o tercio 
                                    de octava en Pa. Ej: 

    Returns:
        ndarray: devuelve el mismo tipo de dato de entrada pero convertido en dB SPL
    """
    octavas_db=np.empty(np.shape(bandas_pa))

    contador=0
    for banda_pa in bandas_pa:
        banda_db=pa_to_nps(banda_pa)
        octavas_db[contador]=banda_db
        contador+=1
    
    return octavas_db

def filtro_norma(fs,audiodata,octava=1,orden_filtro=4,visualizar_data=False):
    
    """
    Banco de filtros segun la norma 61260

    Args:
        fs (int): Frecuencia de muestreo de señal
        audiodata (array): señal a filtrar en Pa
        octava (int, optional): Fraccion de octava. 1 para octavas completas.
                                                    3 para tercios de octava. 
                                                    Defaults to 1.
        orden_filtro (int, optional): orden de filtro a generar. Mayor que 4 Defaults to 12.
        visualizar_data (bool, optional): Visualiza datos referentes a los filtros generados. Defaults to False.

    Returns:
        ndarray: arreglo en donde cada posicion es un arreglo conteniendo los valores
                de las fracciones de octavas filtradas en Pa
        
        array: etiquetas de fracciones de octava (Ej: 25,50,100,200,400,800,etc...) 
    """
    
    
    min_valor = np.finfo(float).eps
    plt.figure(figsize = (12, 5))
 
    if others.validar_fraccion_octava==False :
        print("Error en la seleccion de fraccion de octava. Valores: 1 ó 3.")
        return
    
    if octava==3:
        G=1.0/6.0
        factor = np.power(2, G)
        
        fc=np.array([ 25, 31.5, 40, 50, 63, 80, 100, 125, 160, 200,250,
         315 , 400 , 500 , 630 , 800 , 1000 , 1250 , 1600 , 2000 , 2500 ,
         3150 , 4000 , 5000 , 6300 , 8000 , 10000 , 12500 , 
         16000 , 20000 ],dtype=float)
        
        x_nombres=["25","31.5","40","50","63","80",
                           "100","125","160","200","250","315","400",
                           "500","630","800","1k","1.25k","1.6k",
                           "2k","2.5k","3.15k","4k","5k","6.3k","8k",
                           "10k","12.5k","16k","20k"]
        
        n_de_bandas=30
        
    elif octava == 1:
        G = 1.0/2.0
        factor = np.power(2, G)
        fc=np.array([31.25,62.5,125,250,500,1000,2000,4000,8000,16000],dtype=float)
        x_nombres=fc
        n_de_bandas=10
        
    
    else:
        print("Error en la fraccion de octava. Debe ser 1 ó 3.")
        return 
    
       

    coeficientes= np.zeros((n_de_bandas,orden_filtro,6))
    f_sup=np.arange(0,n_de_bandas)
    f_inf=np.arange(0,n_de_bandas)
    for i,f in enumerate(fc):
        
        f_sup=f*factor
        f_inf=f/factor
        wc = ([f_inf / (0.5*fs), f_sup / (0.5*fs)])
    
        sos = signal.butter(orden_filtro, Wn=wc, btype='bandpass',output="sos")
        freq, z = signal.sosfreqz(sos,worN=2*4096,fs=fs)

        if visualizar_data == True:
            abs_vals=np.absolute(z)
            sin_ceros=np.where(abs_vals == 0,min_valor,abs_vals)
        
            plt.semilogx(freq,20*np.log10(sin_ceros))
        
            if f==1000:
                octava_particular = sin_ceros
                f_inf_particular=f_inf
                f_sup_particular=f_sup
        
        
        coeficientes[i,:,:]=sos
    

    if visualizar_data==True:
        graficar.visualizar_banco_filtros(fc,x_nombres,freq,octava_particular,f_inf_particular,f_sup_particular,octava,1000)
        
    
    
    #preparo el audio para filtrarse:
    audiodata = audiodata.astype(np.float32, order='C') 
    audiodata_filtrada = np.zeros(((n_de_bandas,len(audiodata))))
    
    #se filtran los audios
    for i,f in enumerate(fc):
        audiodata_filtrada[i,:] = signal.sosfilt(coeficientes[i,:,:], audiodata)
        audiodata_filtrada[i,:] = audiodata_filtrada[i,:].astype(np.float32, order='C')

    octavas_filtradas=np.zeros(np.shape(audiodata_filtrada),np.float32)
    for i in range (0,n_de_bandas):
        octavas_filtradas[i]=audiodata_filtrada[i,:]
        

    return octavas_filtradas , fc



def bandas_pa_a_nps(octavas,cal):
    """Convierte bandas en pascales a nps.

    Args:
        octavas (ndarray): ndarray, array en donde cada posicion es un array conteniendo los valores
                           de las fracciones de octavas filtradas en Pa
        cal (array): audio referente al calibrador. 1Pa ó 94dB SPL

    Returns:
        ndarray: octavas convertidas a nps
    """
    octavas_db=np.empty(np.shape(octavas))

    contador=0
    for banda in octavas:
        banda_db=pa_to_nps(banda,cal)
        octavas_db[contador]=banda_db
        contador+=1
    
    return octavas_db

def bandas_a_leq(octavas_db,fs,len,fraccion_octava=1):
    """convierte bandas de NPS a Pa

    Args:
        octavas_db (ndarray): contenedor de octavas
        fs (int): frecuencia de muestreo en Hz
        len (float): longitud de audio original en segundos.
        fraccion_octava (int, optional): Fraccion de octava. 1 para octavas completas.
                                                             3 para tercios de octava. 
                                                             Defaults to 1.

    Returns:
        1d array: array conteniendo los valores de NPS equivalente por octava
    """
    
    if others.validar_fraccion_octava==False :
        print("Error en la seleccion de fraccion de octava. Valores: 1 ó 3.")
        return
    
    n_de_bandas=fraccion_octava*10
    
    bandas_leq=np.zeros([n_de_bandas,])
    
    contador=0
    for bandas in octavas_db:
        leq_banda=leq(bandas,fs,len)
        bandas_leq[contador]=leq_banda
        contador+=1
        
    return bandas_leq



def raw_to_pa(raw,cal):
    """Convierte señal de audio cruda hacia Pa

    Args:
        raw (1darray): señal cruda
        cal (1darray): señal de calibrador referido a 1 Pa

    Returns:
        1darray: señal original en Pa
    """

    valor_rms=np.sqrt(np.mean(cal**2))
    señal_Pa=raw/valor_rms
    return señal_Pa

def normalizar_señal(señal):
    """normaliza una señal segun su maximo valor absoluto
    Args:
        señal (1darray): señal original

    Returns:
        1darray: señal original pero con valores de amplitud que oscilan entre -1 y 1
    """
    return señal/np.max(np.abs(señal))