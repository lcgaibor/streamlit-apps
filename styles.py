import streamlit as st

def apply_styles():
    """
    Aplica los estilos CSS personalizados a la aplicación Streamlit.
    """
    st.markdown("""
    <style>
        /* Estilos generales de la página */
        .main {
            background-color: #f8f9fa;
        }
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        /* Estilos de títulos */
        h1, h2, h3 {
            color: #1e3d59;
        }
        
        /* Estilos de botones */
        .stButton>button {
            background-color: #1e3d59;
            color: white;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #2e5d79;
        }
        
        /* Estilos de información del elemento */
        .element-info {
            background-color: #e6f2ff;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        /* Estilos del contenedor del marcador */
        .marker-container {
            background-color: white;
            padding: 1rem;
            border-radius: 5px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin: 1rem 0;
        }
        
        /* Estilos para enlaces de descarga */
        a[download] {
            display: inline-block;
            background-color: #4CAF50;
            color: white;
            padding: 10px 15px;
            text-align: center;
            text-decoration: none;
            font-size: 16px;
            border-radius: 5px;
            margin: 10px 0;
            transition: background-color 0.3s;
        }
        
        a[download]:hover {
            background-color: #45a049;
        }
        
        /* Estilo para la sidebar */
        .sidebar .sidebar-content {
            background-color: #f0f2f6;
        }
        
        /* Estilo para los selectbox */
        .stSelectbox {
            margin-bottom: 15px;
        }
        
        /* Estilo para los checkboxes */
        .stCheckbox {
            margin-bottom: 10px;
        }
        
        /* Estilo para la información */
        .info-box {
            background-color: #f8f9fa;
            border-left: 5px solid #1e3d59;
            padding: 10px 15px;
            margin: 10px 0;
        }
    </style>
    """, unsafe_allow_html=True)