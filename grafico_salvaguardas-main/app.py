import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(
    page_title="Análisis de Riesgos",
    page_icon="📊",
    layout="wide"
)

# Datos de ejemplo (puedes reemplazarlos con tus datos reales)
data = {
    'Activo': ['HW01', 'HW02', 'HW03', 'HW04', 'AUX01', 'AUX02', 'AUX03', 'AUX04', 'AUX05', 'AUX06'],
    'Nombre': [
        'Cisco Catalyst 9200', 'MikroTik CCR1036', 'Dell PowerEdge R750', 
        'Fortinet FortiGate 100F', 'Daikin TXC60D', 'APC Basic Rack PDU',
        'Leviton Cat6 Patch Panel', 'Fan Panel 2U para rack', 'E91 10-20kVA UPS',
        'Nobreak Senoidal Bivolt'
    ],
    'RD': [6, 5, 5, 5, 8, 6, 4, 9, 3, 4],
    'RI': [8, 5, 5, 5, 8, 6, 6, 8, 4, 8],
    'RC': [8, 5, 5, 3, 10, 6, 4, 4, 3, 3],
    'RA': [10, 5, 5, 5, 6, 8, 10, 5, 3, 4],
    'RT': [4, 3, 7, 3, 4, 6, 4, 7, 5, 4]
}

# Crear DataFrame
df = pd.DataFrame(data)

# Título principal
st.title("📊 Dashboard de Análisis de Riesgos")
st.markdown("---")

# Descripción
st.markdown("""
Este dashboard muestra el análisis de riesgos para diferentes activos, considerando:
- 🔵 RD: Riesgo en Disponibilidad
- 🟢 RI: Riesgo en Integridad
- 🟡 RC: Riesgo en Confidencialidad
- 🟠 RA: Riesgo en Autenticidad
- 🔴 RT: Riesgo en Trazabilidad
""")

# Crear dos columnas
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Comparación de Todos los Activos")
    
    # Crear gráfico de barras agrupadas
    fig = go.Figure()
    
    # Añadir barras para cada tipo de riesgo
    colors = ['#1f77b4', '#2ca02c', '#ffeb3b', '#ff7f0e', '#d62728']
    risk_types = ['RD', 'RI', 'RC', 'RA', 'RT']
    
    for risk, color in zip(risk_types, colors):
        fig.add_trace(go.Bar(
            name=risk,
            x=df['Activo'],
            y=df[risk],
            text=df[risk],
            textposition='auto',
            marker_color=color
        ))

    fig.update_layout(
        barmode='group',
        height=500,
        template='plotly_white',
        title_x=0.5,
        showlegend=True,
        legend_title="Tipos de Riesgo",
        xaxis_title="Activos",
        yaxis_title="Nivel de Riesgo",
        hovermode='x unified'
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Detalles por Activo")
    
    # Selector de activo
    selected_asset = st.selectbox(
        "Selecciona un activo para ver sus detalles:",
        df['Activo'].tolist(),
        format_func=lambda x: f"{x} - {df[df['Activo']==x]['Nombre'].iloc[0]}"
    )
    
    # Filtrar datos para el activo seleccionado
    asset_data = df[df['Activo'] == selected_asset].iloc[0]
    
    # Crear gráfico de radar
    fig_radar = go.Figure()
    
    fig_radar.add_trace(go.Scatterpolar(
        r=[asset_data['RD'], asset_data['RI'], asset_data['RC'], 
        asset_data['RA'], asset_data['RT']],
        theta=['RD', 'RI', 'RC', 'RA', 'RT'],
        fill='toself',
        name=asset_data['Activo']
    ))
    
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )),
        showlegend=False,
        height=400
    )
    
    st.plotly_chart(fig_radar, use_container_width=True)
    
    # Mostrar valores específicos
    st.markdown("### Valores de Riesgo")
    col_stats1, col_stats2 = st.columns(2)
    
    with col_stats1:
        st.metric("Disponibilidad", asset_data['RD'])
        st.metric("Integridad", asset_data['RI'])
        st.metric("Confidencialidad", asset_data['RC'])
        
    with col_stats2:
        st.metric("Autenticidad", asset_data['RA'])
        st.metric("Trazabilidad", asset_data['RT'])

# Añadir footer
st.markdown("---")
st.markdown("Dashboard creado con Streamlit y Plotly")