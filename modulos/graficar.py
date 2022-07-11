from main import plt,np
import others

"""
    Este modulo contiene funciones relacionadas a generar graficos.
    
"""

def señal(t,señal,duracion,titulo,x_label,y_label,ylim=(0,100),xlim=(0,0)):
    """grafica cualquier tipo de señal
    Args:
        t (array): eje temporal (eje x)
        señal (array): señal a graficar (eje y)
        duracion (float): tiempo a mostrar en el grafico
        titulo (str): titulo del grafico
        x_label (str): etiqueta del eje x
        y_label (str): etiqueta del eje y
        ylim (array,optional): limites del eje y
        xlim (array,optional): limites del eje x
    """

    
    plt.figure(figsize=(12,5))
    plt.title(titulo)
    plt.plot(t,señal)
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud")
    plt.xlim(0,duracion)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(True)
    plt.ylim(ylim)
    if xlim != (0,0):
        plt.xlim(xlim)
    plt.show()


def fft(fft_raw,f1,f2,fs,titulo,dB=False,min_dB=0,axvlines=[0]):
    """Genera grafico de fft en db en funcion de frecuencia

    Args:
        fft_raw (array): fft salida desde numpy
        f1 (float): frecuencia inferior a mostrar
        f2 (float): frecuencia superior a mostrar
        fs (int): frecuencia de muestreo
        titulo (str): titulo del grafico
        dB (Bool, optional): true es escala en DB. Defaults to False
        min_dB (float, optional): minimo valor del eje y mostrado en el grafico, si no hay nada se setea al minimo valor que toma la fft
        axvlines (array,optional): posiciones del eje x donde se colocan lineas horizontales de color verde.
    """
    plt.figure(figsize = (16, 5))

    fft = fft_raw[:int(len(fft_raw)/2)]

    fft_mag=(abs(fft))/len(fft_raw)
    xfreqs=[16,31.5,63,125,250,500,1000,2000,4000,8000,16000]
    f2=others.find_nearest(xfreqs,f2)
    f1=others.find_nearest(xfreqs,f1)
    

    freqs=np.linspace(0,fs/2,fft_mag.size)#fs/2 por nyquist

    
    if dB==True:
        fft_mag_db=20*np.log10(fft_mag / np.max(abs(fft_mag)))
        plt.semilogx(freqs, fft_mag_db)
        plt.xticks(xfreqs,xfreqs)
        plt.xlim(f1,f2)
        plt.ylabel("Amplitud(dB)")
        
        if min_dB!=0:
            plt.ylim((min_dB,0))
        else: 
            plt.ylim((np.min(fft_mag_db),0))
    else:
        plt.semilogx(freqs, fft_mag)
        plt.xticks(xfreqs,xfreqs)
        plt.xlim(f1,f2)
        plt.ylabel("Amplitud")
        plt.ylim((np.min(fft_mag),0))
       
    plt.title(titulo)
    plt.grid(True)
    plt.xlabel("Frecuencia (Hz)")
    
    for x in axvlines:
        plt.axvline(x,color="green")
    plt.show()
    return      
        
def señal_periodica(titulo,señal,t,periodos,f,x_label,y_label):

    """
    Args:
        titulo (str): titulo del grafico
        señal (array):arreglo que contiene la señal
        t (array) :eje temporal
        periodos (int): numeros de periodos a mostrar
        f(float): frecuencia de la señal
        x_label,y_label (str): etiquetas de ejes
    """
    plt.figure(figsize = (16, 5))
    plt.title(titulo)
    plt.plot(t,señal)
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud")
    plt.xlim(0,periodos/f)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(True)
    plt.show()
    
def filtro(freq,eje_y,min_x,max_x,titulo,fase=False):
    """grafica respuesta en frecuencia de un filtro dado

    Args:
        freq (array): eje frecuencial del grafico
        eje_y (array): eje y del grafico
        min_x (float): minimo valor del eje x a mostrar
        max_x (float): minimo valor del eje y a mostrar
        titulo (str): titulo del grafico
        fase (bool, optional): Si true grafica la fase. Si false la magnitud. Defaults to False.
    """
    if fase==True:
        min_y=np.min(eje_y)
        max_y=np.max(eje_y)
        plt.ylabel("Fase (rad)")
    else:
        min_y=-100
        max_y=0
        plt.ylabel("Amplitud (dB)")
        
    plt.title(titulo)
    plt.semilogx(freq,eje_y)
    plt.xlabel("Frecuencia (Hz)")
    plt.grid()
    xfreqs=[16,31.5,63,125,250,500,1000,2000,4000,8000,16000]
    plt.xticks(xfreqs ,xfreqs)
    max_x=others.find_nearest(xfreqs,max_x)
    min_x=others.find_nearest(xfreqs,min_x)
    plt.xticks(xfreqs ,xfreqs)
    plt.ylim(min_y,max_y)
    plt.xlim(min_x,max_x)
    
    plt.show()
    

