import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import base64

# Configuración de la página
st.set_page_config(
    page_title="Generador de Símbolos Químicos",
    page_icon="⚛️",
    layout="centered"
)

# Diccionario de elementos químicos con su símbolo y número atómico
ELEMENTOS = {
    "Hidrógeno": {"simbolo": "H", "numero": 1},
    "Helio": {"simbolo": "He", "numero": 2},
    "Litio": {"simbolo": "Li", "numero": 3},
    "Berilio": {"simbolo": "Be", "numero": 4},
    "Boro": {"simbolo": "B", "numero": 5},
    "Carbono": {"simbolo": "C", "numero": 6},
    "Nitrógeno": {"simbolo": "N", "numero": 7},
    "Oxígeno": {"simbolo": "O", "numero": 8},
    "Flúor": {"simbolo": "F", "numero": 9},
    "Neón": {"simbolo": "Ne", "numero": 10},
    "Sodio": {"simbolo": "Na", "numero": 11},
    "Magnesio": {"simbolo": "Mg", "numero": 12},
    "Aluminio": {"simbolo": "Al", "numero": 13},
    "Silicio": {"simbolo": "Si", "numero": 14},
    "Fósforo": {"simbolo": "P", "numero": 15},
    "Azufre": {"simbolo": "S", "numero": 16},
    "Cloro": {"simbolo": "Cl", "numero": 17},
    "Argón": {"simbolo": "Ar", "numero": 18},
    "Potasio": {"simbolo": "K", "numero": 19},
    "Calcio": {"simbolo": "Ca", "numero": 20},
    "Escandio": {"simbolo": "Sc", "numero": 21},
    "Titanio": {"simbolo": "Ti", "numero": 22},
    "Vanadio": {"simbolo": "V", "numero": 23},
    "Cromo": {"simbolo": "Cr", "numero": 24},
    "Manganeso": {"simbolo": "Mn", "numero": 25},
    "Hierro": {"simbolo": "Fe", "numero": 26},
    "Cobalto": {"simbolo": "Co", "numero": 27},
    "Níquel": {"simbolo": "Ni", "numero": 28},
    "Cobre": {"simbolo": "Cu", "numero": 29},
    "Zinc": {"simbolo": "Zn", "numero": 30},
    "Galio": {"simbolo": "Ga", "numero": 31},
    "Germanio": {"simbolo": "Ge", "numero": 32},
    "Arsénico": {"simbolo": "As", "numero": 33},
    "Selenio": {"simbolo": "Se", "numero": 34},
    "Bromo": {"simbolo": "Br", "numero": 35},
    "Kriptón": {"simbolo": "Kr", "numero": 36},
    "Rubidio": {"simbolo": "Rb", "numero": 37},
    "Estroncio": {"simbolo": "Sr", "numero": 38},
    "Itrio": {"simbolo": "Y", "numero": 39},
    "Zirconio": {"simbolo": "Zr", "numero": 40},
    "Niobio": {"simbolo": "Nb", "numero": 41},
    "Molibdeno": {"simbolo": "Mo", "numero": 42},
    "Tecnecio": {"simbolo": "Tc", "numero": 43},
    "Rutenio": {"simbolo": "Ru", "numero": 44},
    "Rodio": {"simbolo": "Rh", "numero": 45},
    "Paladio": {"simbolo": "Pd", "numero": 46},
    "Plata": {"simbolo": "Ag", "numero": 47},
    "Cadmio": {"simbolo": "Cd", "numero": 48},
    "Indio": {"simbolo": "In", "numero": 49},
    "Estaño": {"simbolo": "Sn", "numero": 50},
    "Antimonio": {"simbolo": "Sb", "numero": 51},
    "Telurio": {"simbolo": "Te", "numero": 52},
    "Yodo": {"simbolo": "I", "numero": 53},
    "Xenón": {"simbolo": "Xe", "numero": 54},
    "Cesio": {"simbolo": "Cs", "numero": 55},
    "Bario": {"simbolo": "Ba", "numero": 56},
    "Lantano": {"simbolo": "La", "numero": 57},
    "Cerio": {"simbolo": "Ce", "numero": 58},
    "Praseodimio": {"simbolo": "Pr", "numero": 59},
    "Neodimio": {"simbolo": "Nd", "numero": 60},
    "Promecio": {"simbolo": "Pm", "numero": 61},
    "Samario": {"simbolo": "Sm", "numero": 62},
    "Europio": {"simbolo": "Eu", "numero": 63},
    "Gadolinio": {"simbolo": "Gd", "numero": 64},
    "Terbio": {"simbolo": "Tb", "numero": 65},
    "Disprosio": {"simbolo": "Dy", "numero": 66},
    "Holmio": {"simbolo": "Ho", "numero": 67},
    "Erbio": {"simbolo": "Er", "numero": 68},
    "Tulio": {"simbolo": "Tm", "numero": 69},
    "Iterbio": {"simbolo": "Yb", "numero": 70},
    "Lutecio": {"simbolo": "Lu", "numero": 71},
    "Hafnio": {"simbolo": "Hf", "numero": 72},
    "Tantalio": {"simbolo": "Ta", "numero": 73},
    "Wolframio": {"simbolo": "W", "numero": 74},
    "Renio": {"simbolo": "Re", "numero": 75},
    "Osmio": {"simbolo": "Os", "numero": 76},
    "Iridio": {"simbolo": "Ir", "numero": 77},
    "Platino": {"simbolo": "Pt", "numero": 78},
    "Oro": {"simbolo": "Au", "numero": 79},
    "Mercurio": {"simbolo": "Hg", "numero": 80},
    "Talio": {"simbolo": "Tl", "numero": 81},
    "Plomo": {"simbolo": "Pb", "numero": 82},
    "Bismuto": {"simbolo": "Bi", "numero": 83},
    "Polonio": {"simbolo": "Po", "numero": 84},
    "Astato": {"simbolo": "At", "numero": 85},
    "Radón": {"simbolo": "Rn", "numero": 86},
    "Francio": {"simbolo": "Fr", "numero": 87},
    "Radio": {"simbolo": "Ra", "numero": 88},
    "Actinio": {"simbolo": "Ac", "numero": 89},
    "Torio": {"simbolo": "Th", "numero": 90},
    "Protactinio": {"simbolo": "Pa", "numero": 91},
    "Uranio": {"simbolo": "U", "numero": 92},
    "Neptunio": {"simbolo": "Np", "numero": 93},
    "Plutonio": {"simbolo": "Pu", "numero": 94},
    "Americio": {"simbolo": "Am", "numero": 95},
    "Curio": {"simbolo": "Cm", "numero": 96},
    "Berkelio": {"simbolo": "Bk", "numero": 97},
    "Californio": {"simbolo": "Cf", "numero": 98},
    "Einstenio": {"simbolo": "Es", "numero": 99},
    "Fermio": {"simbolo": "Fm", "numero": 100},
    "Mendelevio": {"simbolo": "Md", "numero": 101},
    "Nobelio": {"simbolo": "No", "numero": 102},
    "Lawrencio": {"simbolo": "Lr", "numero": 103},
    "Rutherfordio": {"simbolo": "Rf", "numero": 104},
    "Dubnio": {"simbolo": "Db", "numero": 105},
    "Seaborgio": {"simbolo": "Sg", "numero": 106},
    "Bohrio": {"simbolo": "Bh", "numero": 107},
    "Hassio": {"simbolo": "Hs", "numero": 108},
    "Meitnerio": {"simbolo": "Mt", "numero": 109},
    "Darmstadtio": {"simbolo": "Ds", "numero": 110},
    "Roentgenio": {"simbolo": "Rg", "numero": 111},
    "Copernicio": {"simbolo": "Cn", "numero": 112},
    "Nihonio": {"simbolo": "Nh", "numero": 113},
    "Flerovio": {"simbolo": "Fl", "numero": 114},
    "Livermorio": {"simbolo": "Lv", "numero": 116},
    "Oganesón": {"simbolo": "Og", "numero": 118}
}

