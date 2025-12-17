import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de página con estilo institucional
st.set_page_config(page_title="Dashboard P7 - Sustrend & MMA", layout="wide")

# Estilo CSS para cumplir con Normas Gráficas del MMA
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    h1 { color: #004488; font-family: 'Arial'; border-bottom: 3px solid #EF3340; }
    .stMetric { background-color: #ffffff; border: 1px solid #004488; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    # Nombre exacto del archivo que decidimos usar
    df = pd.read_csv('P7 Mapa de Replicabilidad Chile - Tabla de resultados procesados.csv')
    return df

try:
    df = load_data()

    # Encabezado con logos e identificación
    st.title("Mapa de Replicabilidad de Instrumentos Internacionales (P7)")
    st.caption("Consultoría Sustrend para la Subsecretaría del Medio Ambiente | ID: 608897-205-COT25")

    # Filtros interactivos (Interoperabilidad)
    col1, col2 = st.columns(2)
    with col1:
        filtro_pais = st.multiselect("Filtrar por País de Origen", options=df['País Origen (P2)'].unique(), default=df['País Origen (P2)'].unique())
    with col2:
        filtro_clase = st.multiselect("Filtrar por Clasificación Estratégica", options=df['Clasificación'].unique(), default=df['Clasificación'].unique())

    df_filtered = df[(df['País Origen (P2)'].isin(filtro_pais)) & (df['Clasificación'].isin(filtro_clase))]

    # Gráfico P7 Interactivo
    fig = px.scatter(
        df_filtered, 
        x="Score Factib. Chile", 
        y="Score Impacto (1-5)",
        text="ID (P2)",
        color="Clasificación",
        hover_name="Instrumento (Nombre Original/Local)",
        hover_data=["Categoría (P2)", "KPI Principal Afectado (P5)"],
        size=[15]*len(df_filtered),
        color_discrete_map={
            "🟢 Quick Win": "#2ECC71",
            "🔵 Estratégico": "#004488",
            "🟡 Táctico": "#F1C40F"
        },
        labels={"Score Factib. Chile": "Factibilidad en Chile (1-5)", "Score Impacto (1-5)": "Impacto Ambiental (1-5)"}
    )

    # Añadir líneas de cuadrantes según metodología P7
    fig.add_vline(x=3, line_dash="dash", line_color="gray", annotation_text="Umbral Factibilidad")
    fig.add_hline(y=3, line_dash="dash", line_color="gray", annotation_text="Umbral Impacto")

    fig.update_layout(
        plot_bgcolor='white',
        xaxis=dict(range=[0.5, 5.5], gridcolor='#e5e5e5'),
        yaxis=dict(range=[0.5, 5.5], gridcolor='#e5e5e5'),
        legend_title_text="Clasificación P7"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Tabla de datos detallada
    st.subheader("Ficha Técnica de Instrumentos")
    st.dataframe(df_filtered[["ID (P2)", "Instrumento (Nombre Original/Local)", "País Origen (P2)", "Score Factib. Chile", "Score Impacto (1-5)", "Clasificación"]], use_container_width=True)

except Exception as e:
    st.error(f"Error cargando el Dashboard: {e}")
    st.warning("Verifica que el nombre del archivo CSV en GitHub sea exactamente: P7 Mapa de Replicabilidad Chile - Tabla de resultados procesados.csv")
