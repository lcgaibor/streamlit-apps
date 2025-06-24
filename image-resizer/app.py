import streamlit as st
import zipfile
from PIL import Image
import io
import base64
from typing import List, Tuple, Dict
import os

# Configuración de la página
st.set_page_config(
    page_title="Redimensionador de Imágenes",
    page_icon="🖼️",
    layout="wide"
)

def resize_image(image: Image.Image, max_size: int = 480) -> Tuple[Image.Image, Tuple[int, int], int]:
    """
    Redimensiona una imagen manteniendo la proporción original.
    
    Args:
        image: Imagen PIL a redimensionar
        max_size: Tamaño máximo para ancho o alto
        
    Returns:
        Tupla con (imagen_redimensionada, nuevo_tamaño, peso_en_kb)
    """
    # Obtener dimensiones originales
    width, height = image.size
    
    # Calcular nueva dimensión manteniendo proporción
    if width > height:
        if width > max_size:
            new_width = max_size
            new_height = int((height * max_size) / width)
        else:
            new_width = width
            new_height = height
    else:
        if height > max_size:
            new_height = max_size
            new_width = int((width * max_size) / height)
        else:
            new_width = width
            new_height = height
    
    # Redimensionar imagen
    resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Calcular peso en KB
    img_byte_arr = io.BytesIO()
    resized_image.save(img_byte_arr, format='PNG', optimize=True)
    weight_kb = len(img_byte_arr.getvalue()) // 1024
    
    return resized_image, (new_width, new_height), weight_kb

def extract_images_from_zip(zip_file) -> Dict[str, Image.Image]:
    """
    Extrae todas las imágenes de un archivo ZIP.
    
    Args:
        zip_file: Archivo ZIP subido
        
    Returns:
        Diccionario con nombre_archivo: imagen_PIL
    """
    images = {}
    supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp')
    
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            for file_name in zip_ref.namelist():
                if file_name.lower().endswith(supported_formats):
                    try:
                        with zip_ref.open(file_name) as img_file:
                            image = Image.open(io.BytesIO(img_file.read()))
                            # Convertir a RGB si es necesario
                            if image.mode in ('RGBA', 'LA', 'P'):
                                image = image.convert('RGB')
                            images[file_name] = image
                    except Exception as e:
                        st.warning(f"No se pudo procesar la imagen {file_name}: {str(e)}")
    except Exception as e:
        st.error(f"Error al extraer el archivo ZIP: {str(e)}")
    
    return images

def create_download_link(img_data: bytes, filename: str) -> str:
    """
    Crea un enlace de descarga para una imagen.
    
    Args:
        img_data: Datos de la imagen en bytes
        filename: Nombre del archivo
        
    Returns:
        HTML con enlace de descarga
    """
    b64 = base64.b64encode(img_data).decode()
    href = f'<a href="data:image/png;base64,{b64}" download="{filename}">📥 Descargar {filename}</a>'
    return href

def create_zip_download(images_data: Dict[str, bytes]) -> bytes:
    """
    Crea un archivo ZIP con múltiples imágenes.
    
    Args:
        images_data: Diccionario con nombre_archivo: datos_imagen
        
    Returns:
        Datos del archivo ZIP
    """
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for filename, img_data in images_data.items():
            zip_file.writestr(filename, img_data)
    return zip_buffer.getvalue()

# Título principal
st.title("🖼️ Redimensionador de Imágenes")
st.markdown("---")

# Descripción
st.markdown("""
### Funcionalidades:
- 📁 Sube archivos de imagen individuales o un archivo ZIP con imágenes
- 🔄 Redimensiona automáticamente a máximo 480x480px manteniendo proporción
- 📊 Muestra el nuevo tamaño y peso de cada imagen
- 💾 Descarga imágenes individualmente o todas en un ZIP
""")

# Inicializar variables de sesión
if 'processed_images' not in st.session_state:
    st.session_state.processed_images = {}
if 'images_data' not in st.session_state:
    st.session_state.images_data = {}

# Sidebar para opciones de carga
st.sidebar.header("📤 Opciones de Carga")
upload_option = st.sidebar.radio(
    "Selecciona el tipo de archivo:",
    ["Imágenes individuales", "Archivo ZIP"]
)

# Área de carga de archivos
if upload_option == "Imágenes individuales":
    uploaded_files = st.file_uploader(
        "Selecciona las imágenes a redimensionar",
        type=['jpg', 'jpeg', 'png', 'bmp', 'gif', 'tiff', 'webp'],
        accept_multiple_files=True,
        key="individual_images"
    )
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} imagen(es) cargada(s)")
        
        # Procesar imágenes individuales
        images_to_process = {}
        for uploaded_file in uploaded_files:
            try:
                image = Image.open(uploaded_file)
                if image.mode in ('RGBA', 'LA', 'P'):
                    image = image.convert('RGB')
                images_to_process[uploaded_file.name] = image
            except Exception as e:
                st.error(f"Error al cargar {uploaded_file.name}: {str(e)}")