# Crear diccionario inverso: número atómico -> elemento
NUMERO_A_ELEMENTO = {datos["numero"]: {"nombre": nombre, "simbolo": datos["simbolo"]} 
                     for nombre, datos in ELEMENTOS.items()}

def crear_imagen_elemento(simbolo, numero_atomico=None, mostrar_numero=False):
    """
    Crea una imagen PNG del símbolo del elemento químico.
    
    Args:
        simbolo (str): Símbolo químico del elemento
        numero_atomico (int): Número atómico del elemento
        mostrar_numero (bool): Si mostrar o no el número atómico
    
    Returns:
        PIL.Image: Imagen generada
    """
    # Dimensiones de la imagen
    ancho, alto = 400, 400
    
    # Crear imagen con fondo blanco
    imagen = Image.new('RGB', (ancho, alto), 'white')
    draw = ImageDraw.Draw(imagen)
    
    # Intentar cargar fuentes con diferentes tamaños según la longitud del símbolo
    longitud_simbolo = len(simbolo)
    
    # Ajustar tamaño de fuente según longitud del símbolo para que ocupe casi toda la imagen
    if longitud_simbolo == 1:
        tamano_fuente = 280  # Símbolos de una letra (H, C, N, etc.)
    elif longitud_simbolo == 2:
        tamano_fuente = 200  # Símbolos de dos letras (He, Li, etc.)
    else:
        tamano_fuente = 150  # Símbolos de tres letras (muy raros)
    
    try:
        # Intentar cargar fuentes con el tamaño calculado
        try:
            fuente_simbolo = ImageFont.truetype("arial.ttf", tamano_fuente)
        except:
            try:
                fuente_simbolo = ImageFont.truetype("DejaVuSans-Bold.ttf", tamano_fuente)
            except:
                # Crear una fuente por defecto más grande
                fuente_simbolo = ImageFont.load_default()
        
        # Fuente para el número atómico
        try:
            fuente_numero = ImageFont.truetype("arial.ttf", 60)
        except:
            try:
                fuente_numero = ImageFont.truetype("DejaVuSans.ttf", 60)
            except:
                fuente_numero = ImageFont.load_default()
    except:
        # Usar fuente por defecto si no se encuentran otras
        fuente_simbolo = ImageFont.load_default()
        fuente_numero = ImageFont.load_default()
    
    # Obtener dimensiones del texto del símbolo usando textbbox
    bbox_simbolo = draw.textbbox((0, 0), simbolo, font=fuente_simbolo)
    ancho_simbolo = bbox_simbolo[2] - bbox_simbolo[0]
    alto_simbolo = bbox_simbolo[3] - bbox_simbolo[1]
    
    # Obtener el offset del texto (importante para centrado perfecto)
    offset_x = bbox_simbolo[0]
    offset_y = bbox_simbolo[1]
    
    # Calcular posición para centrar el símbolo PERFECTAMENTE
    if mostrar_numero and numero_atomico:
        # Si se muestra el número, centrar el símbolo
        x_simbolo = (ancho - ancho_simbolo) // 2 - offset_x
        y_simbolo = (alto - alto_simbolo) // 2 - offset_y
        
        # Dibujar el número atómico en la esquina superior derecha
        numero_str = str(numero_atomico)
        bbox_numero = draw.textbbox((0, 0), numero_str, font=fuente_numero)
        ancho_numero = bbox_numero[2] - bbox_numero[0]
        
        # Posicionar el número en la esquina superior derecha con margen
        x_numero = ancho - ancho_numero - 20
        y_numero = 20
        
        draw.text((x_numero, y_numero), numero_str, fill='black', font=fuente_numero)
    else:
        # Solo símbolo, PERFECTAMENTE centrado compensando el offset
        x_simbolo = (ancho - ancho_simbolo) // 2 - offset_x
        y_simbolo = (alto - alto_simbolo) // 2 - offset_y
    
    # Dibujar el símbolo
    draw.text((x_simbolo, y_simbolo), simbolo, fill='black', font=fuente_simbolo)
    
    return imagen

