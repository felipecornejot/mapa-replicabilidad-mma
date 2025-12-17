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
    .stMetric { background-color: #ffffff; border: 1px solid #004488; }
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

    # Gráfico P7 Mejorado
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
        size_max=40,  # Aumentado para mejor visibilidad
        opacity=0.9,  # Mayor opacidad
        color_discrete_map={
            "🟢 Quick Win": "#27AE60",  # Verde más vibrante
            "🔵 Estratégico": "#2C3E50",  # Azul oscuro elegante
            "🟡 Táctico": "#F39C12"   # Amarillo más cálido
        },
        labels={
            "Score Factib. Chile": "Factibilidad en Chile (1-5)", 
            "Score Impacto (1-5)": "Impacto Ambiental (1-5)"
        }
    )

    # Añadir líneas de cuadrantes con mejor estilo
    fig.add_vline(
        x=3, 
        line_dash="solid",  # Cambiado a sólido para mejor visibilidad
        line_width=2.5,     # Más grueso
        line_color="#2C3E50",  # Negro/azul oscuro
        opacity=0.7,
        annotation=dict(
            text="Umbral Factibilidad",
            textangle=0,
            yanchor="top",
            y=1.02,  # Mover hacia arriba
            xanchor="center",
            font=dict(size=12, color="#2C3E50", family="Arial"),
            bgcolor="white",
            borderpad=4
        )
    )
    
    fig.add_hline(
        y=3, 
        line_dash="solid",  # Cambiado a sólido
        line_width=2.5,     # Más grueso
        line_color="#2C3E50",  # Negro/azul oscuro
        opacity=0.7,
        annotation=dict(
            text="Umbral Impacto",
            textangle=0,
            xanchor="right",
            x=1.02,  # Mover hacia la derecha
            yanchor="middle",
            font=dict(size=12, color="#2C3E50", family="Arial"),
            bgcolor="white",
            borderpad=4
        )
    )

    # Mejorar los textos de los puntos
    fig.update_traces(
        textposition='top center',
        marker=dict(
            line=dict(width=1, color='DarkSlateGrey')  # Borde para los puntos
        ),
        textfont=dict(size=10, family="Arial"),
        hovertemplate="<b>%{hovertext}</b><br><br>" +
                      "País: %{customdata[0]}<br>" +
                      "Categoría: %{customdata[1]}<br>" +
                      "KPI: %{customdata[2]}<br>" +
                      "Factibilidad: %{x:.1f}<br>" +
                      "Impacto: %{y:.1f}<br>" +
                      "<extra></extra>"
    )

    # Layout mejorado
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='#f8f9fa',  # Fondo suave
        xaxis=dict(
            range=[0.5, 5.5], 
            gridcolor='#e0e0e0',
            gridwidth=1,
            showline=True,
            linecolor='#b0b0b0',
            linewidth=1,
            title_font=dict(size=14, family="Arial", color="#2C3E50"),
            tickfont=dict(size=12, family="Arial")
        ),
        yaxis=dict(
            range=[0.5, 5.5], 
            gridcolor='#e0e0e0',
            gridwidth=1,
            showline=True,
            linecolor='#b0b0b0',
            linewidth=1,
            title_font=dict(size=14, family="Arial", color="#2C3E50"),
            tickfont=dict(size=12, family="Arial")
        ),
        legend=dict(
            title=dict(text="<b>Clasificación</b>", font=dict(size=12, family="Arial")),
            font=dict(size=11, family="Arial"),
            bordercolor="#e0e0e0",
            borderwidth=1,
            bgcolor="rgba(255,255,255,0.9)"
        ),
        title=dict(
            text="<b>Mapa de Replicabilidad - Análisis P7</b>",
            font=dict(size=18, family="Arial", color="#004488"),
            x=0.5,
            xanchor='center'
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial",
            bordercolor="#2C3E50"
        ),
        margin=dict(l=20, r=20, t=60, b=20),  # Mejor distribución
        width=None,  # Usará el ancho del contenedor
        height=600   # Altura fija para mejor aspecto
    )

    # Añadir cuadrantes con colores de fondo sutiles
    fig.add_shape(type="rect",
                  x0=0.5, y0=3, x1=3, y1=5.5,
                  fillcolor="rgba(46, 204, 113, 0.05)",  # Verde muy tenue
                  line=dict(width=0))
    
    fig.add_shape(type="rect",
                  x0=3, y0=3, x1=5.5, y1=5.5,
                  fillcolor="rgba(52, 152, 219, 0.05)",  # Azul muy tenue
                  line=dict(width=0))
    
    fig.add_shape(type="rect",
                  x0=0.5, y0=0.5, x1=3, y1=3,
                  fillcolor="rgba(231, 76, 60, 0.03)",  # Rojo muy tenue
                  line=dict(width=0))
    
    fig.add_shape(type="rect",
                  x0=3, y0=0.5, x1=5.5, y1=3,
                  fillcolor="rgba(243, 156, 18, 0.03)",  # Naranja muy tenue
                  line=dict(width=0))

    # Añadir etiquetas de cuadrantes
    quadrant_labels = [
        dict(x=1.75, y=4.5, text="<b>Quick Wins</b><br>(Alto Impacto, Baja Factibilidad)", 
             font=dict(size=10, color="#27AE60"), showarrow=False),
        dict(x=4.25, y=4.5, text="<b>Estratégicos</b><br>(Alto Impacto, Alta Factibilidad)", 
             font=dict(size=10, color="#2C3E50"), showarrow=False),
        dict(x=1.75, y=1.75, text="<b>Baja Prioridad</b><br>(Bajo Impacto, Baja Factibilidad)", 
             font=dict(size=10, color="#95A5A6"), showarrow=False),
        dict(x=4.25, y=1.75, text="<b>Tácticos</b><br>(Bajo Impacto, Alta Factibilidad)", 
             font=dict(size=10, color="#F39C12"), showarrow=False)
    ]
    
    for label in quadrant_labels:
        fig.add_annotation(**label)

    st.plotly_chart(fig, use_container_width=True)

    # Tabla de datos detallada
    st.subheader("Ficha Técnica de Instrumentos")
    st.dataframe(df_filtered[[
        "ID (P2)", 
        "Instrumento (Nombre Original/Local)", 
        "País Origen (P2)", 
        "Score Factib. Chile", 
        "Score Impacto (1-5)", 
        "Clasificación"
    ]], use_container_width=True)

except Exception as e:
    st.error(f"Error cargando el Dashboard: {e}")
    st.warning("Verifica que el nombre del archivo CSV en GitHub sea exactamente: P7 Mapa de Replicabilidad Chile - Tabla de resultados procesados.csv")