else:  # Archivo ZIP
    uploaded_zip = st.file_uploader(
        "Selecciona el archivo ZIP con imágenes",
        type=['zip'],
        key="zip_file"
    )
    
    if uploaded_zip:
        images_to_process = extract_images_from_zip(uploaded_zip)
        if images_to_process:
            st.success(f"✅ {len(images_to_process)} imagen(es) extraída(s) del ZIP")
        else:
            st.warning("⚠️ No se encontraron imágenes válidas en el archivo ZIP")

# Procesamiento y visualización
if 'images_to_process' in locals() and images_to_process:
    
    # Botón para procesar todas las imágenes
    if st.button("🔄 Procesar todas las imágenes", type="primary"):
        with st.spinner("Procesando imágenes..."):
            st.session_state.processed_images = {}
            st.session_state.images_data = {}
            
            for filename, image in images_to_process.items():
                try:
                    # Redimensionar imagen
                    resized_img, new_size, weight_kb = resize_image(image)
                    
                    # Guardar imagen procesada
                    img_byte_arr = io.BytesIO()
                    resized_img.save(img_byte_arr, format='PNG', optimize=True)
                    img_data = img_byte_arr.getvalue()
                    
                    # Almacenar en sesión
                    st.session_state.processed_images[filename] = {
                        'image': resized_img,
                        'original_size': image.size,
                        'new_size': new_size,
                        'weight_kb': weight_kb
                    }
                    st.session_state.images_data[filename] = img_data
                    
                except Exception as e:
                    st.error(f"Error al procesar {filename}: {str(e)}")
        
        st.success("✅ ¡Todas las imágenes han sido procesadas!")

# Mostrar imágenes procesadas
if st.session_state.processed_images:
    st.markdown("---")
    st.header("📋 Resultados del Procesamiento")
    
    # Crear columnas para la galería
    cols = st.columns(3)
    
    for idx, (filename, img_info) in enumerate(st.session_state.processed_images.items()):
        col = cols[idx % 3]
        
        with col:
            st.subheader(f"📷 {filename}")
            
            # Mostrar imagen redimensionada
            st.image(img_info['image'], caption=f"Redimensionada: {filename}")
            
            # Información de la imagen
            st.markdown(f"""
            **📏 Tamaño original:** {img_info['original_size'][0]} x {img_info['original_size'][1]} px
            
            **📐 Nuevo tamaño:** {img_info['new_size'][0]} x {img_info['new_size'][1]} px
            
            **⚖️ Peso:** {img_info['weight_kb']} KB
            """)
            
            # Botón de descarga individual
            if filename in st.session_state.images_data:
                img_data = st.session_state.images_data[filename]
                b64 = base64.b64encode(img_data).decode()
                
                # Crear nombre de archivo para descarga
                name_without_ext = os.path.splitext(filename)[0]
                download_filename = f"{name_without_ext}_480px.png"
                
                st.download_button(
                    label="📥 Descargar imagen",
                    data=img_data,
                    file_name=download_filename,
                    mime="image/png",
                    key=f"download_{idx}"
                )
            
            st.markdown("---")
    
    # Botón para descargar todas las imágenes en ZIP
    if len(st.session_state.images_data) > 1:
        st.markdown("### 📦 Descarga masiva")
        
        if st.button("🗜️ Preparar ZIP con todas las imágenes"):
            with st.spinner("Creando archivo ZIP..."):
                # Preparar datos para ZIP con nombres modificados
                zip_data = {}
                for filename, img_data in st.session_state.images_data.items():
                    name_without_ext = os.path.splitext(filename)[0]
                    new_filename = f"{name_without_ext}_480px.png"
                    zip_data[new_filename] = img_data
                
                zip_bytes = create_zip_download(zip_data)
                
                st.download_button(
                    label="📥 Descargar ZIP con todas las imágenes",
                    data=zip_bytes,
                    file_name="imagenes_redimensionadas_480px.zip",
                    mime="application/zip"
                )
        
        st.info("💡 **Tip:** Puedes descargar cada imagen individualmente o todas juntas en un archivo ZIP.")

# Información adicional en el sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("""
### ℹ️ Información
- **Resolución máxima:** 480x480 px
- **Formato de salida:** PNG optimizado
- **Proporción:** Se mantiene original
- **Formatos soportados:** JPG, PNG, BMP, GIF, TIFF, WebP
""")

st.sidebar.markdown("---")
st.sidebar.markdown("""
### 🔧 Características técnicas
- ✅ Compatible con Streamlit Cloud
- ✅ Procesamiento en memoria
- ✅ Sin archivos temporales
- ✅ Optimización automática
""")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>🖼️ Redimensionador de Imágenes </p>
</div>
""", unsafe_allow_html=True)