import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuración de página con estilo institucional
st.set_page_config(page_title="Dashboard P7 - Sustrend & MMA", layout="wide")

# Estilo CSS para cumplir con Normas Gráficas del MMA
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    h1 { color: #004488; font-family: 'Arial'; border-bottom: 3px solid #EF3340; }
    
    /* Quitar bordes de las métricas */
    div[data-testid="stMetric"] {
        background-color: transparent;
        border: none;
        padding: 0;
    }
    
    /* Estilo para los labels de métricas */
    div[data-testid="stMetricLabel"] {
        font-size: 14px;
        font-weight: bold;
        color: #333333;
        font-family: 'Arial';
    }
    
    /* Estilo para los valores de métricas */
    div[data-testid="stMetricValue"] {
        font-size: 32px;
        font-weight: bold;
        font-family: 'Arial';
    }
    
    /* Estilo específico para Quick Wins */
    div[data-testid="stMetric"]:has(div[data-testid="stMetricLabel"]:contains("Quick Wins")) div[data-testid="stMetricValue"] {
        color: #27AE60;
    }
    
    /* Estilo específico para Estratégicos */
    div[data-testid="stMetric"]:has(div[data-testid="stMetricLabel"]:contains("Estratégicos")) div[data-testid="stMetricValue"] {
        color: #004488;
    }
    
    /* Estilo específico para Tácticos */
    div[data-testid="stMetric"]:has(div[data-testid="stMetricLabel"]:contains("Tácticos")) div[data-testid="stMetricValue"] {
        color: #F39C12;
    }
    
    .stMetric { background-color: transparent; border: none; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv('P7 Mapa de Replicabilidad Chile - Tabla de resultados procesados.csv')
    return df

try:
    df = load_data()

    # Encabezado con logos e identificación
    st.title("Mapa de Replicabilidad de Instrumentos Internacionales")
    st.caption("Consultoría Sustrend para la Subsecretaría del Medio Ambiente | ID: 608897-205-COT25")

    # Filtros interactivos
    col1, col2 = st.columns(2)
    with col1:
        filtro_pais = st.multiselect("Filtrar por País de Origen", 
                                    options=df['País Origen (P2)'].unique(), 
                                    default=df['País Origen (P2)'].unique())
    with col2:
        filtro_clase = st.multiselect("Filtrar por Clasificación Estratégica", 
                                     options=df['Clasificación'].unique(), 
                                     default=df['Clasificación'].unique())

    df_filtered = df[(df['País Origen (P2)'].isin(filtro_pais)) & 
                     (df['Clasificación'].isin(filtro_clase))]

    # Mejorar el tamaño de los puntos según la importancia
    df_filtered['Size'] = 25  # Tamaño base
    df_filtered.loc[df_filtered['Clasificación'] == '🔵 Estratégico', 'Size'] = 35
    df_filtered.loc[df_filtered['Clasificación'] == '🟢 Quick Win', 'Size'] = 30

    # Gráfico con estética minimalista inspirada en tu referencia
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
            "🔵 Estratégico": "#004488",  # Azul MMA
            "🟡 Táctico": "#F39C12"   # Amarillo
        },
        labels={
            "Score Factib. Chile": "Factibilidad en Chile (1-5)", 
            "Score Impacto (1-5)": "Impacto Ambiental (1-5)"
        }
    )

    # Líneas de umbral estilo minimalista
    fig.add_vline(
        x=3, 
        line_dash="dash",
        line_width=1.5,
        line_color="#333333",
        opacity=0.7
    )
    
    fig.add_hline(
        y=3, 
        line_dash="dash",
        line_width=1.5,
        line_color="#333333",
        opacity=0.7
    )

    # Mejorar los textos de los puntos
    fig.update_traces(
        textposition='top center',
        marker=dict(
            line=dict(width=0.8, color='rgba(0,0,0,0.3)')
        ),
        textfont=dict(size=9, family="Arial", color="#333333"),
        hovertemplate="<b>%{hovertext}</b><br>" +
                      "Factibilidad: %{x:.1f} | Impacto: %{y:.1f}<br>" +
                      "País: %{customdata[0]}<br>" +
                      "Categoría: %{customdata[1]}<br>" +
                      "<extra></extra>"
    )

    # Layout minimalista al estilo de tu referencia
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(
            range=[0.5, 5.5], 
            gridcolor='rgba(0,0,0,0.08)',  # Grilla muy sutil
            gridwidth=0.5,
            showline=True,
            linecolor='rgba(0,0,0,0.3)',
            linewidth=1,
            showgrid=True,
            zeroline=False,
            title_font=dict(size=13, family="Arial", color="#333333"),
            tickfont=dict(size=11, family="Arial", color="#333333"),
            tickmode='linear',
            tick0=1,
            dtick=1,
            ticks="outside",
            ticklen=4,
            tickcolor='rgba(0,0,0,0.3)',
            title_text="Factibilidad en Chile (1-5)"
        ),
        yaxis=dict(
            range=[0.5, 5.5], 
            gridcolor='rgba(0,0,0,0.08)',  # Grilla muy sutil
            gridwidth=0.5,
            showline=True,
            linecolor='rgba(0,0,0,0.3)',
            linewidth=1,
            showgrid=True,
            zeroline=False,
            title_font=dict(size=13, family="Arial", color="#333333"),
            tickfont=dict(size=11, family="Arial", color="#333333"),
            tickmode='linear',
            tick0=1,
            dtick=1,
            ticks="outside",
            ticklen=4,
            tickcolor='rgba(0,0,0,0.3)',
            title_text="Impacto Ambiental (1-5)"
        ),
        legend=dict(
            title=dict(
                text="Clasificación", 
                font=dict(size=12, family="Arial", color="#333333")
            ),
            font=dict(size=11, family="Arial", color="#333333"),
            bordercolor="rgba(0,0,0,0.1)",
            borderwidth=0.5,
            bgcolor="rgba(255,255,255,0.8)",
            x=1.02,
            xanchor="left",
            y=1,
            yanchor="top"
        ),
        title=dict(
            text="Análisis Mapa de Replicabilidad",
            font=dict(size=16, family="Arial", color="#333333", weight="normal"),
            x=0.5,
            xanchor='center',
            y=0.95
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=11,
            font_family="Arial",
            font_color="#333333",
            bordercolor="rgba(0,0,0,0.1)"
        ),
        margin=dict(l=50, r=20, t=80, b=50),
        width=None,
        height=600,
        showlegend=True
    )

    # Añadir cuadrantes con colores de fondo muy sutiles (como en la referencia)
    fig.add_shape(type="rect",
                  x0=0.5, y0=3, x1=3, y1=5.5,
                  fillcolor="rgba(39, 174, 96, 0.03)",  # Quick Wins - verde muy tenue
                  line=dict(width=0),
                  layer="below")
    
    fig.add_shape(type="rect",
                  x0=3, y0=3, x1=5.5, y1=5.5,
                  fillcolor="rgba(0, 68, 136, 0.03)",  # Estratégicos - azul muy tenue
                  line=dict(width=0),
                  layer="below")
    
    fig.add_shape(type="rect",
                  x0=0.5, y0=0.5, x1=3, y1=3,
                  fillcolor="rgba(243, 156, 18, 0.02)",  # Tácticos - amarillo muy tenue
                  line=dict(width=0),
                  layer="below")

    # Añadir etiquetas de cuadrantes minimalistas
    quadrant_labels = [
        dict(x=1.75, y=4.5, text="QUICK WINS", 
             font=dict(size=10, family="Arial", color="#27AE60", weight="bold"), 
             showarrow=False,
             bgcolor="rgba(255,255,255,0.7)"),
        dict(x=4.25, y=4.5, text="ESTRATÉGICOS", 
             font=dict(size=10, family="Arial", color="#004488", weight="bold"), 
             showarrow=False,
             bgcolor="rgba(255,255,255,0.7)"),
        dict(x=4.25, y=1.75, text="TÁCTICOS", 
             font=dict(size=10, family="Arial", color="#F39C12", weight="bold"), 
             showarrow=False,
             bgcolor="rgba(255,255,255,0.7)")
    ]
    
    for label in quadrant_labels:
        fig.add_annotation(**label)

    # Añadir etiquetas de umbrales discretas
    fig.add_annotation(
        x=3, y=5.4,
        text="Umbral Factibilidad",
        showarrow=False,
        font=dict(size=10, color="#666666"),
        bgcolor="white",
        bordercolor="#e0e0e0",
        borderwidth=1,
        borderpad=3
    )
    
    fig.add_annotation(
        x=5.4, y=3,
        text="Umbral Impacto",
        showarrow=False,
        font=dict(size=10, color="#666666"),
        bgcolor="white",
        bordercolor="#e0e0e0",
        borderwidth=1,
        borderpad=3
    )

    st.plotly_chart(fig, use_container_width=True)

    # Sección de métricas resumen SIN recuadros
    st.subheader("Resumen de Clasificaciones")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        quick_wins = len(df_filtered[df_filtered['Clasificación'] == '🟢 Quick Win'])
        # Usamos markdown para crear una visualización limpia sin recuadros
        st.markdown(f"""
        <div style="text-align: center; padding: 20px 0;">
            <div style="font-size: 14px; font-weight: bold; color: #333333; margin-bottom: 8px;">
                Quick Wins
            </div>
            <div style="font-size: 32px; font-weight: bold; color: #27AE60;">
                {quick_wins}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        estrategicos = len(df_filtered[df_filtered['Clasificación'] == '🔵 Estratégico'])
        st.markdown(f"""
        <div style="text-align: center; padding: 20px 0;">
            <div style="font-size: 14px; font-weight: bold; color: #333333; margin-bottom: 8px;">
                Estratégicos
            </div>
            <div style="font-size: 32px; font-weight: bold; color: #004488;">
                {estrategicos}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        tacticos = len(df_filtered[df_filtered['Clasificación'] == '🟡 Táctico'])
        st.markdown(f"""
        <div style="text-align: center; padding: 20px 0;">
            <div style="font-size: 14px; font-weight: bold; color: #333333; margin-bottom: 8px;">
                Tácticos
            </div>
            <div style="font-size: 32px; font-weight: bold; color: #F39C12;">
                {tacticos}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Tabla de datos detallada
    st.subheader("Ficha Técnica de Instrumentos")
    st.dataframe(
        df_filtered[[
            "ID (P2)", 
            "Instrumento (Nombre Original/Local)", 
            "País Origen (P2)", 
            "Score Factib. Chile", 
            "Score Impacto (1-5)", 
            "Clasificación"
        ]].sort_values("Score Impacto (1-5)", ascending=False),
        use_container_width=True,
        height=300
    )

except Exception as e:
    st.error(f"Error cargando el Dashboard: {e}")
    st.warning("Verifica que el nombre del archivo CSV en GitHub sea exactamente: P7 Mapa de Replicabilidad Chile - Tabla de resultados procesados.csv")
