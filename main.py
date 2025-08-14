# app.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- Configuración de la página ---
st.set_page_config(
    page_title="EDA con Datos Aleatorios",
    page_icon="📊",
    layout="wide"
)

st.title('Análisis Exploratorio de Datos con Streamlit 📊')
st.markdown('Esta aplicación genera datos aleatorios para demostrar un flujo básico de EDA y visualizaciones.')

# --- Generación de datos aleatorios ---
@st.cache_data
def generar_datos():
    """
    Genera un DataFrame de pandas con datos aleatorios.
    """
    # Genera 100 filas de datos
    filas = 100
    
    # Crea una columna de fechas
    fechas = pd.date_range('2023-01-01', periods=filas, freq='D')
    
    # Crea datos aleatorios para ventas
    ventas = np.random.randint(100, 500, size=filas)
    
    # Crea una columna de categoría con 3 categorías
    categorias = np.random.choice(['Electrónica', 'Ropa', 'Hogar'], size=filas)
    
    # Combina todo en un DataFrame
    df = pd.DataFrame({
        'Fecha': fechas,
        'Categoría': categorias,
        'Ventas': ventas
    })
    
    return df

df = generar_datos()

# --- Sección de Análisis Exploratorio de Datos (EDA) ---
st.header('1. Resumen de los Datos')
st.subheader('DataFrame (primeras 5 filas)')
st.write(df.head())

st.subheader('Estadísticas descriptivas')
st.write(df.describe())

st.subheader('Conteo de valores por categoría')
st.write(df['Categoría'].value_counts())

# --- Sección de Visualizaciones ---
st.header('2. Visualizaciones')

# --- Gráfico de Barras ---
st.subheader('Ventas por Categoría')

# Agrupa los datos por categoría y suma las ventas
ventas_por_categoria = df.groupby('Categoría')['Ventas'].sum()

# Crea la figura y los ejes para el gráfico
fig_bar, ax_bar = plt.subplots(figsize=(10, 6))

# Genera el gráfico de barras
ax_bar.bar(ventas_por_categoria.index, ventas_por_categoria.values, color=['skyblue', 'salmon', 'lightgreen'])

# Añade etiquetas y título
ax_bar.set_title('Total de Ventas por Categoría', fontsize=16)
ax_bar.set_xlabel('Categoría', fontsize=12)
ax_bar.set_ylabel('Ventas Totales', fontsize=12)
ax_bar.grid(axis='y', linestyle='--', alpha=0.7)

# Muestra el gráfico en Streamlit
st.pyplot(fig_bar)

# --- Gráfico de Líneas ---
st.subheader('Tendencia de Ventas a lo Largo del Tiempo')

# Crea la figura y los ejes para el gráfico
fig_line, ax_line = plt.subplots(figsize=(12, 6))

# Genera el gráfico de líneas
ax_line.plot(df['Fecha'], df['Ventas'], color='purple', marker='o', linestyle='-')

# Añade etiquetas y título
ax_line.set_title('Tendencia Diaria de Ventas', fontsize=16)
ax_line.set_xlabel('Fecha', fontsize=12)
ax_line.set_ylabel('Ventas', fontsize=12)
ax_line.grid(True, linestyle='--', alpha=0.7)
ax_line.tick_params(axis='x', rotation=45)

# Muestra el gráfico en Streamlit
st.pyplot(fig_line)

st.markdown('---')
st.info('¡El EDA está completo! Puedes modificar el código para explorar diferentes visualizaciones.')

