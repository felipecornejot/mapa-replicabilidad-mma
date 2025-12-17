import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. CONFIGURACIÓN DE PÁGINA Y ESTILO MMA
st.set_page_config(page_title="Dashboard Economía Circular - MMA", layout="wide")

# Aplicación de colores institucionales según Manual de Normas MMA
# Azul: #004488 | Rojo: #EF3340
st.markdown("""
    <style>
    .main { background-color: #f9f9f9; }
    .stMetric { background-color: #ffffff; border-left: 5px solid #004488; padding: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    h1 { color: #004488; border-bottom: 2px solid #EF3340; padding-bottom: 10px; }
    h2 { color: #004488; }
    .stButton>button { background-color: #004488; color: white; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 2. CARGA DE DATOS (Simulada con tus hallazgos de P2)
@st.cache_data
def load_data():
    data = [
        {"Case_ID": "DEU-01", "Nombre": "Ley Economía Circular", "Pais": "Alemania", "Replicabilidad": "Alta", "QuickWin": "No", "Tipo": "Regulatorio"},
        {"Case_ID": "DEU-03", "Nombre": "Ley Envases (EPR)", "Pais": "Alemania", "Replicabilidad": "Alta", "QuickWin": "Sí", "Tipo": "Datos/EPR"},
        {"Case_ID": "NLD-02", "Nombre": "Green Deals", "Pais": "Países Bajos", "Replicabilidad": "Media", "QuickWin": "Sí", "Tipo": "Cooperación"},
        {"Case_ID": "NLD-03", "Nombre": "Compra Pública Circular", "Pais": "Países Bajos", "Replicabilidad": "Alta", "QuickWin": "Sí", "Tipo": "Compra Pública"},
        {"Case_ID": "DNK-02", "Nombre": "Simbiosis Kalundborg", "Pais": "Dinamarca", "Replicabilidad": "Alta", "QuickWin": "Sí", "Tipo": "Cooperación"},
        {"Case_ID": "ESP-02", "Nombre": "Ley Residuos 7/2022", "Pais": "España", "Replicabilidad": "Alta", "QuickWin": "Sí", "Tipo": "Regulatorio"},
        {"Case_ID": "COL-02", "Nombre": "Esquema REP Envases", "Pais": "Colombia", "Replicabilidad": "Alta", "QuickWin": "Sí", "Tipo": "Regulatorio"},
        {"Case_ID": "COL-03", "Nombre": "Impuesto Bolsas Plásticas", "Pais": "Colombia", "Replicabilidad": "Alta", "QuickWin": "Sí", "Tipo": "Económico"},
    ]
    df = pd.DataFrame(data)
    
    # Mapeo numérico para el Mapa P7
    # Replicabilidad: Alta=3, Media=2, Baja=1
    # Impacto (basado en QuickWin): Sí=3, No=1.5 (Estratégico)
    rep_map = {"Alta": 3, "Media": 2, "Baja": 1}
    qw_map = {"Sí": 3, "No": 1.5}
    
    df['x_score'] = df['Replicabilidad'].map(rep_map)
    df['y_score'] = df['QuickWin'].map(qw_map)
    
    return df

df = load_data()

# 3. HEADER INSTITUCIONAL
col_logo1, col_logo2 = st.columns([1, 4])
with col_logo1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Logo_del_Ministerio_del_Medio_Ambiente_de_Chile.svg/1200px-Logo_del_Ministerio_del_Medio_Ambiente_de_Chile.svg.png", width=150)
with col_logo2:
    st.title("Sistema de Soporte para la Cooperación Internacional en Economía Circular")
    st.subheader("Visualizador de Hallazgos y Priorización (P7)")

# 4. FILTROS LATERALES
st.sidebar.header("Filtros de Análisis")
selected_pais = st.sidebar.multiselect("Seleccionar País", options=df['Pais'].unique(), default=df['Pais'].unique())
selected_tipo = st.sidebar.multiselect("Tipo de Instrumento", options=df['Tipo'].unique(), default=df['Tipo'].unique())

df_filtered = df[(df['Pais'].isin(selected_pais)) & (df['Tipo'].isin(selected_tipo))]

# 5. MATRIZ P7: MAPA DE PRIORIZACIÓN
st.header("📌 Mapa P7: Matriz de Priorización Estratégica")

# Creación del gráfico de burbujas/cuadrantes
fig_p7 = px.scatter(
    df_filtered, 
    x="x_score", 
    y="y_score",
    text="Case_ID",
    color="QuickWin",
    color_discrete_map={"Sí": "#EF3340", "No": "#004488"},
    size=[15]*len(df_filtered),
    hover_name="Nombre",
    labels={"x_score": "Nivel de Replicabilidad (Baja a Alta)", "y_score": "Potencial Quick Win / Impacto"},
    range_x=[0.5, 3.5],
    range_y=[0.5, 3.5]
)

# Añadir líneas de cuadrantes
fig_p7.add_shape(type="line", x0=2, y0=0.5, x1=2, y1=3.5, line=dict(color="Gray", dash="dash"))
fig_p7.add_shape(type="line", x0=0.5, y0=2.25, x1=3.5, y1=2.25, line=dict(color="Gray", dash="dash"))

# Anotaciones de Cuadrantes
fig_p7.add_annotation(x=3, y=3.2, text="QUICK WINS (Alta Prioridad)", showarrow=False, font=dict(color="#EF3340", size=12))
fig_p7.add_annotation(x=3, y=0.8, text="ESTRATÉGICOS (Largo Plazo)", showarrow=False, font=dict(color="#004488", size=12))

fig_p7.update_traces(textposition='top center')
fig_p7.update_layout(
    plot_bgcolor='white',
    height=600,
    margin=dict(l=20, r=20, t=40, b=20)
)

st.plotly_chart(fig_p7, use_container_width=True)

# 6. TABLA DE DETALLES (P2)
st.header("📊 Detalle de Hallazgos Replicables")
st.dataframe(df_filtered[["Case_ID", "Nombre", "Pais", "Tipo", "Replicabilidad", "QuickWin"]].sort_values(by="x_score", ascending=False), use_container_width=True)

# 7. FOOTER
st.markdown("---")
st.caption("Generado para el Ministerio del Medio Ambiente - Consultoría Sustrend 2024. Los datos cumplen con la trazabilidad de fuentes primarias y secundarias.")
