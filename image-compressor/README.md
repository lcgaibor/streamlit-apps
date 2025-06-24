# Compresor de Imágenes

Una aplicación web desarrollada con Streamlit para comprimir imágenes reduciendo su tamaño y peso manteniendo la calidad visual.

## Funcionalidades

- 📁 Carga de imágenes individuales o archivos ZIP
- 🗜️ Compresión ajustable de calidad (1-100%)
- 📊 Comparación de tamaños antes/después con porcentaje de reducción
- 💾 Descarga individual o masiva en ZIP
- 🖼️ Vista previa con miniaturas de las imágenes

## Cómo usar

1. Visita la aplicación en Streamlit Cloud
2. Sube imágenes individuales o un archivo ZIP
3. Ajusta la calidad de compresión en la barra lateral (85% por defecto)
4. Comprime imágenes individualmente o todas a la vez
5. Descarga las imágenes comprimidas

## Formatos soportados

- **Entrada:** JPG, JPEG, PNG, BMP, TIFF, WebP
- **Salida:** JPG (formato optimizado para compresión)

## Ejecutar localmente

```bash
pip install streamlit pillow
streamlit run app.py
```

## Características técnicas

- Conversión automática a RGB para optimizar compresión
- Procesamiento en memoria sin almacenamiento permanente
- Estadísticas detalladas de reducción de tamaño
- Interfaz responsive con acciones masivas
- Compatible con archivos ZIP para procesamiento masivo