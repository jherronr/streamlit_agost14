# --- Configuración de la página ---
st.set_page_config(
    page_title="Tablero de Control de Riesgo en Salud",
    page_icon="🏥",
    layout="wide"
)

st.title('Tablero de Control de Riesgo en Salud 📊')
st.markdown('Este tablero muestra un análisis exploratorio de datos de riesgo en salud de una compañía, permitiendo al usuario filtrar y visualizar la información.')

# --- Generación de datos de salud aleatorios ---
@st.cache_data
def generar_datos_salud():
    """
    Genera un DataFrame de pandas con datos ficticios sobre salud de empleados.
    """
    # Genera 100 filas de datos de empleados
    num_empleados = 100
    
    # Crea datos aleatorios para la edad y departamento
    edades = np.random.randint(25, 65, size=num_empleados)
    departamentos = np.random.choice(['IT', 'Recursos Humanos', 'Ventas', 'Marketing', 'Finanzas'], size=num_empleados)

    # Crea datos aleatorios para los riesgos de salud (escalas de 0 a 1)
    riesgo_rcv = np.random.uniform(0.1, 0.8, size=num_empleados)
    riesgo_diabetes = np.random.uniform(0.05, 0.6, size=num_empleados)
    
    # Crea datos booleanos para el uso de la aplicación y estado activo
    uso_app = np.random.choice([True, False], size=num_empleados, p=[0.7, 0.3])
    activo = np.random.choice([True, False], size=num_empleados, p=[0.9, 0.1])
    
    # Combina todo en un DataFrame
    df = pd.DataFrame({
        'ID_Empleado': range(1, num_empleados + 1),
        'Edad': edades,
        'Departamento': departamentos,
        'Riesgo_RCV': riesgo_rcv,
        'Riesgo_Diabetes': riesgo_diabetes,
        'Uso_App': uso_app,
        'Activo': activo
    })
    
    return df

df = generar_datos_salud()

# --- Sección de KPIs (Métricas Clave) ---
st.header('Métricas Clave')

# Calcular los KPIs
total_empleados = df.shape[0]
usuarios_app = df[df['Uso_App'] == True].shape[0]
usuarios_activos = df[df['Activo'] == True].shape[0]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Total de Empleados", value=total_empleados)
with col2:
    st.metric(label="Usuarios de la App", value=usuarios_app)
with col3:
    st.metric(label="Usuarios Activos", value=usuarios_activos)

st.markdown('---')

# --- Sección de Filtros Interactivos ---
st.header('Filtros')

# Sliders para filtrar por edad
min_edad, max_edad = int(df['Edad'].min()), int(df['Edad'].max())
edad_seleccionada = st.slider(
    'Selecciona un rango de edad',
    min_edad, max_edad, (min_edad, max_edad)
)

# Multiselect para filtrar por departamento
departamentos_disponibles = df['Departamento'].unique()
departamentos_seleccionados = st.multiselect(
    'Selecciona uno o más departamentos',
    options=departamentos_disponibles,
    default=departamentos_disponibles
)

# Selectbox para elegir el tipo de riesgo a visualizar
riesgo_seleccionado = st.selectbox(
    'Selecciona el tipo de riesgo para la visualización',
    options=['Riesgo_RCV', 'Riesgo_Diabetes'],
    format_func=lambda x: x.replace('_', ' ')
)

# Aplicar filtros al DataFrame
df_filtrado = df[
    (df['Edad'] >= edad_seleccionada[0]) &
    (df['Edad'] <= edad_seleccionada[1]) &
    (df['Departamento'].isin(departamentos_seleccionados))
]

st.markdown('---')

# --- Sección de Visualizaciones ---
st.header('Visualizaciones Interactivas')

# 1. Gráfico de Barras: Riesgo promedio por departamento
st.subheader(f'Riesgo Promedio por Departamento (Tipo de Riesgo: {riesgo_seleccionado.replace("_", " ")})')

# Agrupar por departamento y calcular el riesgo promedio del riesgo seleccionado
riesgo_promedio_depto = df_filtrado.groupby('Departamento')[riesgo_seleccionado].mean().sort_values(ascending=False)

fig_bar, ax_bar = plt.subplots(figsize=(10, 6))
ax_bar.bar(riesgo_promedio_depto.index, riesgo_promedio_depto.values, color='teal')
ax_bar.set_title('Riesgo Promedio por Departamento', fontsize=16)
ax_bar.set_xlabel('Departamento', fontsize=12)
ax_bar.set_ylabel('Nivel de Riesgo Promedio', fontsize=12)
ax_bar.tick_params(axis='x', rotation=45)
ax_bar.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig_bar)


# 2. Histograma: Distribución de riesgo
st.subheader(f'Distribución de {riesgo_seleccionado.replace("_", " ")}')

fig_hist, ax_hist = plt.subplots(figsize=(10, 6))
ax_hist.hist(df_filtrado[riesgo_seleccionado], bins=15, color='purple', edgecolor='black')
ax_hist.set_title(f'Distribución del Nivel de {riesgo_seleccionado.replace("_", " ")}', fontsize=16)
ax_hist.set_xlabel('Nivel de Riesgo', fontsize=12)
ax_hist.set_ylabel('Frecuencia', fontsize=12)
ax_hist.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig_hist)

st.markdown('---')
st.info('¡El tablero está listo! Intenta usar los filtros para ver cómo cambian las visualizaciones.')
