import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuración de página con estilo institucional
st.set_page_config(page_title="Dashboard P7 - Sustrend & MMA", layout="wide")

# ESTILO CSS - FONDO BLANCO COMPLETO ABSOLUTO
st.markdown("""
    <style>
    /* ===== FONDO BLANCO ABSOLUTO PARA TODO ===== */
    .main {
        background-color: white !important;
    }
    
    /* Fondo blanco para todas las secciones de Streamlit */
    section[data-testid="stSidebar"], 
    section[data-testid="stSidebar"] > div,
    .stApp,
    .stApp > header,
    .stApp > div,
    .block-container,
    .element-container,
    .st-emotion-cache-18ni7ap,
    .st-emotion-cache-1dp5vir,
    .st-emotion-cache-zt5igj,
    .st-emotion-cache-16idsys,
    .st-emotion-cache-1oe5ca3,
    .st-emotion-cache-1y4p8pa,
    .st-emotion-cache-10trblm,
    .st-emotion-cache-1n76uvr,
    .st-emotion-cache-1r4qj8v,
    .st-emotion-cache-1wrcr25,
    .st-emotion-cache-uf99v8,
    .st-emotion-cache-12fmjuu,
    div[data-testid="stVerticalBlock"],
    div[data-testid="stHorizontalBlock"] {
        background-color: white !important;
    }
    
    /* Estilos para encabezados en azul marino */
    h1, h2, h3, h4, h5, h6 {
        color: #0f69b4 !important;
        font-family: 'Arial', sans-serif !important;
    }
    
    h1 {
        font-size: 28px !important;
        font-weight: 600 !important;
        border-bottom: 2px solid #0f69b4 !important;
        padding-bottom: 10px !important;
        margin-bottom: 20px !important;
        background-color: white !important;
    }
    
    h2 {
        font-size: 22px !important;
        font-weight: 500 !important;
        margin-top: 25px !important;
        margin-bottom: 15px !important;
        background-color: white !important;
    }
    
    h3 {
        font-size: 18px !important;
        font-weight: 500 !important;
        background-color: white !important;
    }
    
    /* Texto general en azul marino */
    .stText, .stMarkdown, .stCaption, p, div, span, label {
        color: #0f69b4 !important;
        background-color: white !important;
    }
    
    /* Inputs y selectores con fondo blanco */
    .stSelectbox, .stMultiselect, .stTextInput, .stNumberInput {
        background-color: white !important;
    }
    
    .stSelectbox label, .stMultiselect label {
        color: #0f69b4 !important;
        font-weight: 500 !important;
        background-color: white !important;
    }
    
    /* Fondo blanco para los widgets de selección */
    div[data-baseweb="select"] > div,
    div[data-baseweb="popover"] {
        background-color: white !important;
        border-color: #0f69b4 !important;
    }
    
    /* Tabla con fondo blanco */
    .stDataFrame {
        border: 1px solid #e0e0e0 !important;
        border-radius: 4px !important;
        background-color: white !important;
    }
    
    /* Divisores */
    .stDivider {
        border-color: #e0e0e0 !important;
        background-color: white !important;
    }
    
    /* Widget containers */
    .stWidget > div {
        background-color: white !important;
        border: none !important;
    }
    
    /* Métricas - completamente transparentes sobre blanco */
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
    
    /* Scrollbar personalizado */
    ::-webkit-scrollbar {
        width: 8px !important;
        height: 8px !important;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1 !important;
        border-radius: 4px !important;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #0f69b4 !important;
        border-radius: 4px !important;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #0c5490 !important;
    }
    
    /* Asegurar que todos los textos sean visibles */
    .stAlert, .stException {
        background-color: white !important;
        border-color: #0f69b4 !important;
        color: #0f69b4 !important;
    }
    
    /* Asegurar que el caption tenga fondo blanco */
    .stCaption {
        background-color: white !important;
        padding: 5px !important;
    }
    
    /* Override de cualquier otro fondo oscuro */
    * {
        background-color: white !important;
    }
    
    /* Fuerza el fondo blanco incluso en elementos inline */
    body, html {
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

    # ENCABEZADO CON TEXTO AZUL MARINO SOBRE FONDO BLANCO
    st.markdown("""
    <div style='background-color: white; padding: 10px; border-radius: 5px;'>
        <h1>Mapa de Replicabilidad de Instrumentos Internacionales</h1>
        <p style='color: #0f69b4; background-color: white;'>
            Consultoría Sustrend para la Subsecretaría del Medio Ambiente | ID: 608897-205-COT25
        </p>
    </div>
    """, unsafe_allow_html=True)

    # FILTROS INTERACTIVOS - CON FONDO BLANCO
    st.markdown("### Filtros de Análisis")
    
    # Crear contenedor blanco para los filtros
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            filtro_pais = st.multiselect(
                "Seleccionar País de Origen", 
                options=df['País Origen (P2)'].unique(), 
                default=df['País Origen (P2)'].unique(),
                help="Filtra los instrumentos por país de origen"
            )
        with col2:
            filtro_clase = st.multiselect(
                "Seleccionar Clasificación Estratégica", 
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
    st.markdown("### Análisis de Replicabilidad")
    
    # Contenedor blanco para el gráfico
    with st.container():
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
                "🟢 Quick Win": "#27AE60",  # Verde institucional
                "🔵 Estratégico": "#0f69b4",  # AZUL MARINO (#0f69b4)
                "🟡 Táctico": "#F39C12"   # Amarillo
            },
            labels={
                "Score Factib. Chile": "Factibilidad en Chile (1-5)", 
                "Score Impacto (1-5)": "Impacto Ambiental (1-5)"
            }
        )

        # LÍNEAS DE UMBRAL
        fig.add_vline(
            x=3, 
            line_dash="dash",
            line_width=1.5,
            line_color="#0f69b4",  # AZUL MARINO
            opacity=0.7
        )
        
        fig.add_hline(
            y=3, 
            line_dash="dash",
            line_width=1.5,
            line_color="#0f69b4",  # AZUL MARINO
            opacity=0.7
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

        # LAYOUT DEL GRÁFICO - Fondo blanco asegurado
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
                bgcolor="white",  # Fondo blanco sólido
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
            font=dict(size=10, color="#0f69b4", family="Arial"),
            bgcolor="white",
            bordercolor="#0f69b4",
            borderwidth=0.8,
            borderpad=4,
            xanchor="center",
            yanchor="bottom"
        )
        
        fig.add_annotation(
            x=5.4, y=3,
            text="<b>Umbral Impacto</b>",
            showarrow=False,
            font=dict(size=10, color="#0f69b4", family="Arial"),
            bgcolor="white",
            bordercolor="#0f69b4",
            borderwidth=0.8,
            borderpad=4,
            xanchor="left",
            yanchor="middle"
        )

        st.plotly_chart(fig, use_container_width=True)

    # ========== SECCIÓN DE MÉTRICAS ==========
    st.markdown("### Resumen de Clasificaciones")
    
    # Contenedor blanco para métricas
    with st.container():
        col1, col2, col3 = st.columns(3)
        
        with col1:
            quick_wins = len(df_filtered[df_filtered['Clasificación'] == '🟢 Quick Win'])
            st.markdown(f"""
            <div style="text-align: center; padding: 20px; background-color: white; border-radius: 6px; border: 1px solid #e0e0e0;">
                <div style="font-size: 36px; font-weight: bold; color: #27AE60; margin-bottom: 5px;">
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
            <div style="text-align: center; padding: 20px; background-color: white; border-radius: 6px; border: 1px solid #e0e0e0;">
                <div style="font-size: 36px; font-weight: bold; color: #0f69b4; margin-bottom: 5px;">
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
            <div style="text-align: center; padding: 20px; background-color: white; border-radius: 6px; border: 1px solid #e0e0e0;">
                <div style="font-size: 36px; font-weight: bold; color: #F39C12; margin-bottom: 5px;">
                    {tacticos}
                </div>
                <div style="font-size: 14px; font-weight: 600; color: #0f69b4; text-transform: uppercase; letter-spacing: 0.5px;">
                    Tácticos
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ========== TABLA DE DATOS ==========
    st.markdown("### Ficha Técnica de Instrumentos")
    
    # Contenedor blanco para la tabla
    with st.container():
        display_df = df_filtered[[
            "ID (P2)", 
            "Instrumento (Nombre Original/Local)", 
            "País Origen (P2)", 
            "Score Factib. Chile", 
            "Score Impacto (1-5)", 
            "Clasificación"
        ]].copy()
        
        display_df = display_df.sort_values("Score Impacto (1-5)", ascending=False)
        
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

    # ========== PIE DE PÁGINA ==========
    st.divider()
    st.markdown(
        "<div style='text-align: center; color: #0f69b4; font-size: 12px; background-color: white; padding: 10px;'>"
        "Dashboard P7 - Mapa de Replicabilidad de Instrumentos Internacionales | "
        "Consultoría Sustrend para el Ministerio del Medio Ambiente de Chile"
        "</div>",
        unsafe_allow_html=True
    )

except Exception as e:
    st.error(f"Error cargando el Dashboard: {e}")
    st.warning("Verifica que el nombre del archivo CSV sea: P7 Mapa de Replicabilidad Chile - Tabla de resultados procesados.csv")
