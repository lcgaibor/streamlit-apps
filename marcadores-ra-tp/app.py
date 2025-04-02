import streamlit as st
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
import io
import base64
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="Generador de Marcadores RA - Tabla Periódica",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Aplicar estilo CSS personalizado
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    h1, h2, h3 {
        color: #1e3d59;
    }
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
    .element-info {
        background-color: #e6f2ff;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .marker-container {
        background-color: white;
        padding: 1rem;
        border-radius: 5px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class ElementARMarkerGenerator:
    def __init__(self):
        """
        Inicializa el generador de marcadores RA para elementos químicos.
        """
        self.marker_size = 400  # Tamaño del marcador en píxeles
        self.border_size = 40   # Tamaño del borde en píxeles
        
        # Elementos de la tabla periódica (símbolo, nombre, número atómico)
        self.elements = [
            ("H", "Hidrógeno", 1), ("He", "Helio", 2), ("Li", "Litio", 3), 
            ("Be", "Berilio", 4), ("B", "Boro", 5), ("C", "Carbono", 6),
            ("N", "Nitrógeno", 7), ("O", "Oxígeno", 8), ("F", "Flúor", 9),
            ("Ne", "Neón", 10), ("Na", "Sodio", 11), ("Mg", "Magnesio", 12),
            ("Al", "Aluminio", 13), ("Si", "Silicio", 14), ("P", "Fósforo", 15),
            ("S", "Azufre", 16), ("Cl", "Cloro", 17), ("Ar", "Argón", 18),
            ("K", "Potasio", 19), ("Ca", "Calcio", 20), ("Sc", "Escandio", 21),
            ("Ti", "Titanio", 22), ("V", "Vanadio", 23), ("Cr", "Cromo", 24),
            ("Mn", "Manganeso", 25), ("Fe", "Hierro", 26), ("Co", "Cobalto", 27),
            ("Ni", "Níquel", 28), ("Cu", "Cobre", 29), ("Zn", "Zinc", 30),
            ("Ga", "Galio", 31), ("Ge", "Germanio", 32), ("As", "Arsénico", 33),
            ("Se", "Selenio", 34), ("Br", "Bromo", 35), ("Kr", "Kriptón", 36),
            ("Rb", "Rubidio", 37), ("Sr", "Estroncio", 38), ("Y", "Itrio", 39),
            ("Zr", "Zirconio", 40), ("Nb", "Niobio", 41), ("Mo", "Molibdeno", 42),
            ("Tc", "Tecnecio", 43), ("Ru", "Rutenio", 44), ("Rh", "Rodio", 45),
            ("Pd", "Paladio", 46), ("Ag", "Plata", 47), ("Cd", "Cadmio", 48),
            ("In", "Indio", 49), ("Sn", "Estaño", 50), ("Sb", "Antimonio", 51),
            ("Te", "Telurio", 52), ("I", "Yodo", 53), ("Xe", "Xenón", 54),
            ("Cs", "Cesio", 55), ("Ba", "Bario", 56), ("La", "Lantano", 57),
            ("Ce", "Cerio", 58), ("Pr", "Praseodimio", 59), ("Nd", "Neodimio", 60),
            ("Pm", "Prometio", 61), ("Sm", "Samario", 62), ("Eu", "Europio", 63),
            ("Gd", "Gadolinio", 64), ("Tb", "Terbio", 65), ("Dy", "Disprosio", 66),
            ("Ho", "Holmio", 67), ("Er", "Erbio", 68), ("Tm", "Tulio", 69),
            ("Yb", "Iterbio", 70), ("Lu", "Lutecio", 71), ("Hf", "Hafnio", 72),
            ("Ta", "Tántalo", 73), ("W", "Wolframio", 74), ("Re", "Renio", 75),
            ("Os", "Osmio", 76), ("Ir", "Iridio", 77), ("Pt", "Platino", 78),
            ("Au", "Oro", 79), ("Hg", "Mercurio", 80), ("Tl", "Talio", 81),
            ("Pb", "Plomo", 82), ("Bi", "Bismuto", 83), ("Po", "Polonio", 84),
            ("At", "Astato", 85), ("Rn", "Radón", 86), ("Fr", "Francio", 87),
            ("Ra", "Radio", 88), ("Ac", "Actinio", 89), ("Th", "Torio", 90),
            ("Pa", "Protactinio", 91), ("U", "Uranio", 92), ("Np", "Neptunio", 93),
            ("Pu", "Plutonio", 94), ("Am", "Americio", 95), ("Cm", "Curio", 96),
            ("Bk", "Berkelio", 97), ("Cf", "Californio", 98), ("Es", "Einstenio", 99),
            ("Fm", "Fermio", 100), ("Md", "Mendelevio", 101), ("No", "Nobelio", 102),
            ("Lr", "Lawrencio", 103), ("Rf", "Rutherfordio", 104), ("Db", "Dubnio", 105),
            ("Sg", "Seaborgio", 106), ("Bh", "Bohrio", 107), ("Hs", "Hasio", 108),
            ("Mt", "Meitnerio", 109), ("Ds", "Darmstadtio", 110), ("Rg", "Roentgenio", 111),
            ("Cn", "Copernicio", 112), ("Nh", "Nihonio", 113), ("Fl", "Flerovio", 114),
            ("Mc", "Moscovio", 115), ("Lv", "Livermorio", 116), ("Ts", "Teneso", 117),
            ("Og", "Oganesón", 118)
        ]
    
    def generate_element_marker(self, symbol, name, atomic_number, show_symbol=False, show_atomic_number=True):
        """
        Genera un marcador RA único para un elemento químico.
        
        Args:
            symbol (str): Símbolo del elemento.
            name (str): Nombre del elemento.
            atomic_number (int): Número atómico del elemento.
            show_symbol (bool): Indica si se debe mostrar el símbolo del elemento.
            show_atomic_number (bool): Indica si se debe mostrar el número atómico.
            
        Returns:
            np.array: Imagen del marcador como array de NumPy.
        """
        # Crear una imagen base blanca
        img_size = self.marker_size + 2 * self.border_size
        img = Image.new('RGB', (img_size, img_size), color='white')
        draw = ImageDraw.Draw(img)
        
        # Dibujar un borde negro
        draw.rectangle(
            [(0, 0), (img_size-1, img_size-1)],
            outline='black',
            width=10
        )
        
        # Crear un patrón único basado en el número atómico
        np.random.seed(atomic_number)  # Usar número atómico como semilla
        
        # Generar una matriz de celdas para el marcador
        grid_size = 5
        cell_size = (self.marker_size) // grid_size
        
        # Dibujar celdas negras basadas en un patrón único
        for i in range(grid_size):
            for j in range(grid_size):
                # Generar un valor aleatorio determinista basado en el número atómico
                if np.random.random() > 0.5:
                    x0 = self.border_size + i * cell_size
                    y0 = self.border_size + j * cell_size
                    x1 = x0 + cell_size
                    y1 = y0 + cell_size
                    draw.rectangle([(x0, y0), (x1, y1)], fill='black')
        
        # Agregar información del elemento al marcador si se solicita
        if show_symbol:
            try:
                font_symbol = ImageFont.truetype("arial.ttf", 72)
            except IOError:
                # Si no se encuentra la fuente Arial, usar fuente por defecto
                font_symbol = ImageFont.load_default()
            
            # Agregar símbolo centrado en la celda central
            center_cell_x = self.border_size + (grid_size // 2) * cell_size
            center_cell_y = self.border_size + (grid_size // 2) * cell_size
            
            # Obtener tamaño del texto para centrarlo
            symbol_width = draw.textlength(symbol, font=font_symbol)
            
            # Dibujar un fondo blanco para el símbolo
            draw.rectangle(
                [(center_cell_x - 40, center_cell_y - 40), 
                 (center_cell_x + 40, center_cell_y + 40)],
                fill='white'
            )
            
            # Dibujar el símbolo
            draw.text(
                (center_cell_x - symbol_width/2, center_cell_y - 36),
                symbol,
                fill='black',
                font=font_symbol
            )
        
        # Agregar número atómico en la esquina
        if show_atomic_number:
            try:
                font_info = ImageFont.truetype("arial.ttf", 24)
            except IOError:
                font_info = ImageFont.load_default()
                
            draw.text(
                (self.border_size + 10, self.border_size + 10),
                str(atomic_number),
                fill='black',
                font=font_info
            )
        
        # Convertir a matriz numpy y a escala de grises
        marker_array = np.array(img)
        marker_gray = cv2.cvtColor(marker_array, cv2.COLOR_RGB2GRAY)
        
        return marker_gray

    def get_element_by_atomic_number(self, atomic_number):
        """Obtiene un elemento por su número atómico."""
        for element in self.elements:
            if element[2] == atomic_number:
                return element
        return None

def get_image_download_link(img, filename, text):
    """Genera un enlace para descargar una imagen."""
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/png;base64,{img_str}" download="{filename}">{text}</a>'
    return href

def main():
    st.title("🧪 Generador de Marcadores RA para la Tabla Periódica")
    
    st.markdown("""
    Esta aplicación genera marcadores de Realidad Aumentada (RA) únicos para cada elemento 
    de la tabla periódica. Cada marcador se genera utilizando el número atómico del elemento 
    como semilla, lo que garantiza un patrón único y reconocible.
    """)

    # Inicializar generador
    generator = ElementARMarkerGenerator()
    
    # Sidebar para opciones
    st.sidebar.header("Opciones de Configuración")
    
    # Selector de elemento
    st.sidebar.subheader("Selecciona un Elemento")
    
    # Crear opciones de selección por categoría
    element_categories = {
        "Metales alcalinos": [3, 11, 19, 37, 55, 87],
        "Metales alcalinotérreos": [4, 12, 20, 38, 56, 88],
        "Metales de transición": list(range(21, 31)) + list(range(39, 49)) + list(range(72, 81)) + list(range(104, 113)),
        "Lantánidos": list(range(57, 72)),
        "Actínidos": list(range(89, 104)),
        "Otros metales": [13, 31, 49, 50, 81, 82, 83, 113, 114, 115, 116],
        "Metaloides": [5, 14, 32, 33, 51, 52, 84],
        "No metales": [1, 6, 7, 8, 9, 15, 16, 17, 34, 35, 53],
        "Gases nobles": [2, 10, 18, 36, 54, 86, 118]
    }
    
    category_select = st.sidebar.selectbox(
        "Categoría de elementos",
        options=list(element_categories.keys()),
        index=0
    )
    
    # Obtener elementos de la categoría seleccionada
    category_elements = element_categories[category_select]
    
    # Crear lista de opciones para el selectbox
    element_options = []
    for atomic_num in category_elements:
        element = generator.get_element_by_atomic_number(atomic_num)
        if element:
            symbol, name, _ = element
            element_options.append(f"{atomic_num}: {name} ({symbol})")
    
    # Seleccionar elemento de la categoría
    selected_element_str = st.sidebar.selectbox(
        "Elemento",
        options=element_options,
        index=0 if element_options else None
    )
    
    # Permitir también búsqueda por número atómico directo
    st.sidebar.subheader("O ingresa un número atómico")
    atomic_number_input = st.sidebar.number_input(
        "Número atómico (1-118)",
        min_value=1,
        max_value=118,
        value=1
    )
    
    # Opciones de visualización
    st.sidebar.subheader("Opciones de Visualización")
    show_symbol = st.sidebar.checkbox("Mostrar símbolo del elemento", value=False)
    show_atomic_number = st.sidebar.checkbox("Mostrar número atómico", value=True)
    
    # Botón para generar
    generate_button = st.sidebar.button("Generar Marcador")
    
    # Determinar el número atómico del elemento seleccionado
    if generate_button:
        if selected_element_str and ":" in selected_element_str:
            selected_atomic_number = int(selected_element_str.split(':')[0])
        else:
            selected_atomic_number = atomic_number_input
    else:
        # Usar el valor predeterminado al inicio
        selected_atomic_number = atomic_number_input
    
    # Obtener el elemento seleccionado
    selected_element = generator.get_element_by_atomic_number(selected_atomic_number)
    
    if selected_element:
        symbol, name, atomic_number = selected_element
        
        # Crear un layout de dos columnas
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Marcador RA generado")
            
            # Generar marcador
            marker = generator.generate_element_marker(
                symbol, 
                name, 
                atomic_number, 
                show_symbol=show_symbol,
                show_atomic_number=show_atomic_number
            )
            
            # Convertir a formato de imagen
            pil_img = Image.fromarray(marker)
            
            # Mostrar imagen (usando use_container_width en lugar de use_column_width)
            st.image(pil_img, caption=f"Marcador RA para {name}", use_container_width=True)
            
            # Enlace para descargar
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"marcador_{atomic_number:03d}_{symbol}_{timestamp}.png"
            st.markdown(get_image_download_link(pil_img, filename, "📥 Descargar Marcador"), unsafe_allow_html=True)
        
        with col2:
            st.subheader("Información del Elemento")
            
            # Mostrar información del elemento
            st.markdown(f"""
            <div class="element-info">
                <h3 style="text-align: center; color: black;">{symbol}</h3>
                <h2 style="text-align: center; color: black;">{name}</h2>
                <p style="text-align: center; color: black;"><strong>Número atómico:</strong> {atomic_number}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Explicar cómo funciona el marcador (versión condensada)
            st.markdown("""
            ### Sobre el marcador RA
            
            * Se utiliza el algoritmo Mersenne Twister.
            * El algoritmo aplica transformaciones matemáticas, desplazamientos de bits y XOR.
            * Este método garantiza que se generará exactamente el mismo patrón.
            * La probabilidad de que cada celda sea negra o blanca se determina comparando el valor generado con 0.5.
            """)
        
        # Instrucciones de uso
        st.markdown("""
        ### Cómo usar el marcador
        
        1. Descarga la imagen del marcador
        2. Imprímela en papel o muéstrala en una pantalla
        3. Utiliza una aplicación compatible con marcadores AR para escanear la imagen
        4. La aplicación reconocerá el patrón único y mostrará información o contenido 3D relacionado con el elemento
        """)
    
    # Pie de página
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Acerca de")
    st.sidebar.markdown("""
    Desarrollado por lcgaibor.  
    GitHub: [lcgaibor's apps](https://github.com/lcgaibor/streamlit-apps)
    """)

if __name__ == "__main__":
    main()