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
import matplotlib.pyplot as plt 

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
    os.makedirs(outdir, exist_ok=True)
    df.to_csv(csv_ruta, index=False, sep=";", decimal=",")
    return csv_ruta

#calculo de un dato por año a partir de la tabla mensual
def serie_anual(df,
                meses=(1, 2, 3, 4),
                col="TME",
                agregacion="promedio"):
    """toma la tabla mensual (anio, mes, variable), se queda solo con los meses
    de la tupla 'meses' y devuelve un valor por año. 'agregacion' puede ser
    'promedio' o 'acumulado' (suma). si a un año le falta algún mes o tiene
    un mes sin dato, el valor de ese año queda en NaN."""
    
    #me quedo solo con los meses que pedí
    sel = df[df["mes"].isin(meses)]
    g = sel.groupby("anio")[col]
    
    if agregacion == "promedio":
        valor = g.mean()
    elif agregacion == "acumulado":
        valor = g.sum(min_count=1)
    else:
        raise ValueError("agregacion tiene que ser 'promedio' o 'acumulado'")
    
    #si no están todos los meses con dato, el año no vale
    valor = valor.where(g.count() == len(meses))
    
    anual = valor.reset_index()
    anual.columns = ["anio", f"{col}_{agregacion}"]
    return anual

def graficar_serie(df,
                   nombre_salida,
                   col=None,
                   titulo="",
                   ylabel="",
                   color="steelblue",
                   outdir="resultados"):
    """toma el df anual (columnas anio y la variable) y guarda un gráfico de la
    serie con su línea de tendencia en resultados/series_temporales.
    nombre_salida va con extensión, por ejemplo "posadas_tme_anual.png".
    si no paso 'col', agarra la última columna del df.
    devuelve un diccionario con r, pendiente, n y la ruta donde guardó."""
    
    #si no le digo qué columna, usa la última (la variable de la serie)
    if col is None:
        col = df.columns[-1]
    
    #creo la carpeta si no existe
    carpeta = f"{outdir}/series_temporales"
    os.makedirs(carpeta, exist_ok=True)
    
    x = df["anio"].to_numpy()
    y = df[col].to_numpy(dtype=float)
    
    #solo los años con dato para la tendencia (~ invierte los nan)
    ok = ~np.isnan(y)
    if ok.sum() < 3:
        raise ValueError("hay menos de 3 años con dato, no alcanza para una tendencia")
    
    pendiente, ordenada = np.polyfit(x[ok], y[ok], 1)
    r = np.corrcoef(x[ok], y[ok])[0, 1]
    
    #grafico: serie con huecos donde hay nan, y la recta de tendencia
    plt.figure(figsize=(10, 4))
    plt.plot(x, y, color=color, marker="o")
    plt.plot(x, pendiente * x + ordenada, color="black", linestyle="--",
             label=f"tendencia: {pendiente:.3f} por año (r = {r:.2f})")
    plt.title(titulo)
    plt.xlabel("Año")
    plt.ylabel(ylabel)
    plt.xticks(range(int(x.min()), int(x.max()) + 1, 5))
    plt.legend()
    plt.tight_layout()
    
    ruta = f"{carpeta}/{nombre_salida}"
    plt.savefig(ruta, dpi=150)
    plt.close()
    return {"r": r, "pendiente": pendiente, "n": int(ok.sum()), "ruta": ruta}

#prueba con datos de posadas
df_posadas = cargar_datos("posadas.txt")
tme_posadas = calculo_tme(df_posadas,5)
guardar_resultados(tme_posadas, "posadas_tme.csv")
tme_anual = serie_anual(tme_posadas)
res = graficar_serie(tme_anual, "posadas_tme_anual.png",
                     titulo="TME promedio ene-abr - Posadas",
                     ylabel="TME (°C)")