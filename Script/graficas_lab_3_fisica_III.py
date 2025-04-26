import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame, Series
import numpy as np
from scipy.fft import rfft, rfftfreq

color_graficas_verde = "#6aa84f"
color_graficas_azul = "#5793b5"
verde_uis = "#67b93e"
nombre_archivo_velocidades = "Velocidades_Pendulo"
tamanio_graficas = (12, 7)


def extraer_dataframe(nombre_archivo: str,
                      buscar_en_hoja_especifica: bool = False,
                      nombre_hoja: str = None):
    if buscar_en_hoja_especifica == False:
        try:
            df = pd.read_excel(f'{nombre_archivo}.xlsx', engine='openpyxl')
        except FileNotFoundError:
            try:
                df = pd.read_excel(f'{nombre_archivo}.xls')
            except FileNotFoundError:
                print(f"El archivo '{nombre_archivo}.xlsx' o '{nombre_archivo}.xls' no se encontró en el directorio actual.")
                print("Por favor, asegúrate de que el archivo está en el directorio correcto o proporciona la ruta completa.")
                exit()
    else:
        try:
            df = pd.read_excel(f'{nombre_archivo}.xlsx', engine='openpyxl', sheet_name=nombre_hoja)
        except FileNotFoundError:
            try:
                df = pd.read_excel(f'{nombre_archivo}.xls', engine='openpyxl', sheet_name=nombre_hoja)
            except FileNotFoundError:
                print(f"El archivo '{nombre_archivo}.xlsx' o '{nombre_archivo}.xls' no se encontró en el directorio actual.")
                print("Por favor, asegúrate de que el archivo está en el directorio correcto o proporciona la ruta completa.")
                exit()
    
    return df


def graficar_df_frecuencias(t: Series, f: Series):
    plt.figure(figsize=tamanio_graficas)
    plt.plot(t, f, color=color_graficas_verde)
    plt.title("Frecuencia percibida vs Tiempo")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Frecuencia [Hz]")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def graficar_seccion_frecuencias(t: Series, f: Series,
                                 y_lim_i: float, y_lim_f: float,
                                 x_lim_i: float, x_lim_f: float):
    plt.figure(figsize=tamanio_graficas)
    plt.scatter(t, f, s=20, color=verde_uis, alpha=1, label="Valores Registrados")
    plt.plot(t, f, color=color_graficas_verde)
    plt.title("Frecuencia percibida vs Tiempo")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Frecuencia [Hz]")
    plt.ylim(y_lim_i, y_lim_f)
    plt.xlim(x_lim_i, x_lim_f)
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.show()


def graficar_fourier(t_inicio: float, df: DataFrame):
    # --- SELECCIÓN DE INTERVALO ---              
    t_final = t_inicio + 4.2     
    df_filtrado = df[(df["Time (s)"] >= t_inicio) & (df["Time (s)"] <= t_final)].copy()

    # --- EXTRAER Y PREPARAR DATOS ---
    t = df_filtrado["Time (s)"].values
    try:
        f = df_filtrado["Frequency (Hz)"].values
    except:
        f = df_filtrado["V (m/s)"].values

    # Calcular delta t (debería ser constante o casi constante)
    dt = np.mean(np.diff(t))

    # Restar el promedio → se centra la señal
    f_centrada = f - np.mean(f)

    # --- TRANSFORMADA DE FOURIER ---
    F_fft = rfft(f_centrada)
    frecuencias = rfftfreq(len(f), d=dt)
    magnitud = np.abs(F_fft)


    # --- ENCONTRAR EL PICO PRINCIPAL ---
    indice_pico = np.argmax(magnitud)
    frecuencia_dominante = frecuencias[indice_pico]

    # --- GRAFICAR ---
    plt.figure(figsize=tamanio_graficas)
    plt.plot(frecuencias, magnitud, color='mediumblue')
    plt.axvline(frecuencia_dominante, color='red', linestyle='--', label=f"Pico: {frecuencia_dominante:.2f} Hz")
    plt.title("Espectro de Frecuencia (Transformada de Fourier)")
    plt.xlabel("Frecuencia (Hz)")
    plt.ylabel("Magnitud")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------------------
# Para el receptor oscilando, frecuencia base 1000 Hz.
# ---------------------------------------------------------------------

# nombre_archivo = "Efecto Doppler 2025-04-04 19-12-45"
# df = extraer_dataframe(nombre_archivo)

# t = df["Time (s)"]
# f = df["Frequency (Hz)"]

# graficar_df_frecuencias(t, f)

# # Viendo la gráfica, se seleccionan los datos desde t=10.3 hasta t=14.5
# graficar_seccion_frecuencias(t, f, 995, 1004, 10.3, 14.5)
# graficar_fourier(10.3, df)

# # Análisis por Fourier de las velocidades obtenidas por medio de Tracker
# df_vel = extraer_dataframe(nombre_archivo_velocidades, True, "1k Receptor Oscilando")
# graficar_fourier(0, df_vel)