def bandas_db(leq_bandas,titulo,octava=1,axhline=[0,0]):
    """Muestra grafico de barras referente a los leqs por banda

    Args:
        leq_bandas (array): eje y del grafico, LEQS por banda
        titulo (str): titulo del grafici
        octava (int, optional): 1 para bandas de octava y 3 para bandas de tercio. Defaults to 1.
        axhline (int, optional): muestra linea horizontal en el grafico. Defaults to 0.
    """

    octava_nombres=["31.25","62.5","125","250","500","1k","2k","4k","8k","16k"]
    tercio_octava_nombres=["25","31.5","40","50","63","80",
                           "100","125","160","200","250","315","400",
                           "500","630","800","1k","1.25k","1.6k",
                           "2k","2.5k","3.15k","4k","5k","6.3k","8k",
                           "10k","12.5k","16k","20k"]
    
    
    if others.validar_fraccion_octava==False :
        print("Error en la seleccion de fraccion de octava. Valores: 1 ó 3.")
        return
        
    if octava==1:
        plt.figure(figsize = (13, 5))
        
        if np.shape(leq_bandas) != (10,):
            print("Error en la cantidad de datos o tipo de banda")
            return  
        plt.bar(octava_nombres,leq_bandas)  
        
          
    elif octava==3:
        plt.figure(figsize = (16, 5))
        if np.shape(leq_bandas) != (30,):
            print("Error en la cantidad de datos o tipo de banda")
            return 
        plt.bar(tercio_octava_nombres,leq_bandas)
        

    
    plt.axhline(axhline[0],color="green")
    plt.axhline(axhline[1],color="yellow")
    
    plt.xlabel("Banda (Hz)")
    plt.ylabel("Nivel de Presion Sonora (dB)")
    plt.title(titulo)
    plt.grid()
    plt.show()
    return

def visualizar_banco_filtros(fc,x_nombres,freq,octava_particular,f_inf_particular,f_sup_particular,fraccion_octava,f_muestra):
    """
    Esta funcion es parte de otro modulo. No tiene sentido por si sola. Grafica e 
    imprime informacion respectiva a los filtros que se generan en el banco de filtros.
    """
    
    plt.ylabel("Atenuacion (dB)")
    plt.title("Filtros generados")
    plt.xlabel("Frecuencia (Hz)")
    plt.grid()
    xfreqs=fc
    plt.xticks(xfreqs ,x_nombres)
    plt.xlim(16,16000)
    plt.ylim(-60,0)
    plt.show() 
    
    plt.figure(figsize = (12, 5))  
    plt.semilogx(freq,20*np.log10(octava_particular))
    plt.ylabel("Atenuacion (dB)")
    
    plt.xlim(250,4000)
    plt.grid()
    
    if fraccion_octava==1:
        xfreqs=[f_muestra/4,f_muestra/2,f_muestra/1.5,f_muestra,f_muestra*1.5,f_muestra*2,f_muestra*4]
        plt.title("Octava centrada en 1000 Hz")
        xfreqs_nombres=np.around(np.log2(np.divide(xfreqs,f_muestra)),decimals=2)
        plt.xlabel("Frecuencia normalizada - valor mostrado: log2(f/fm) ")
        plt.xticks(xfreqs ,xfreqs_nombres)
        
        plt.xlim(16,16000)
        plt.axhline(-5.5,color="red")
        plt.axhline(-16.5,color="blue")
        plt.axvline(f_muestra/2,color="blue")
        plt.axvline(f_muestra/1.5,color="red")
        
    elif fraccion_octava==3:
            plt.title("Tercio de octava centrada en 1000 Hz")
            xfreqs=[f_muestra*2**(-2/3),f_muestra*2**(-1/3),f_muestra*2**(-0.5/3),f_muestra,f_muestra*2**(0.5/3),f_muestra*2**(1/3),f_muestra*2**(2/3)]
            plt.xlim(f_muestra*2**(-2/3),f_muestra*2**(2/3))
            xfreqs_nombres=np.around(np.divide(xfreqs,f_muestra),decimals=2)
            plt.axhline(-5.5,color="red")
            plt.axhline(-16.5,color="blue")
            plt.axvline(f_muestra*2**(-1/3),color="blue")
            plt.axvline(f_muestra*2**(-0.5/3),color="red")
            plt.xlabel("Frecuencia normalizada - valor mostrado: f/fm ")
            plt.xticks(xfreqs ,xfreqs_nombres)
            
            
    #plt.xlim(16,16000)
    plt.ylim(-60,0)
    plt.show()

    print("Frencuencia central: %.01f Hz" % f_muestra)
    print("Frecuencias de corte: %.01f Hz - %.01f Hz" % (f_inf_particular,f_sup_particular))
    resta=f_sup_particular-f_inf_particular
    print("Ancho de banda: %.01f Hz" % resta)
    print("Relacion f_superior/f_inferior:", f_sup_particular/f_inf_particular)
    