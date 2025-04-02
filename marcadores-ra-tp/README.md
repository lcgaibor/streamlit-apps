# Generador de Marcadores RA para la Tabla Periódica

Esta aplicación genera marcadores de Realidad Aumentada (RA) únicos para cada elemento de la tabla periódica, utilizando el número atómico como semilla para crear patrones visuales distintivos y reconocibles.

## Características

- Genera marcadores RA para los 118 elementos de la tabla periódica
- Cada marcador tiene un patrón único basado matemáticamente en el número atómico
- Interfaz fácil de usar con filtrado por categorías de elementos
- Opción para mostrar u ocultar el símbolo del elemento
- Descarga de marcadores en formato PNG
- Uso de Mersenne Twister

## Cómo funciona

1. Selecciona un elemento por categoría o introduce directamente su número atómico
2. Configura las opciones de visualización (mostrar/ocultar símbolo, número atómico)
3. Haz clic en "Generar Marcador"
4. Visualiza el marcador RA único para ese elemento
5. Descarga la imagen para usarla en aplicaciones de Realidad Aumentada

## Instalación local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
streamlit run app.py
```

## Uso en aplicaciones de RA

Los marcadores generados pueden ser utilizados como targets en frameworks de Realidad Aumentada como:

- ARToolKit
- Vuforia
- AR.js
- ARCore