# ---------------------------------------------------------------------
# Para el receptor oscilando, frecuencia base 1500 Hz.
# ---------------------------------------------------------------------

nombre_archivo = "Efecto Doppler 2025-04-04 19-15-57"
df = extraer_dataframe(nombre_archivo)

t = df["Time (s)"]
f = df["Frequency (Hz)"]

graficar_df_frecuencias(t, f)

# Viendo la gráfica, se seleccionan los datos desde t=11.45 hasta t=15.7
graficar_seccion_frecuencias(t, f, 1497, 1502.5, 11.45, 15.7)
graficar_fourier(11.45, df)

# Análisis por Fourier de las velocidades obtenidas por medio de Tracker
df_vel = extraer_dataframe(nombre_archivo_velocidades, True, "1.5k Receptor Oscilando")
graficar_fourier(0, df_vel)


# ---------------------------------------------------------------------
# Para el receptor oscilando, frecuencia base 2000 Hz.
# ---------------------------------------------------------------------

nombre_archivo = "Efecto Doppler 2025-04-04 19-20-05"
df = extraer_dataframe(nombre_archivo)

t = df["Time (s)"]
f = df["Frequency (Hz)"]

graficar_df_frecuencias(t, f)

# Viendo la gráfica, se seleccionan los datos desde t=12 hasta t=16.2
graficar_seccion_frecuencias(t, f, 1997, 2003, 12, 16.2)
graficar_fourier(12, df)

# Análisis por Fourier de las velocidades obtenidas por medio de Tracker
df_vel = extraer_dataframe(nombre_archivo_velocidades, True, "2k Receptor Oscilando")
graficar_fourier(0, df_vel)


# ---------------------------------------------------------------------
# Para el receptor oscilando, frecuencia base 2500 Hz.
# ---------------------------------------------------------------------

nombre_archivo = "Efecto Doppler 2025-04-04 19-21-20"
df = extraer_dataframe(nombre_archivo)

t = df["Time (s)"]
f = df["Frequency (Hz)"]

graficar_df_frecuencias(t, f)

# Viendo la gráfica, se seleccionan los datos desde t=11 hasta t=15.2
graficar_seccion_frecuencias(t, f, 2492, 2507, 11, 15.2)
graficar_fourier(11, df)

# Análisis por Fourier de las velocidades obtenidas por medio de Tracker
df_vel = extraer_dataframe(nombre_archivo_velocidades, True, "2.5k Receptor Oscilando")
graficar_fourier(0, df_vel)


# ---------------------------------------------------------------------
# Para el receptor oscilando, frecuencia base 3000 Hz.
# ---------------------------------------------------------------------

nombre_archivo = "Efecto Doppler 2025-04-04 19-22-25"
df = extraer_dataframe(nombre_archivo)

t = df["Time (s)"]
f = df["Frequency (Hz)"]


graficar_df_frecuencias(t, f)

# Viendo la gráfica, se seleccionan los datos desde t=11.96 hasta t=16.16
graficar_seccion_frecuencias(t, f, 2994, 3006.5, 11.96, 16.16)
graficar_fourier(11.96, df)

# Análisis por Fourier de las velocidades obtenidas por medio de Tracker
df_vel = extraer_dataframe(nombre_archivo_velocidades, True, "3k Receptor Oscilando")
graficar_fourier(0, df_vel)


# ---------------------------------------------------------------------
# Para el receptor oscilando, frecuencia base 3500 Hz.
# ---------------------------------------------------------------------

nombre_archivo = "Efecto Doppler 2025-04-04 19-23-30"
df = extraer_dataframe(nombre_archivo)

t = df["Time (s)"]
f = df["Frequency (Hz)"]


graficar_df_frecuencias(t, f)

# Viendo la gráfica, se seleccionan los datos desde t=7 hasta t=11.2
graficar_seccion_frecuencias(t, f, 3491.5, 3506, 7, 11.2)
graficar_fourier(7, df)

# Análisis por Fourier de las velocidades obtenidas por medio de Tracker
df_vel = extraer_dataframe(nombre_archivo_velocidades, True, "3.5k Receptor Oscilando")
graficar_fourier(0, df_vel)


# ---------------------------------------------------------------------
# Para el receptor en reposo, frecuencia base 1000 Hz.
# ---------------------------------------------------------------------

nombre_archivo = "Efecto Doppler 2025-04-04 19-02-33"
df = extraer_dataframe(nombre_archivo)

t = df["Time (s)"]
f = df["Frequency (Hz)"]


graficar_df_frecuencias(t, f)

# Viendo la gráfica, se seleccionan los datos desde t=13.48 hasta t=17.68
graficar_seccion_frecuencias(t, f, 996, 1002, 13.48, 17.68)
graficar_fourier(13.48, df)

# Análisis por Fourier de las velocidades obtenidas por medio de Tracker
df_vel = extraer_dataframe(nombre_archivo_velocidades, True, "1k Receptor Reposo")
graficar_fourier(-1.242, df_vel)


# ---------------------------------------------------------------------
# Para el receptor en reposo, frecuencia base 1500 Hz.
# ---------------------------------------------------------------------

