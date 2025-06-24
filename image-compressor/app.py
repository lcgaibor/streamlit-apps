import streamlit as st
import zipfile
import io
from PIL import Image
import base64
import os
from typing import List, Tuple, Dict

def compress_image(image: Image.Image, quality: int = 85) -> Tuple[io.BytesIO, int]:
    """Comprime una imagen y retorna el buffer y el tamaño."""
    output = io.BytesIO()
    
    # Convertir a RGB si es necesario
    if image.mode in ('RGBA', 'P'):
        image = image.convert('RGB')
    
    # Comprimir la imagen
    image.save(output, format='JPEG', quality=quality, optimize=True)
    output.seek(0)
    
    size = len(output.getvalue())
    return output, size

def extract_images_from_zip(zip_file) -> Dict[str, Tuple[Image.Image, int]]:
    """Extrae imágenes de un archivo ZIP."""
    images = {}
    supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp')
    
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        for file_info in zip_ref.filelist:
            if file_info.filename.lower().endswith(supported_formats):
                try:
                    with zip_ref.open(file_info) as img_file:
                        image_data = img_file.read()
                        image = Image.open(io.BytesIO(image_data))
                        original_size = len(image_data)
                        images[file_info.filename] = (image, original_size)
                except Exception as e:
                    st.warning(f"No se pudo cargar la imagen {file_info.filename}: {str(e)}")
    
    return images

