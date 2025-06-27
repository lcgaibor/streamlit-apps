import streamlit as st
import zipfile
import io
from PIL import Image
import base64
import os
from typing import List, Tuple, Dict
import time

def compress_image(image: Image.Image, quality: int = 85, max_width: int = None, max_height: int = None) -> Tuple[io.BytesIO, int]:
    """Comprime una imagen y retorna el buffer y el tamaño."""
    output = io.BytesIO()
    
    # Crear una copia para no modificar la original
    img_copy = image.copy()
    
    # Redimensionar si se especifica
    if max_width or max_height:
        img_copy.thumbnail((max_width or img_copy.width, max_height or img_copy.height), Image.Resampling.LANCZOS)
    
    # Convertir a RGB si es necesario
    if img_copy.mode in ('RGBA', 'P'):
        # Para PNG con transparencia, crear fondo blanco
        if img_copy.mode == 'RGBA':
            background = Image.new('RGB', img_copy.size, (255, 255, 255))
            background.paste(img_copy, mask=img_copy.split()[-1])
            img_copy = background
        else:
            img_copy = img_copy.convert('RGB')
    
    # Comprimir la imagen
    img_copy.save(output, format='JPEG', quality=quality, optimize=True)
    output.seek(0)
    
    size = len(output.getvalue())
    return output, size

def extract_images_from_zip(zip_file) -> Dict[str, Tuple[Image.Image, int]]:
    """Extrae imágenes de un archivo ZIP."""
    images = {}
    supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp', '.gif')
    
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            for file_info in zip_ref.filelist:
                if file_info.filename.lower().endswith(supported_formats) and not file_info.filename.startswith('__MACOSX'):
                    try:
                        with zip_ref.open(file_info) as img_file:
                            image_data = img_file.read()
                            image = Image.open(io.BytesIO(image_data))
                            original_size = len(image_data)
                            images[file_info.filename] = (image, original_size)
                    except Exception as e:
                        st.warning(f"No se pudo cargar la imagen {file_info.filename}: {str(e)}")
    except Exception as e:
        st.error(f"Error al leer el archivo ZIP: {str(e)}")
    
    return images