nombre_archivo = "Efecto Doppler 2025-04-04 19-08-15"
df = extraer_dataframe(nombre_archivo)

t = df["Time (s)"]
f = df["Frequency (Hz)"]

graficar_df_frecuencias(t, f)

# Viendo la gráfica, se seleccionan los datos desde t=11.2 hasta t=15.4
# Además, se ordenan los valores del tiempo para evitar algunas irregularidades por Phyphox
# además, se interpolan los datos para eliminar los "huecos"
df = df.sort_values(by='Time (s)').reset_index(drop=True)
df = df.interpolate(method='linear')
t = df["Time (s)"]
f = df["Frequency (Hz)"]
graficar_seccion_frecuencias(t, f, 1492, 1508.5, 11.2, 15.4)
graficar_fourier(11.2, df)

# Análisis por Fourier de las velocidades obtenidas por medio de Tracker
df_vel = extraer_dataframe(nombre_archivo_velocidades, True, "1.5k Receptor Reposo")
graficar_fourier(0, df_vel)


# ---------------------------------------------------------------------
# Para el receptor en reposo, frecuencia base 2000 Hz.
# ---------------------------------------------------------------------

nombre_archivo = "Efecto Doppler 2025-04-04 19-10-01"
df = extraer_dataframe(nombre_archivo)

t = df["Time (s)"]
f = df["Frequency (Hz)"]

graficar_df_frecuencias(t, f)

# Viendo la gráfica, se seleccionan los datos desde t=10.48 hasta t=14.68
graficar_seccion_frecuencias(t, f, 1992, 2006, 10.48, 14.68)
graficar_fourier(10.48, df)

# Análisis por Fourier de las velocidades obtenidas por medio de Tracker
df_vel = extraer_dataframe(nombre_archivo_velocidades, True, "2k Receptor Reposo")
graficar_fourier(0, df_vel)


# ---------------------------------------------------------------------
# Para el receptor en reposo, frecuencia base 2500 Hz.
# ---------------------------------------------------------------------

nombre_archivo = "Efecto Doppler 2025-04-04 19-24-33"
df = extraer_dataframe(nombre_archivo)

t = df["Time (s)"]
f = df["Frequency (Hz)"]

graficar_df_frecuencias(t, f)

# Viendo la gráfica, se seleccionan los datos desde t=14.2 hasta t=18.4
graficar_seccion_frecuencias(t, f, 2492.5, 2508, 14.2, 18.4)
graficar_fourier(14.2, df)

# Análisis por Fourier de las velocidades obtenidas por medio de Tracker
df_vel = extraer_dataframe(nombre_archivo_velocidades, True, "2.5k Receptor Reposo")
graficar_fourier(0, df_vel)


# ---------------------------------------------------------------------
# Para el receptor en reposo, frecuencia base 3000 Hz.
# ---------------------------------------------------------------------

nombre_archivo = "Efecto Doppler 2025-04-04 19-27-03"
df = extraer_dataframe(nombre_archivo)

t = df["Time (s)"]
f = df["Frequency (Hz)"]

graficar_df_frecuencias(t, f)

# Viendo la gráfica, se seleccionan los datos desde t=9.5 hasta t=13.7
# Además, se ordenan los valores del tiempo para evitar algunas irregularidades por Phyphox
# además, se interpolan los datos para eliminar los "huecos"
df = df.sort_values(by='Time (s)').reset_index(drop=True)
df = df.interpolate(method='linear')
t = df["Time (s)"]
f = df["Frequency (Hz)"]
graficar_seccion_frecuencias(t, f, 2991, 3010, 9.5, 13.7)
graficar_fourier(9.5, df)

# Análisis por Fourier de las velocidades obtenidas por medio de Tracker
df_vel = extraer_dataframe(nombre_archivo_velocidades, True, "3k Receptor Reposo")
graficar_fourier(0, df_vel)


# ---------------------------------------------------------------------
# Para el receptor en reposo, frecuencia base 3500 Hz.
# ---------------------------------------------------------------------

nombre_archivo = "Efecto Doppler 2025-04-04 19-32-08"
df = extraer_dataframe(nombre_archivo)

t = df["Time (s)"]
f = df["Frequency (Hz)"]

graficar_df_frecuencias(t, f)

# Viendo la gráfica, se seleccionan los datos desde t=10.6 hasta t=14.8
# Además, se ordenan los valores del tiempo para evitar algunas irregularidades por Phyphox
# además, se interpolan los datos para eliminar los "huecos"
df = df.sort_values(by='Time (s)').reset_index(drop=True)
df = df.interpolate(method='linear')
t = df["Time (s)"]
f = df["Frequency (Hz)"]
graficar_seccion_frecuencias(t, f, 3490, 3510, 10.6, 14.8)
graficar_fourier(10.6, df)

# Análisis por Fourier de las velocidades obtenidas por medio de Tracker
df_vel = extraer_dataframe(nombre_archivo_velocidades, True, "3.5k Receptor Reposo")
graficar_fourier(0, df_vel)