def imagen_a_bytes(imagen):
    """
    Convierte una imagen PIL a bytes para descarga.
    
    Args:
        imagen (PIL.Image): Imagen a convertir
    
    Returns:
        bytes: Imagen en formato bytes
    """
    buffer = io.BytesIO()
    imagen.save(buffer, format='PNG')
    return buffer.getvalue()

def main():
    # Título de la aplicación
    st.title("⚛️ Generador de Símbolos de Elementos Químicos")
    st.markdown("---")
    
    # Descripción
    st.markdown("""
    Esta aplicación genera imágenes minimalistas de símbolos de elementos químicos.
    Selecciona un elemento y elige si quieres mostrar solo el símbolo o incluir el número atómico.
    """)
    
    # Crear dos columnas para la interfaz
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("⚙️ Configuración")
        
        # Modo de selección
        modo_seleccion = st.radio(
            "🔍 Modo de selección:",
            options=["Por elemento químico", "Por número atómico"],
            index=0,
            help="Elige cómo quieres seleccionar el elemento"
        )
        
        if modo_seleccion == "Por elemento químico":
            # Selector de elemento
            elemento_seleccionado = st.selectbox(
                "Selecciona un elemento químico:",
                options=list(ELEMENTOS.keys()),
                index=0
            )
            
            # Obtener datos del elemento seleccionado
            datos_elemento = ELEMENTOS[elemento_seleccionado]
            simbolo_final = datos_elemento["simbolo"]
            numero_final = datos_elemento["numero"]
            
        else:  # Por número atómico
            # Selector de número atómico
            numero_seleccionado = st.number_input(
                " Ingresa un número atómico:",
                min_value=1,
                max_value=118,
                value=1,
                step=1,
                help="Número atómico (1-118)"
            )
            
            # Obtener datos del número seleccionado
            if numero_seleccionado in NUMERO_A_ELEMENTO:
                elemento_info = NUMERO_A_ELEMENTO[numero_seleccionado]
                simbolo_final = elemento_info["simbolo"]
                numero_final = numero_seleccionado
                elemento_seleccionado = elemento_info["nombre"]
            else:
                # Fallback (aunque no debería ocurrir)
                simbolo_final = "X"
                numero_final = numero_seleccionado
                elemento_seleccionado = "Elemento desconocido"
        
        # Opción para mostrar número atómico
        mostrar_numero = st.radio(
            "¿Qué deseas mostrar?",
            options=["Solo símbolo", "Símbolo y número atómico"],
            index=0
        )
        
        # Mostrar información del elemento seleccionado
        st.info(f"**Elemento:** {elemento_seleccionado}  \n**Símbolo:** {simbolo_final}  \n**Número atómico:** {numero_final}")
        
        # Botón para generar imagen
        if st.button("🧪 Generar Imagen", type="primary"):
            # Determinar qué mostrar
            incluir_numero = mostrar_numero == "Símbolo y número atómico"
            numero_a_usar = numero_final if incluir_numero else None
            
            # Generar imagen
            with st.spinner("Generando imagen..."):
                imagen = crear_imagen_elemento(
                    simbolo=simbolo_final,
                    numero_atomico=numero_a_usar,
                    mostrar_numero=incluir_numero
                )
                
                # Guardar en session state
                st.session_state.imagen_generada = imagen
                st.session_state.elemento_actual = elemento_seleccionado
                st.session_state.simbolo_actual = simbolo_final
                st.session_state.numero_usado = numero_a_usar if incluir_numero else None
    
    with col2:
        st.subheader("🖼️ Vista Previa")
        
        # Mostrar imagen si existe
        if hasattr(st.session_state, 'imagen_generada') and st.session_state.imagen_generada:
            st.image(
                st.session_state.imagen_generada,
                caption=f"Símbolo: {st.session_state.simbolo_actual}",
                use_container_width=True
            )
            
            # Botón de descarga
            imagen_bytes = imagen_a_bytes(st.session_state.imagen_generada)
            
            st.download_button(
                label="⬇️ Descargar PNG",
                data=imagen_bytes,
                file_name=nombre_archivo,
                mime="image/png",
                type="secondary"
            )
            
            # Información adicional
            info_texto = f"**Elemento:** {st.session_state.elemento_actual}"
            if hasattr(st.session_state, 'numero_usado') and st.session_state.numero_usado:
                info_texto += f" | **Número atómico:** {st.session_state.numero_usado}"
            
            st.info(info_texto)
            
        else:
            st.info("Haz clic en 'Generar Imagen' para crear tu símbolo químico.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
        <small>Generador de Símbolos Químicos </small>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