def format_file_size(size_bytes: int) -> str:
    """Convierte bytes a formato legible."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"

def create_zip_download(compressed_images: Dict[str, io.BytesIO]) -> bytes:
    """Crea un archivo ZIP con todas las imágenes comprimidas."""
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zip_file:
        for filename, image_buffer in compressed_images.items():
            # Cambiar extensión a .jpg para las imágenes comprimidas
            base_name = os.path.splitext(filename)[0]
            new_filename = f"{base_name}_compressed.jpg"
            zip_file.writestr(new_filename, image_buffer.getvalue())
    
    zip_buffer.seek(0)
    return zip_buffer.getvalue()

def get_quality_description(quality: int) -> str:
    """Retorna una descripción de la calidad de compresión."""
    if quality >= 95:
        return "Calidad máxima (archivo grande)"
    elif quality >= 85:
        return "Calidad alta (recomendado)"
    elif quality >= 70:
        return "Calidad media (buen balance)"
    elif quality >= 50:
        return "Calidad baja (archivo pequeño)"
    else:
        return "Calidad muy baja (archivo muy pequeño)"

def main():
    st.set_page_config(
        page_title="Compresor de Imágenes",
        page_icon="🖼️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🖼️ Compresor de Imágenes")
    st.markdown("Sube imágenes individuales o un archivo ZIP para comprimirlas y reducir su tamaño.")
    
    # Inicializar session state
    if 'images_data' not in st.session_state:
        st.session_state.images_data = {}
    if 'compressed_images' not in st.session_state:
        st.session_state.compressed_images = {}
    if 'compression_settings' not in st.session_state:
        st.session_state.compression_settings = {}
    
    # Sidebar para configuración
    st.sidebar.header("⚙️ Configuración de Compresión")
    
    # Configuración de calidad con descripción
    quality = st.sidebar.slider(
        "Calidad de Compresión", 
        1, 100, 85, 
        help="Ajusta la calidad de la imagen comprimida"
    )
    st.sidebar.caption(f"📊 {get_quality_description(quality)}")
    
    # Configuración de redimensionamiento
    st.sidebar.subheader("📏 Redimensionamiento (opcional)")
    resize_enabled = st.sidebar.checkbox("Redimensionar imágenes", help="Reduce las dimensiones de las imágenes")
    
    max_width = None
    max_height = None
    
    if resize_enabled:
        col1, col2 = st.sidebar.columns(2)
        with col1:
            max_width = st.number_input("Ancho máx.", min_value=100, max_value=5000, value=1920, step=100)
        with col2:
            max_height = st.number_input("Alto máx.", min_value=100, max_value=5000, value=1080, step=100)
    
    # Información de configuración actual
    st.sidebar.markdown("---")
    st.sidebar.subheader("📋 Configuración Actual")
    st.sidebar.write(f"**Calidad:** {quality}%")
    if resize_enabled:
        st.sidebar.write(f"**Redimensionar:** {max_width}x{max_height}px")
    else:
        st.sidebar.write("**Redimensionar:** Deshabilitado")
    
    # Área de carga de archivos
    st.header("📁 Cargar Archivos")
    
    # Pestañas para diferentes tipos de carga
    tab1, tab2 = st.tabs(["📷 Imágenes Individuales", "📦 Archivo ZIP"])
    
    with tab1:
        uploaded_images = st.file_uploader(
            "Selecciona imágenes",
            type=['jpg', 'jpeg', 'png', 'bmp', 'tiff', 'webp', 'gif'],
            accept_multiple_files=True,
            help="Puedes seleccionar múltiples imágenes a la vez"
        )
    
    with tab2:
        uploaded_zip = st.file_uploader(
            "Selecciona un archivo ZIP",
            type=['zip'],
            help="El ZIP puede contener múltiples imágenes"
        )
    
    # Procesar archivos cargados
    current_images = {}
    
    # Procesar imágenes individuales
    if uploaded_images:
        for uploaded_file in uploaded_images:
            try:
                # Resetear el puntero del archivo
                uploaded_file.seek(0)
                image = Image.open(uploaded_file)
                original_size = len(uploaded_file.getvalue())
                current_images[uploaded_file.name] = (image, original_size)
            except Exception as e:
                st.error(f"Error al cargar {uploaded_file.name}: {str(e)}")
    
    # Procesar archivo ZIP
    if uploaded_zip:
        try:
            zip_images = extract_images_from_zip(uploaded_zip)
            current_images.update(zip_images)
            if zip_images:
                st.success(f"✅ Se extrajeron {len(zip_images)} imágenes del archivo ZIP")
            else:
                st.warning("⚠️ No se encontraron imágenes válidas en el archivo ZIP")
        except Exception as e:
            st.error(f"❌ Error al procesar el archivo ZIP: {str(e)}")
    
    # Actualizar session state solo si hay cambios
    if current_images != st.session_state.images_data:
        st.session_state.images_data = current_images
        # Limpiar imágenes comprimidas si se cargan nuevas imágenes
        st.session_state.compressed_images = {}
    
    if st.session_state.images_data:
        st.header("🖼️ Imágenes Cargadas")
        
        # Botones de acción masiva al principio
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Comprimir Todas", use_container_width=True, type="primary"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                total_images = len(st.session_state.images_data)
                
                for i, (filename, (image, original_size)) in enumerate(st.session_state.images_data.items()):
                    status_text.text(f"Comprimiendo {filename}...")
                    try:
                        compressed_buffer, compressed_size = compress_image(
                            image, quality, max_width if resize_enabled else None, max_height if resize_enabled else None
                        )
                        st.session_state.compressed_images[filename] = compressed_buffer
                        progress_bar.progress((i + 1) / total_images)
                    except Exception as e:
                        st.error(f"Error al comprimir {filename}: {str(e)}")
                
                status_text.text("¡Compresión completada!")
                time.sleep(1)
                status_text.empty()
                st.success(f"✅ Se comprimieron {len(st.session_state.compressed_images)} imágenes!")
                st.rerun()
        
        with col2:
            if st.button("🗑️ Limpiar Comprimidas", use_container_width=True):
                st.session_state.compressed_images = {}
                st.success("✅ Se limpiaron las imágenes comprimidas!")
                st.rerun()
        
        with col3:
            if st.session_state.compressed_images:
                try:
                    zip_data = create_zip_download(st.session_state.compressed_images)
                    st.download_button(
                        label="📦 Descargar ZIP",
                        data=zip_data,
                        file_name="imagenes_comprimidas.zip",
                        mime="application/zip",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"Error al crear ZIP: {str(e)}")
        
        st.markdown("---")
        
        # Mostrar información de las imágenes en una tabla más organizada
        for i, (filename, (image, original_size)) in enumerate(st.session_state.images_data.items()):
            with st.expander(f"📸 {filename} ({format_file_size(original_size)})", expanded=False):
                col1, col2, col3 = st.columns([1, 2, 1])
                
                with col1:
                    # Mostrar miniatura
                    try:
                        thumbnail = image.copy()
                        thumbnail.thumbnail((150, 150))
                        st.image(thumbnail, use_container_width=True)
                    except Exception as e:
                        st.error(f"Error al mostrar miniatura: {str(e)}")
                
                with col2:
                    # Información de la imagen
                    st.write(f"**📏 Dimensiones:** {image.size[0]} × {image.size[1]} píxeles")
                    st.write(f"**📊 Tamaño original:** {format_file_size(original_size)}")
                    st.write(f"**🎨 Formato:** {image.format if image.format else 'Desconocido'}")
                    st.write(f"**🌈 Modo de color:** {image.mode}")
                    
                    # Mostrar información de compresión si existe
                    if filename in st.session_state.compressed_images:
                        compressed_size = len(st.session_state.compressed_images[filename].getvalue())
                        reduction = ((original_size - compressed_size) / original_size) * 100
                        st.success(f"✅ **Comprimida:** {format_file_size(compressed_size)} (-{reduction:.1f}%)")
                
                with col3:
                    # Botón de compresión individual
                    if st.button(f"🔄 Comprimir", key=f"compress_{i}"):
                        with st.spinner("Comprimiendo..."):
                            try:
                                compressed_buffer, compressed_size = compress_image(
                                    image, quality, max_width if resize_enabled else None, max_height if resize_enabled else None
                                )
                                st.session_state.compressed_images[filename] = compressed_buffer
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error al comprimir: {str(e)}")
                    
                    # Botón de descarga individual
                    if filename in st.session_state.compressed_images:
                        compressed_buffer = st.session_state.compressed_images[filename]
                        base_name = os.path.splitext(filename)[0]
                        download_filename = f"{base_name}_compressed.jpg"
                        
                        st.download_button(
                            label="⬇️ Descargar",
                            data=compressed_buffer.getvalue(),
                            file_name=download_filename,
                            mime="image/jpeg",
                            key=f"download_{i}",
                            use_container_width=True
                        )
        
        # Resumen estadístico
        if st.session_state.compressed_images:
            st.markdown("---")
            st.header("📊 Resumen de Compresión")
            
            total_original = sum(original_size for filename, (_, original_size) in st.session_state.images_data.items() 
                            if filename in st.session_state.compressed_images)
            total_compressed = sum(len(buffer.getvalue()) for buffer in st.session_state.compressed_images.values())
            total_reduction = ((total_original - total_compressed) / total_original) * 100 if total_original > 0 else 0
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📷 Imágenes Comprimidas", len(st.session_state.compressed_images))
            
            with col2:
                st.metric("📦 Tamaño Original", format_file_size(total_original))
            
            with col3:
                st.metric("📦 Tamaño Comprimido", format_file_size(total_compressed))
            
            with col4:
                st.metric("💾 Reducción Total", f"{total_reduction:.1f}%", delta=f"-{format_file_size(total_original - total_compressed)}")
        
    else:
        # Página de inicio con información
        st.info("👆 Sube archivos de imagen o un archivo ZIP para comenzar.")
        
        # Información de ayuda
        with st.expander("ℹ️ Información de Uso", expanded=True):
            st.markdown("""
            ### 🎯 **Cómo usar esta aplicación:**
            
            1. **📁 Cargar archivos**: Sube imágenes individuales o un archivo ZIP
            2. **⚙️ Configurar compresión**: Ajusta la calidad y redimensionamiento en la barra lateral
            3. **🔄 Comprimir**: Comprime imágenes individualmente o todas a la vez
            4. **⬇️ Descargar**: Descarga imágenes comprimidas individualmente o en un ZIP
            
            ### 📋 **Formatos soportados:**
            - **Imágenes**: JPG, JPEG, PNG, BMP, TIFF, WEBP, GIF
            - **Archivos comprimidos**: ZIP
            
            ### 💡 **Consejos de uso:**
            - **Calidad 85-95%**: Para fotos de alta calidad
            - **Calidad 70-85%**: Balance entre calidad y tamaño
            - **Calidad 50-70%**: Para imágenes web o previsualizaciones
            - **Redimensionar**: Útil para reducir el tamaño de imágenes muy grandes
            
            ### 🔒 **Privacidad:**
            - Las imágenes se procesan localmente en tu navegador
            - No se almacenan permanentemente en el servidor
            - Tus archivos no se comparten con terceros
            """)

if __name__ == "__main__":
    main()
