import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Configuración de página con estilo institucional
st.set_page_config(
    page_title="Mapa de Replicabilidad - MMA", 
    layout="wide",
    page_icon="🌍"
)

# ESTILO CSS - FONDO BLANCO COMPLETO SIN FRANJAS NEGRAS
st.markdown("""
    <style>
    /* ===== ELIMINAR FRANJA NEGRA DEL HEADER ===== */
    .stApp > header {
        background-color: white !important;
    }
    
    .stApp > header > div {
        background-color: white !important;
    }
    
    /* Eliminar cualquier fondo oscuro del header */
    .st-emotion-cache-18ni7ap {
        background-color: white !important;
    }
    
    /* ===== FONDO BLANCO PARA TODA LA PÁGINA ===== */
    .main {
        background-color: white !important;
    }
    
    .stApp {
        background-color: white !important;
    }
    
    .block-container {
        background-color: white !important;
        padding-top: 1rem !important;
    }
    
    /* Estilos para encabezados en azul marino */
    h1, h2, h3, h4, h5, h6 {
        color: #0f69b4 !important;
        font-family: 'Arial', sans-serif !important;
        background-color: white !important;
    }
    
    h1 {
        font-size: 32px !important;
        font-weight: 600 !important;
        border-bottom: 2px solid #0f69b4 !important;
        padding-bottom: 10px !important;
        margin-bottom: 15px !important;
    }
    
    h2 {
        font-size: 22px !important;
        font-weight: 500 !important;
        margin-top: 20px !important;
        margin-bottom: 10px !important;
    }
    
    h3 {
        font-size: 18px !important;
        font-weight: 500 !important;
    }
    
    /* Texto general en azul marino */
    .stMarkdown, .stCaption {
        color: #0f69b4 !important;
    }
    
    p, .stText {
        color: #0f69b4 !important;
    }
    
    /* ===== FILTROS TRANSPARENTES ===== */
    /* Labels de filtros */
    .stSelectbox label, .stMultiselect label {
        color: #0f69b4 !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        background-color: transparent !important;
    }
    
    /* Widgets de selección - TRANSPARENTES */
    div[data-baseweb="select"] > div,
    div[data-baseweb="popover"],
    div[data-baseweb="input"] {
        background-color: transparent !important;
        border: 1px solid #0f69b4 !important;
        border-radius: 4px !important;
    }
    
    /* Texto dentro de los filtros */
    div[data-baseweb="select"] span,
    div[data-baseweb="input"] input {
        color: #0f69b4 !important;
        background-color: transparent !important;
    }
    
    /* Opciones del dropdown */
    div[role="listbox"] li {
        color: #0f69b4 !important;
        background-color: white !important;
    }
    
    /* Tabla visible */
    .stDataFrame {
        border: 1px solid #e0e0e0 !important;
        border-radius: 4px !important;
        background-color: white !important;
    }
    
    /* Hacer visible las celdas de la tabla */
    .stDataFrame td, .stDataFrame th {
        background-color: white !important;
        color: #0f69b4 !important;
        border-color: #e0e0e0 !important;
    }
    
    /* Divisores */
    .stDivider {
        border-color: #e0e0e0 !important;
    }
    
    /* Métricas - estilo limpio */
    div[data-testid="stMetric"] {
        background-color: transparent !important;
        border: none !important;
        padding: 0 !important;
    }
    
    /* Labels de métricas en azul marino */
    div[data-testid="stMetricLabel"] {
        font-size: 14px !important;
        font-weight: bold !important;
        color: #0f69b4 !important;
        font-family: 'Arial', sans-serif !important;
        background-color: transparent !important;
    }
    
    /* Valores de métricas */
    div[data-testid="stMetricValue"] {
        font-size: 32px !important;
        font-weight: bold !important;
        font-family: 'Arial', sans-serif !important;
        background-color: transparent !important;
    }
    
    /* Métricas específicas */
    div[data-testid="stMetric"]:has(div[data-testid="stMetricLabel"]:contains("Quick Wins")) div[data-testid="stMetricValue"] {
        color: #27AE60 !important;
    }
    
    div[data-testid="stMetric"]:has(div[data-testid="stMetricLabel"]:contains("Estratégicos")) div[data-testid="stMetricValue"] {
        color: #0f69b4 !important;
    }
    
    div[data-testid="stMetric"]:has(div[data-testid="stMetricLabel"]:contains("Tácticos")) div[data-testid="stMetricValue"] {
        color: #F39C12 !important;
    }
    
    /* Asegurar que los contenedores sean visibles */
    .stPlotlyChart, .stDataFrame {
        visibility: visible !important;
        opacity: 1 !important;
    }
    
    /* Asegurar que los emojis de banderas sean visibles */
    .st-emotion-cache-16idsys span {
        background-color: transparent !important;
    }
    
    /* Placeholder color */
    ::placeholder {
        color: #0f69b4 !important;
        opacity: 0.7 !important;
    }
    
    /* Eliminar cualquier fondo de elementos de Streamlit */
    .st-emotion-cache-1dp5vir, 
    .st-emotion-cache-zt5igj,
    .st-emotion-cache-16idsys,
    .st-emotion-cache-1oe5ca3,
    .st-emotion-cache-1y4p8pa,
    .st-emotion-cache-10trblm {
        background-color: white !important;
    }
    
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv('P7 Mapa de Replicabilidad Chile - Tabla de resultados procesados.csv')
    return df

try:
    df = load_data()

    # ENCABEZADO
    st.title("Mapa de Replicabilidad de Instrumentos Internacionales")
    st.caption("Consultoría Sustrend para la Subsecretaría del Medio Ambiente | ID: 608897-205-COT25")

    # ========== EXPLICACIÓN INICIAL ==========
    st.markdown("---")
    st.markdown("""
    ### 📊 **Guía de Interpretación del Análisis**
    
    Este dashboard analiza la **replicabilidad en Chile** de instrumentos internacionales de gestión eficiente de recursos y economía circular. 
    La evaluación se basa en dos dimensiones clave:
    
    **1. Impacto Ambiental (1-5)**  
    *Puntuación que mide el potencial beneficio ambiental del instrumento si se implementara en Chile.*
    - **1-2**: Bajo impacto | **3**: Impacto moderado | **4-5**: Alto impacto
    
    **2. Factibilidad en Chile (1-5)**  
    *Puntuación que evalúa la viabilidad de implementación considerando el contexto chileno actual.*
    - **1-2**: Baja factibilidad | **3**: Factibilidad media | **4-5**: Alta factibilidad
    
    **Clasificación estratégica:**  
    • **🟢 Quick Wins**: Alto impacto, factibilidad media-baja (implementación rápida)  
    • **🔵 Estratégicos**: Alto impacto, alta factibilidad (prioridad máxima)  
    • **🟡 Tácticos**: Bajo impacto, alta factibilidad (implementación sencilla)
    """)

    # FILTROS INTERACTIVOS
    st.markdown("---")
    st.markdown("### Filtros de Análisis")
    st.markdown("*Seleccione los países y clasificaciones que desea analizar:*")
    
    col1, col2 = st.columns(2)
    with col1:
        filtro_pais = st.multiselect(
            "País de Origen", 
            options=df['País Origen (P2)'].unique(), 
            default=df['País Origen (P2)'].unique(),
            help="Filtra los instrumentos por país de origen"
        )
    with col2:
        filtro_clase = st.multiselect(
            "Clasificación Estratégica", 
            options=df['Clasificación'].unique(), 
            default=df['Clasificación'].unique(),
            help="Filtra los instrumentos por clasificación estratégica"
        )

    df_filtered = df[(df['País Origen (P2)'].isin(filtro_pais)) & 
                     (df['Clasificación'].isin(filtro_clase))]

    # CONFIGURACIÓN DE TAMAÑOS DE PUNTOS
    df_filtered['Size'] = 25  # Tamaño base
    df_filtered.loc[df_filtered['Clasificación'] == '🔵 Estratégico', 'Size'] = 35
    df_filtered.loc[df_filtered['Clasificación'] == '🟢 Quick Win', 'Size'] = 30

    # ========== GRÁFICO PRINCIPAL ==========
    st.markdown("---")
    st.markdown("### Análisis de Replicabilidad")
    
    st.markdown("""
    **📈 Interpretación del gráfico:**
    Cada punto representa un instrumento internacional evaluado. Su posición indica:
    - **Eje X**: Factibilidad de implementación en Chile (1 = baja, 5 = alta)
    - **Eje Y**: Impacto ambiental potencial (1 = bajo, 5 = alto)
    
    **📊 Líneas de referencia (rojo):**
    - **Línea vertical (3 en X)**: Umbral mínimo de factibilidad para considerar implementación
    - **Línea horizontal (3 en Y)**: Umbral mínimo de impacto ambiental para ser considerado relevante
    
    **🎯 Cuadrantes estratégicos:**
    1. **Superior derecho (🔵)**: Estratégicos - Alta prioridad
    2. **Superior izquierdo (🟢)**: Quick Wins - Oportunidades rápidas
    3. **Inferior derecho (🟡)**: Tácticos - Implementación sencilla
    4. **Inferior izquierdo**: Baja prioridad - Revisar en el largo plazo
    """)
    
    # Crear el gráfico
    fig = px.scatter(
        df_filtered, 
        x="Score Factib. Chile", 
        y="Score Impacto (1-5)",
        text="ID (P2)",
        color="Clasificación",
        hover_name="Instrumento (Nombre Original/Local)",
        hover_data={
            "País Origen (P2)": True,
            "Categoría (P2)": True,
            "KPI Principal Afectado (P5)": True,
            "Score Factib. Chile": ":.1f",
            "Score Impacto (1-5)": ":.1f"
        },
        size="Size",
        size_max=38,
        opacity=0.85,
        color_discrete_map={
            "🟢 Quick Win": "#27AE60",
            "🔵 Estratégico": "#0f69b4",
            "🟡 Táctico": "#F39C12"
        },
        labels={
            "Score Factib. Chile": "Factibilidad en Chile (1-5)", 
            "Score Impacto (1-5)": "Impacto Ambiental (1-5)"
        }
    )

    # LÍNEAS DE UMBRAL - ROJO GOBIERNO (#eb3c46)
    fig.add_vline(
        x=3, 
        line_dash="dash",
        line_width=1.8,
        line_color="#eb3c46",
        opacity=0.8
    )
    
    fig.add_hline(
        y=3, 
        line_dash="dash",
        line_width=1.8,
        line_color="#eb3c46",
        opacity=0.8
    )

    # ESTILO DE PUNTOS
    fig.update_traces(
        textposition='top center',
        marker=dict(
            line=dict(width=0.8, color='rgba(255,255,255,0.8)')
        ),
        textfont=dict(size=9, family="Arial", color="#0f69b4"),
        hovertemplate="<b>%{hovertext}</b><br>" +
                      "Factibilidad: %{x:.1f} | Impacto: %{y:.1f}<br>" +
                      "País: %{customdata[0]}<br>" +
                      "Categoría: %{customdata[1]}<br>" +
                      "KPI: %{customdata[2]}<br>" +
                      "<extra></extra>"
    )

    # LAYOUT DEL GRÁFICO
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(
            range=[0.5, 5.5], 
            gridcolor='rgba(15, 105, 180, 0.08)',
            gridwidth=0.5,
            showline=True,
            linecolor='#0f69b4',
            linewidth=1.2,
            showgrid=True,
            zeroline=False,
            title_font=dict(size=13, family="Arial", color="#0f69b4", weight="bold"),
            tickfont=dict(size=11, family="Arial", color="#0f69b4"),
            tickmode='linear',
            tick0=1,
            dtick=1,
            ticks="outside",
            ticklen=4,
            tickcolor='#0f69b4',
            title_text="Factibilidad en Chile (1-5)"
        ),
        yaxis=dict(
            range=[0.5, 5.5], 
            gridcolor='rgba(15, 105, 180, 0.08)',
            gridwidth=0.5,
            showline=True,
            linecolor='#0f69b4',
            linewidth=1.2,
            showgrid=True,
            zeroline=False,
            title_font=dict(size=13, family="Arial", color="#0f69b4", weight="bold"),
            tickfont=dict(size=11, family="Arial", color="#0f69b4"),
            tickmode='linear',
            tick0=1,
            dtick=1,
            ticks="outside",
            ticklen=4,
            tickcolor='#0f69b4',
            title_text="Impacto Ambiental (1-5)"
        ),
        legend=dict(
            title=dict(
                text="Clasificación", 
                font=dict(size=12, family="Arial", color="#0f69b4")
            ),
            font=dict(size=11, family="Arial", color="#0f69b4"),
            bordercolor="#0f69b4",
            borderwidth=0.8,
            bgcolor="white",
            x=1.02,
            xanchor="left",
            y=1,
            yanchor="top"
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=11,
            font_family="Arial",
            font_color="#0f69b4",
            bordercolor="#0f69b4"
        ),
        margin=dict(l=60, r=60, t=40, b=60),
        width=None,
        height=550,
        showlegend=True
    )

    # CUADRANTES CON COLORES SUTILES
    fig.add_shape(type="rect",
                  x0=0.5, y0=3, x1=3, y1=5.5,
                  fillcolor="rgba(39, 174, 96, 0.05)",
                  line=dict(width=0),
                  layer="below")
    
    fig.add_shape(type="rect",
                  x0=3, y0=3, x1=5.5, y1=5.5,
                  fillcolor="rgba(15, 105, 180, 0.05)",
                  line=dict(width=0),
                  layer="below")
    
    fig.add_shape(type="rect",
                  x0=0.5, y0=0.5, x1=3, y1=3,
                  fillcolor="rgba(243, 156, 18, 0.04)",
                  line=dict(width=0),
                  layer="below")

    # ETIQUETAS DE CUADRANTES
    quadrant_labels = [
        dict(
            x=1.75, y=4.5, 
            text="QUICK WINS", 
            font=dict(size=10, family="Arial", color="#27AE60", weight="bold"), 
            showarrow=False,
            bgcolor="white",
            bordercolor="#27AE60",
            borderwidth=0.5,
            borderpad=3
        ),
        dict(
            x=4.25, y=4.5, 
            text="ESTRATÉGICOS", 
            font=dict(size=10, family="Arial", color="#0f69b4", weight="bold"),
            showarrow=False,
            bgcolor="white",
            bordercolor="#0f69b4",
            borderwidth=0.5,
            borderpad=3
        ),
        dict(
            x=4.25, y=1.75, 
            text="TÁCTICOS", 
            font=dict(size=10, family="Arial", color="#F39C12", weight="bold"), 
            showarrow=False,
            bgcolor="white",
            bordercolor="#F39C12",
            borderwidth=0.5,
            borderpad=3
        )
    ]
    
    for label in quadrant_labels:
        fig.add_annotation(**label)

    # ETIQUETAS DE UMBRAL
    fig.add_annotation(
        x=3, y=5.4,
        text="<b>Umbral Factibilidad</b>",
        showarrow=False,
        font=dict(size=10, color="#eb3c46", family="Arial", weight="bold"),
        bgcolor="white",
        bordercolor="#eb3c46",
        borderwidth=0.8,
        borderpad=4,
        xanchor="center",
        yanchor="bottom"
    )
    
    fig.add_annotation(
        x=5.4, y=3,
        text="<b>Umbral Impacto</b>",
        showarrow=False,
        font=dict(size=10, color="#eb3c46", family="Arial", weight="bold"),
        bgcolor="white",
        bordercolor="#eb3c46",
        borderwidth=0.8,
        borderpad=4,
        xanchor="left",
        yanchor="middle"
    )

    # MOSTRAR EL GRÁFICO
    st.plotly_chart(fig, use_container_width=True)

    # ========== SECCIÓN DE MÉTRICAS ==========
    st.markdown("---")
    st.markdown("### Resumen de Clasificaciones")
    
    st.markdown("""
    **📊 Interpretación de las métricas:**
    Este resumen muestra la cantidad de instrumentos en cada categoría estratégica según los filtros aplicados.
    - **Quick Wins**: Instrumentos con alto impacto ambiental pero factibilidad media-baja. Prioridad para implementación rápida.
    - **Estratégicos**: Máxima prioridad - alto impacto y alta factibilidad. Implementación recomendada en el corto plazo.
    - **Tácticos**: Bajo impacto pero alta factibilidad. Útiles para ganar experiencia con baja inversión.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        quick_wins = len(df_filtered[df_filtered['Clasificación'] == '🟢 Quick Win'])
        st.markdown(f"""
        <div style="text-align: center; padding: 15px; background-color: white; border-radius: 6px; border: 1px solid #e0e0e0;">
            <div style="font-size: 32px; font-weight: bold; color: #27AE60; margin-bottom: 5px;">
                {quick_wins}
            </div>
            <div style="font-size: 14px; font-weight: 600; color: #0f69b4; text-transform: uppercase; letter-spacing: 0.5px;">
                Quick Wins
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        estrategicos = len(df_filtered[df_filtered['Clasificación'] == '🔵 Estratégico'])
        st.markdown(f"""
        <div style="text-align: center; padding: 15px; background-color: white; border-radius: 6px; border: 1px solid #e0e0e0;">
            <div style="font-size: 32px; font-weight: bold; color: #0f69b4; margin-bottom: 5px;">
                {estrategicos}
            </div>
            <div style="font-size: 14px; font-weight: 600; color: #0f69b4; text-transform: uppercase; letter-spacing: 0.5px;">
                Estratégicos
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        tacticos = len(df_filtered[df_filtered['Clasificación'] == '🟡 Táctico'])
        st.markdown(f"""
        <div style="text-align: center; padding: 15px; background-color: white; border-radius: 6px; border: 1px solid #e0e0e0;">
            <div style="font-size: 32px; font-weight: bold; color: #F39C12; margin-bottom: 5px;">
                {tacticos}
            </div>
            <div style="font-size: 14px; font-weight: 600; color: #0f69b4; text-transform: uppercase; letter-spacing: 0.5px;">
                Tácticos
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ========== TABLA DE DATOS ==========
    st.markdown("---")
    st.markdown("### Ficha Técnica de Instrumentos")
    
    st.markdown("""
    **📋 Interpretación de la tabla:**
    Esta tabla detalla cada instrumento evaluado. Las columnas incluyen:
    - **ID**: Identificador único del instrumento
    - **Instrumento**: Nombre del instrumento internacional
    - **País**: País de origen
    - **Factibilidad**: Puntuación de 1-5 (1=baja, 5=alta)
    - **Impacto**: Puntuación de 1-5 (1=bajo, 5=alto)
    - **Clasificación**: Categoría estratégica asignada
    
    **💡 Contexto según el informe:**
    La evaluación considera factores como madurez institucional, dependencia normativa, 
    complejidad de gobernanza, evidencia de resultados y compatibilidad con el marco chileno. 
    Los instrumentos con alta replicabilidad son aquellos que requieren ajustes menores y 
    se alinean con capacidades existentes en Chile.
    """)
    
    display_df = df_filtered[[
        "ID (P2)", 
        "Instrumento (Nombre Original/Local)", 
        "País Origen (P2)", 
        "Score Factib. Chile", 
        "Score Impacto (1-5)", 
        "Clasificación"
    ]].copy()
    
    display_df = display_df.sort_values("Score Impacto (1-5)", ascending=False)
    
    # Asegurar que la tabla sea visible
    st.dataframe(
        display_df,
        use_container_width=True,
        height=300,
        column_config={
            "ID (P2)": st.column_config.TextColumn("ID", width="small"),
            "Instrumento (Nombre Original/Local)": st.column_config.TextColumn("Instrumento", width="large"),
            "País Origen (P2)": st.column_config.TextColumn("País", width="medium"),
            "Score Factib. Chile": st.column_config.NumberColumn("Factibilidad", format="%.1f", width="small"),
            "Score Impacto (1-5)": st.column_config.NumberColumn("Impacto", format="%.1f", width="small"),
            "Clasificación": st.column_config.TextColumn("Clasificación", width="medium")
        }
    )

    # ========== PIE DE PÁGINA CON MEMBRETE PEQUEÑO ==========
    st.markdown("---")
    
    # Espaciado para el pie de página
    st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
    
    # Verificar si existe la imagen del membrete
    membrete_path = Path("membrete.png")
    
    # Contenedor para el membrete (esquina inferior izquierda)
    col1, col2, col3 = st.columns([3, 6, 3])
    
    with col1:
        if membrete_path.exists():
            # Mostrar el membrete pequeño en la esquina inferior izquierda
            st.markdown("""
            <div style="position: relative; bottom: 0; left: 0;">
                <img src="membrete.png" style="width: 120px; height: auto; opacity: 0.8;">
            </div>
            """, unsafe_allow_html=True)
        else:
            # Membrette textual pequeño
            st.markdown("""
            <div style="font-size: 8px; color: #0f69b4; opacity: 0.6; margin-top: 20px;">
                <p style="margin: 0; padding: 0; font-weight: bold;">Gobierno de Chile</p>
                <p style="margin: 0; padding: 0;">Ministerio del Medio Ambiente</p>
                <p style="margin: 0; padding: 0; font-size: 7px;">Dashboard de Replicabilidad</p>
            </div>
            """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error cargando el Dashboard: {e}")
    st.warning("Verifica que el nombre del archivo CSV sea: P7 Mapa de Replicabilidad Chile - Tabla de resultados procesados.csv")