def format_file_size(size_bytes: int) -> str:
    """Convierte bytes a formato legible."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"

def create_download_link(file_data: bytes, filename: str, link_text: str) -> str:
    """Crea un enlace de descarga para un archivo."""
    b64 = base64.b64encode(file_data).decode()
    return f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">{link_text}</a>'

def create_zip_download(compressed_images: Dict[str, io.BytesIO]) -> bytes:
    """Crea un archivo ZIP con todas las imágenes comprimidas."""
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for filename, image_buffer in compressed_images.items():
            # Cambiar extensión a .jpg para las imágenes comprimidas
            base_name = os.path.splitext(filename)[0]
            new_filename = f"{base_name}_compressed.jpg"
            zip_file.writestr(new_filename, image_buffer.getvalue())
    
    zip_buffer.seek(0)
    return zip_buffer.getvalue()

def main():
    st.set_page_config(
        page_title="Compresor de Imágenes",
        page_icon="🖼️",
        layout="wide"
    )
    
    st.title("🖼️ Compresor de Imágenes")
    st.markdown("Sube imágenes individuales o un archivo ZIP para comprimirlas y reducir su tamaño.")
    
    # Inicializar session state
    if 'images_data' not in st.session_state:
        st.session_state.images_data = {}
    if 'compressed_images' not in st.session_state:
        st.session_state.compressed_images = {}
    
    # Sidebar para configuración
    st.sidebar.header("Configuración de Compresión")
    quality = st.sidebar.slider("Calidad de Compresión", 1, 100, 85, help="Menor valor = mayor compresión")
    
    # Área de carga de archivos
    st.header("📁 Cargar Archivos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Imágenes Individuales")
        uploaded_images = st.file_uploader(
            "Selecciona imágenes",
            type=['jpg', 'jpeg', 'png', 'bmp', 'tiff', 'webp'],
            accept_multiple_files=True,
            key="individual_images"
        )
    
    with col2:
        st.subheader("Archivo ZIP")
        uploaded_zip = st.file_uploader(
            "Selecciona un archivo ZIP",
            type=['zip'],
            key="zip_file"
        )
    
    # Procesar archivos cargados
    current_images = {}
    
    # Procesar imágenes individuales
    if uploaded_images:
        for uploaded_file in uploaded_images:
            try:
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
                st.success(f"Se extrajeron {len(zip_images)} imágenes del archivo ZIP")
        except Exception as e:
            st.error(f"Error al procesar el archivo ZIP: {str(e)}")
    
    # Actualizar session state
    st.session_state.images_data = current_images
    
    if st.session_state.images_data:
        st.header("🖼️ Imágenes Cargadas")
        
        # Mostrar información de las imágenes
        for i, (filename, (image, original_size)) in enumerate(st.session_state.images_data.items()):
            with st.expander(f"📸 {filename} ({format_file_size(original_size)})"):
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    # Mostrar miniatura
                    thumbnail = image.copy()
                    thumbnail.thumbnail((200, 200))
                    st.image(thumbnail, caption=f"Dimensiones: {image.size[0]}x{image.size[1]}")
                
                with col2:
                    st.write(f"**Tamaño original:** {format_file_size(original_size)}")
                    st.write(f"**Formato:** {image.format if image.format else 'Desconocido'}")
                    st.write(f"**Modo:** {image.mode}")
                
                with col3:
                    if st.button(f"Comprimir", key=f"compress_{i}"):
                        with st.spinner("Comprimiendo..."):
                            compressed_buffer, compressed_size = compress_image(image, quality)
                            st.session_state.compressed_images[filename] = compressed_buffer
                            
                            # Mostrar resultados
                            reduction = ((original_size - compressed_size) / original_size) * 100
                            st.success(f"✅ Comprimida!")
                            st.write(f"**Nuevo tamaño:** {format_file_size(compressed_size)}")
                            st.write(f"**Reducción:** {reduction:.1f}%")
                
                # Mostrar enlace de descarga si ya está comprimida
                if filename in st.session_state.compressed_images:
                    compressed_buffer = st.session_state.compressed_images[filename]
                    compressed_size = len(compressed_buffer.getvalue())
                    
                    st.write("---")
                    col_info, col_download = st.columns([2, 1])
                    
                    with col_info:
                        reduction = ((original_size - compressed_size) / original_size) * 100
                        st.success(f"✅ **Comprimida:** {format_file_size(compressed_size)} (-{reduction:.1f}%)")
                    
                    with col_download:
                        base_name = os.path.splitext(filename)[0]
                        download_filename = f"{base_name}_compressed.jpg"
                        
                        st.download_button(
                            label="⬇️ Descargar",
                            data=compressed_buffer.getvalue(),
                            file_name=download_filename,
                            mime="image/jpeg",
                            key=f"download_{i}"
                        )
        
        # Botones de acción masiva
        st.header("⚡ Acciones Masivas")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Comprimir Todas", use_container_width=True):
                progress_bar = st.progress(0)
                total_images = len(st.session_state.images_data)
                
                for i, (filename, (image, original_size)) in enumerate(st.session_state.images_data.items()):
                    compressed_buffer, compressed_size = compress_image(image, quality)
                    st.session_state.compressed_images[filename] = compressed_buffer
                    progress_bar.progress((i + 1) / total_images)
                
                st.success(f"✅ Se comprimieron {total_images} imágenes!")
                st.rerun()
        
        with col2:
            if st.button("🗑️ Limpiar Comprimidas", use_container_width=True):
                st.session_state.compressed_images = {}
                st.success("✅ Se limpiaron las imágenes comprimidas!")
                st.rerun()
        
        with col3:
            if st.session_state.compressed_images:
                zip_data = create_zip_download(st.session_state.compressed_images)
                st.download_button(
                    label="📦 Descargar ZIP",
                    data=zip_data,
                    file_name="imagenes_comprimidas.zip",
                    mime="application/zip",
                    use_container_width=True
                )
        
        # Resumen estadístico
        if st.session_state.compressed_images:
            st.header("📊 Resumen")
            
            total_original = sum(original_size for filename, (_, original_size) in st.session_state.images_data.items() 
                            if filename in st.session_state.compressed_images)
            total_compressed = sum(len(buffer.getvalue()) for buffer in st.session_state.compressed_images.values())
            total_reduction = ((total_original - total_compressed) / total_original) * 100 if total_original > 0 else 0
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Imágenes Comprimidas", len(st.session_state.compressed_images))
            
            with col2:
                st.metric("Tamaño Original", format_file_size(total_original))
            
            with col3:
                st.metric("Tamaño Comprimido", format_file_size(total_compressed))
            
            with col4:
                st.metric("Reducción Total", f"{total_reduction:.1f}%")
        
    else:
        st.info("👆 Sube archivos de imagen o un archivo ZIP para comenzar.")
        
        # Información de ayuda
        with st.expander("ℹ️ Información de Uso"):
            st.markdown("""
            **Formatos soportados:**
            - Imágenes: JPG, JPEG, PNG, BMP, TIFF, WEBP
            - Archivos comprimidos: ZIP
            
            **Cómo usar:**
            1. Sube imágenes individuales o un archivo ZIP
            2. Ajusta la calidad de compresión en la barra lateral
            3. Comprime imágenes individualmente o todas a la vez
            4. Descarga las imágenes comprimidas o un ZIP con todas
            
            **Nota:** Las imágenes se procesan en memoria y no se guardan permanentemente.
            """)

if __name__ == "__main__":
    main()