import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuración de página con estilo institucional
st.set_page_config(page_title="Dashboard P7 - Sustrend & MMA", layout="wide")

# Estilo CSS minimalista
st.markdown("""
    <style>
    .main { background-color: white; }
    h1 { 
        color: #183a68; 
        font-family: 'Calibri, Arial'; 
        font-size: 28px;
        font-weight: 600;
        border-bottom: 2px solid #eb3c46;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    h2, h3 { 
        color: #4e4e4c; 
        font-family: 'Calibri, Arial';
        font-weight: 500;
    }
    .st-emotion-cache-16txtl3 {
        padding-top: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv('P7 Mapa de Replicabilidad Chile - Tabla de resultados procesados.csv')
    return df

try:
    df = load_data()

    # Encabezado limpio
    col_title, col_logo = st.columns([4, 1])
    with col_title:
        st.title("Análisis Mapa de Replicabilidad")
        st.caption("Consultoría Sustrend | MMA Chile | ID: 608897-205-COT25")

    # Filtros en línea minimalistas
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        filtro_pais = st.multiselect(
            "País de Origen", 
            options=df['País Origen (P2)'].unique(), 
            default=df['País Origen (P2)'].unique(),
            placeholder="Seleccionar países..."
        )
    with col2:
        filtro_clase = st.multiselect(
            "Clasificación", 
            options=df['Clasificación'].unique(), 
            default=df['Clasificación'].unique(),
            placeholder="Seleccionar clasificaciones..."
        )

    df_filtered = df[(df['País Origen (P2)'].isin(filtro_pais)) & 
                     (df['Clasificación'].isin(filtro_clase))]

    # Convertir clasificaciones a nombres más cortos para el gráfico
    df_filtered = df_filtered.copy()
    df_filtered['Clasif_Corta'] = df_filtered['Clasificación'].replace({
        '🟢 Quick Win': 'Quick Win',
        '🔵 Estratégico': 'Estratégico', 
        '🟡 Táctico': 'Táctico'
    })

    # Crear tamaño para los puntos (basado en importancia)
    df_filtered['Tamaño'] = 20  # Base
    df_filtered.loc[df_filtered['Clasificación'] == '🔵 Estratégico', 'Tamaño'] = 35
    df_filtered.loc[df_filtered['Clasificación'] == '🟢 Quick Win', 'Tamaño'] = 30
    df_filtered.loc[df_filtered['Clasificación'] == '🟡 Táctico', 'Tamaño'] = 25

    # Gráfico principal - estilo minimalista inspirado en la referencia
    fig = px.scatter(
        df_filtered,
        x="Score Factib. Chile",
        y="Score Impacto (1-5)",
        size="Tamaño",
        color="Clasif_Corta",
        hover_name="Instrumento (Nombre Original/Local)",
        hover_data={
            "País Origen (P2)": True,
            "Categoría (P2)": True,
            "Score Factib. Chile": ":.1f",
            "Score Impacto (1-5)": ":.1f"
        },
        size_max=45,
        color_discrete_sequence=["#0f69b4", "#eb3c46", "#183a68"]  # Azul, Rojo, Azul oscuro
    )

    # Líneas de cuadrantes - estilo punto discreto
    x0, y0 = 3, 3
    fig.add_vline(
        x=x0, 
        line_width=1.2, 
        line_dash="dot", 
        opacity=0.55, 
        line_color="#4e4e4c"
    )
    fig.add_hline(
        y=y0, 
        line_width=1.2, 
        line_dash="dot", 
        opacity=0.55, 
        line_color="#4e4e4c"
    )

    # Estética clara - opacidad y bordes suaves
    fig.update_traces(
        marker=dict(
            opacity=0.82, 
            line=dict(width=1.2, color="rgba(255,255,255,0.95)"),
            sizemode='diameter'
        ),
        textfont=dict(family="Calibri, Arial", size=10, color="#4e4e4c"),
        hovertemplate=(
            "<b>%{hovertext}</b><br>"
            "Factibilidad: %{x:.1f} | Impacto: %{y:.1f}<br>"
            "País: %{customdata[0]}<br>"
            "Categoría: %{customdata[1]}<br>"
            "<extra></extra>"
        )
    )

    # Layout minimalista tipo "simple_white"
    fig.update_layout(
        template="simple_white",
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="Calibri, Arial", size=13, color="#4e4e4c"),
        margin=dict(l=65, r=35, t=60, b=65),
        legend_title_text="",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5,
            font=dict(size=12),
            itemclick="toggleothers",
            itemdoubleclick="toggle"
        ),
        title=dict(
            text="",
            font=dict(size=16, color="#183a68", family="Calibri, Arial")
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Calibri, Arial",
            font_color="#4e4e4c",
            bordercolor="#e1e1e1"
        )
    )

    # Ejes 1–5 con ticks enteros
    ticks = [1, 2, 3, 4, 5]
    fig.update_xaxes(
        title="Factibilidad en Chile (1–5)",
        range=[0.8, 5.2],
        tickmode="array", 
        tickvals=ticks,
        gridcolor="rgba(233,233,233,0.9)",
        linecolor="#c9c9c9",
        linewidth=1,
        showgrid=True,
        zeroline=False,
        tickfont=dict(size=12),
        title_font=dict(size=13, color="#4e4e4c")
    )
    
    fig.update_yaxes(
        title="Impacto Ambiental (1–5)",
        range=[0.8, 5.2],
        tickmode="array", 
        tickvals=ticks,
        gridcolor="rgba(233,233,233,0.9)",
        linecolor="#c9c9c9",
        linewidth=1,
        showgrid=True,
        zeroline=False,
        tickfont=dict(size=12),
        title_font=dict(size=13, color="#4e4e4c")
    )

    # Títulos de cuadrantes (posición similar a la referencia)
    quadrant_annotations = [
        dict(
            x=4.2, y=4.6, 
            text="<b>Alto Impacto<br>Alta Factibilidad</b>",
            showarrow=False,
            font=dict(size=11, color="#183a68", family="Calibri, Arial"),
            align="center",
            bgcolor="rgba(255,255,255,0.7)",
            bordercolor="#e1e1e1",
            borderwidth=1,
            borderpad=4
        ),
        dict(
            x=1.8, y=4.6, 
            text="<b>Alto Impacto<br>Baja Factibilidad</b>",
            showarrow=False,
            font=dict(size=11, color="#0f69b4", family="Calibri, Arial"),
            align="center",
            bgcolor="rgba(255,255,255,0.7)",
            bordercolor="#e1e1e1",
            borderwidth=1,
            borderpad=4
        ),
        dict(
            x=1.8, y=1.4, 
            text="<b>Bajo Impacto<br>Baja Factibilidad</b>",
            showarrow=False,
            font=dict(size=11, color="#4e4e4c", family="Calibri, Arial"),
            align="center",
            bgcolor="rgba(255,255,255,0.7)",
            bordercolor="#e1e1e1",
            borderwidth=1,
            borderpad=4
        ),
        dict(
            x=4.2, y=1.4, 
            text="<b>Bajo Impacto<br>Alta Factibilidad</b>",
            showarrow=False,
            font=dict(size=11, color="#4e4e4c", family="Calibri, Arial"),
            align="center",
            bgcolor="rgba(255,255,255,0.7)",
            bordercolor="#e1e1e1",
            borderwidth=1,
            borderpad=4
        )
    ]
    
    for ann in quadrant_annotations:
        fig.add_annotation(ann)

    # Display del gráfico
    st.plotly_chart(fig, use_container_width=True)

    # Estadísticas resumen minimalistas (sin recuadros)
    st.divider()
    st.markdown("### Resumen de Clasificaciones")
    
    col_qw, col_est, col_tac = st.columns(3)
    
    with col_qw:
        quick_wins = len(df_filtered[df_filtered['Clasificación'] == '🟢 Quick Win'])
        st.markdown(f"""
        <div style="text-align: center;">
            <div style="font-size: 24px; font-weight: 600; color: #0f69b4; margin-bottom: 4px;">
                {quick_wins}
            </div>
            <div style="font-size: 13px; color: #4e4e4c; font-weight: 500; letter-spacing: 0.5px;">
                QUICK WINS
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_est:
        estrategicos = len(df_filtered[df_filtered['Clasificación'] == '🔵 Estratégico'])
        st.markdown(f"""
        <div style="text-align: center;">
            <div style="font-size: 24px; font-weight: 600; color: #eb3c46; margin-bottom: 4px;">
                {estrategicos}
            </div>
            <div style="font-size: 13px; color: #4e4e4c; font-weight: 500; letter-spacing: 0.5px;">
                ESTRATÉGICOS
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_tac:
        tacticos = len(df_filtered[df_filtered['Clasificación'] == '🟡 Táctico'])
        st.markdown(f"""
        <div style="text-align: center;">
            <div style="font-size: 24px; font-weight: 600; color: #183a68; margin-bottom: 4px;">
                {tacticos}
            </div>
            <div style="font-size: 13px; color: #4e4e4c; font-weight: 500; letter-spacing: 0.5px;">
                TÁCTICOS
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Tabla de datos - minimalista
    st.divider()
    st.markdown("### Ficha Técnica de Instrumentos")
    
    # Preparar datos para tabla
    display_df = df_filtered[[
        "ID (P2)", 
        "Instrumento (Nombre Original/Local)", 
        "País Origen (P2)", 
        "Score Factib. Chile", 
        "Score Impacto (1-5)", 
        "Clasif_Corta"
    ]].copy()
    
    # Renombrar columnas para mejor visualización
    display_df.columns = ["ID", "Instrumento", "País", "Factibilidad", "Impacto", "Clasificación"]
    
    # Ordenar por impacto descendente
    display_df = display_df.sort_values("Impacto", ascending=False)
    
    # Mostrar tabla con estilo minimalista
    st.dataframe(
        display_df,
        use_container_width=True,
        height=350,
        column_config={
            "ID": st.column_config.TextColumn(width="small"),
            "Instrumento": st.column_config.TextColumn(width="large"),
            "País": st.column_config.TextColumn(width="medium"),
            "Factibilidad": st.column_config.NumberColumn(format="%.1f"),
            "Impacto": st.column_config.NumberColumn(format="%.1f"),
            "Clasificación": st.column_config.TextColumn(width="medium")
        }
    )

    # Pie de página minimalista
    st.divider()
    st.caption("Dashboard P7 - Mapa de Replicabilidad de Instrumentos Internacionales | v1.0")

except Exception as e:
    st.error(f"Error cargando el Dashboard: {e}")
    st.warning("Verifica que el nombre del archivo CSV sea: P7 Mapa de Replicabilidad Chile - Tabla de resultados procesados.csv")
