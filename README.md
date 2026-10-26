# Climatología y sequías

Herramientas en Python para procesar series diarias de estaciones meteorológicas y calcular indicadores 
climatológicos extremos mensuales. El proyecto está diseñado para trabajar con datos de distintas estaciones
 y forma parte de un trabajo de análisis climatológico orientado al estudio de condiciones asociadas a 
sequías e incendios.

## Objetivo

Desarrollar herramientas para procesar series históricas de datos meteorológicos y obtener indicadores 
que permitan caracterizar el comportamiento de las temperaturas extremas. A futuro, se busca incorporar
variables de precipitación y explorar la relación entre estos indicadores, los eventos de sequía y otros
factores climáticos.

## Metodología

### Temperatura máxima extrema (TME)

Actualmente, el script implementa el cálculo de la temperatura máxima extrema (TME) a partir de datos 
diarios de temperatura máxima (`tmax`), correspondientes al período 1991–2020.

Para cada mes de cada año, el procedimiento consiste en:

1. Identificar los cinco valores diarios de temperatura máxima más elevados.
2. Calcular el promedio de esos valores.
3. Asignar el resultado como valor mensual de TME para ese año.

La cantidad de valores considerados puede modificarse mediante el parámetro `n` de la función `calculo_tme()`.
Por defecto, se utilizan los cinco valores más altos.

El indicador permite resumir el comportamiento de las temperaturas máximas más elevadas de cada mes a lo largo 
de la serie histórica.

**Calidad de los datos:** se espera que las series de entrada hayan pasado previamente por controles de calidad, 
que no contengan fechas duplicadas y que se hayan revisado los valores atípicos y los datos faltantes. El script
 actual no realiza estos controles automáticamente.

## Estructura del repositorio

```text
climatologia-sequias/
├── data/
│   └── posadas.txt
├── resultados/
└── src/
    └── script_general.py
```

- **`data/`**: contiene los archivos de datos diarios de las estaciones meteorológicas. Se incluye un archivo de 
ejemplo correspondiente a Posadas.
- **`src/`**: contiene `script_general.py`, con las funciones para cargar los datos, calcular la TME y guardar 
los resultados.
- **`resultados/`**: directorio de salida donde se guardan los archivos CSV generados por el análisis.

## Requisitos

- Python 3.
- [pandas](https://pandas.pydata.org/) para la lectura, manipulación y agrupamiento de los datos.
- [NumPy](https://numpy.org/) como dependencia del entorno de trabajo.

## Formato de los datos de entrada

El programa espera archivos de texto delimitados por tabulaciones, con una fila por día y las siguientes columnas:

| Columna | Descripción |
|---|---|
| `anio` | Año de la observación. |
| `mes` | Mes de la observación, del 1 al 12. |
| `dia` | Día de la observación. |
| `tmax` | Temperatura máxima diaria. |

Los nombres de las columnas correspondientes al año, mes y día pueden adaptarse mediante los parámetros de la 
función `cargar_datos()`. El separador también puede modificarse si el archivo utiliza un formato diferente.

Se recomienda trabajar con series diarias completas, sin fechas duplicadas y con los valores sometidos a controles 
de calidad previos. El tratamiento de datos faltantes y la aplicación de criterios de completitud mensual deberán 
definirse y verificarse antes de utilizar los resultados en análisis climatológicos definitivos.

## Cómo utilizar el script

1. Descargar o clonar el repositorio.
2. Instalar las dependencias necesarias.
3. Colocar los archivos de datos en la carpeta `data/`.
4. Abrir `src/script_general.py` y configurar la variable `dir0` con la ruta local de la carpeta raíz del proyecto.
5. Verificar que exista la carpeta `resultados/`.
6. Ejecutar el script.

El archivo incluye un ejemplo de uso con los datos de Posadas y las funciones implementadas. Al ejecutarlo, se genera 
el archivo `posadas_tme.csv` en la carpeta `resultados/`.

El CSV se exporta con punto y coma como separador de campos y coma como separador decimal.

### Funciones disponibles

- **`cargar_datos()`**: lee un archivo de datos diarios y permite configurar la ruta, el separador y los nombres 
de las columnas de fecha.
- **`calculo_tme()`**: calcula la TME para cada combinación de año y mes. El parámetro `n` permite definir cuántos 
valores máximos se utilizan en el promedio.
- **`guardar_resultados()`**: exporta el DataFrame resultante a un archivo CSV y devuelve la ruta del archivo generado.

## Fuente de los datos y licencias

### Código

El código del proyecto se distribuye bajo la licencia MIT, siempre que esté incluido el archivo `LICENSE` correspondiente. Esta licencia se aplica al código y no implica que los datos meteorológicos tengan las mismas condiciones de uso.

### Datos meteorológicos

- **Fuente:** Servicio Meteorológico Nacional (SMN), Argentina.
- **Estación:** Posadas. Número de estación: [87178].
- **Período:** 1991–2020.
- **Variables:** temperatura máxima diaria; se prevé incorporar precipitación.
- **Origen del archivo:** Servicio Meteorológico Nacional (Argentina).
- **Fecha de obtención:** 2026
- **Condiciones de uso:** verificar la licencia y las condiciones de reutilización aplicables a los datos originales. 
Si corresponde la licencia Creative Commons Atribución 2.5 Argentina (CC BY 2.5 AR), deberá respetarse la atribución 
a la fuente.

Sitio oficial: [Servicio Meteorológico Nacional](https://www.smn.gob.ar/).

## Desarrollo futuro

Las próximas etapas previstas incluyen:

- Incorporar el procesamiento de datos de precipitación.
- Implementar controles de calidad y criterios de completitud de las series.
- Calcular percentiles para establecer umbrales climatológicos de temperaturas extremas.
- Identificar los valores de TME que superen los umbrales definidos.
- Generar gráficos para visualizar y analizar los resultados.
- Explorar la relación entre los indicadores climatológicos, las sequías, los incendios y factores de variabilidad climática como ENSO.

Estas funcionalidades se encuentran pendientes de implementación.