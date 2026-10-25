"""
Funciones para calcular variables climatologicas extremas mensuales a partir de
datos DIARIOS de una estacion meteorologica.

Por ahora: TME (Temperatura Maxima Extrema).
Pendiente: Variable de precipitacion (se agrega como bloque nuevo mas adelante).

Pensado para cualquier estacion con datos diarios (ej. SMN Argentina), no solo
Misiones. Lo unico que cambia entre estaciones suele ser el paso asociodo
a la carga de datos.

En la carga de datos hay que tener en cuenta que la carpeta tiene la siguiente 
estructura:
    climatologia-sequia
        data            #datos de estaciones
        resultados      #donde se guardan los resultados
        scr             #script
"""

import os
import numpy as np
import pandas as pd

#seteamos directorio en dónde está la carpeta "climatologia-sequia" y entramos
os.getcwd()
dir0 = "C:\\Users\\Pc\\Desktop\\prog\\git\\climatologia-sequias"
dir1 = ""  #Espacio para cargar ruta hacia el archivo a leer
os.chdir(dir0)

#cargamos las funciones que vamos a utilizar para la climatologia

#cargamos los datos que deben estar en la carpeta data
def cargar_datos(nombre,
                 ruta="data",
                 sep="\t",
                 col_anio="anio",
                 col_mes="mes",
                 col_dia="dia"):
    """Esta función lo que hace es tomar como ruta nombre del archivo y necesita
    que esté separados por tabulaciones, en caso de que su archivo no esté 
    separado de esa manera puede modificar el sep para que lo lea correctamente"""
    
    ruta_archivo = f"{ruta}/{nombre}"
    df = pd.read_csv(ruta_archivo, sep=sep)
    df = df.rename(columns={col_anio: "anio", col_mes: "mes", col_dia: "dia"})
    return df

#calculamos la tme
def calculo_tme(df,
                n=5):
    """Esta función toma el DataFrame cargado con los datos diarios como primer
    parámetro, el segundo es para la cantidad de días que va a considerar. Estos
    días mencionados representan la cantidad de datos que toma para calcular el
    promedio, el valor predefinido es 5, es decir, toma los 5 valores máximos
    de cada mes y calculo un promedio que representará al mes."""
    TME = df.groupby(["anio", "mes"])["tmax"].apply(lambda x: x.nlargest(n).mean())
    TME = TME.reset_index()
    TME.columns = ["anio", "mes", "TME"]
    return TME
#espacio para la variable pp

#union de dataframe para trabajar cómodamente

#guardo los datos
def guardar_resultados(df, nombre_salida, outdir="resultados"):
    """Esta función guarda un DataFrame como CSV en la carpeta de resultados.
    Como salida guarda la ruta en la que está guardado esta tabla para un posible
    uso en el futuro. En una próxima actualización se le pueden agregar parámetros
    de separacion para guardar en distinto formatos.
    obs: para excel en español funciona guardar el nombre_salida.csv
    """
    
    csv_ruta = f"{outdir}/{nombre_salida}"
    df.to_csv(csv_ruta, index=False, sep=";", decimal=",")
    return csv_ruta

#prueba con datos de posadas
df_posadas = cargar_datos("posadas.txt")
tme_posadas = calculo_tme(df_posadas,5)
guardar_resultados(tme_posadas, "posadas_tme.csv")
