# Redimensionador de Imágenes

Una aplicación web desarrollada con Streamlit para redimensionar imágenes de forma masiva.

## Funcionalidades

- 📁 Carga de imágenes individuales o archivos ZIP
- 🔄 Redimensionado automático a máximo 480x480px
- 📊 Información detallada de cada imagen procesada
- 💾 Descarga individual o masiva en ZIP

## Cómo usar

1. Visita la aplicación en Streamlit Cloud
2. Selecciona el tipo de archivo (imágenes individuales o ZIP)
3. Sube tus archivos
4. Haz clic en "Procesar todas las imágenes"
5. Descarga las imágenes redimensionadas

## Formatos soportados

- JPG, JPEG, PNG, BMP, GIF, TIFF, WebP

## Ejecutar localmente

```bash
pip install streamlit pillow
streamlit run app.py
```

## Características técnicas

- Mantiene la proporción original de las imágenes
- Procesamiento en memoria sin almacenamiento permanente
- Interfaz intuitiva con miniaturas y estadísticas
- Compatible con archivos ZIP para procesamiento masivo