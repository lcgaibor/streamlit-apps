⚛️ Generador de Símbolos de Elementos Químicos
Aplicación web desarrollada con Streamlit que genera imágenes minimalistas de símbolos de elementos químicos con diseño profesional y limpio.
Características

Selección completa: Todos los 118 elementos de la tabla periódica disponibles
Dos modos de selección: Por elemento químico o por número atómico
Opciones flexibles: Solo símbolo o símbolo + número atómico
Descarga directa: Archivo PNG listo para usar como "logo_elemento.png"
Vista previa en tiempo real: Ve el resultado antes de descargar

 Modos de uso
Modo 1: Por elemento químico

Selecciona un elemento del menú desplegable
El símbolo y número atómico se configuran automáticamente
Elige si mostrar solo el símbolo o incluir el número atómico

Modo 2: Por número atómico

Ingresa un número atómico (1-118)
El elemento y símbolo se detectan automáticamente
Elige si mostrar solo el símbolo o incluir el número atómico

Instalación y uso local
Prerrequisitos

Python 3.7+
pip

Instalación
bash# Clonar el repositorio
git clone https://github.com/lcgaibor/streamlit-apps.git
cd generador-simbolos-quimicos

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
streamlit run app.py
Dependencias
streamlit>=1.28.0
Pillow>=9.0.0