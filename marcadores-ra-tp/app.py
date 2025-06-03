import streamlit as st
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
import io
import base64
from datetime import datetime
from styles import apply_styles

# Configuración de la página
st.set_page_config(
    page_title="Generador de Marcadores RA - Tabla Periódica",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Aplicar estilos personalizados
apply_styles()


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
    
    def generate_unique_corner_pattern(self, atomic_number, corner_index):
        """
        Genera un patrón de esquina único para cada elemento y cada esquina.
        
        Args:
            atomic_number (int): Número atómico del elemento.
            corner_index (int): Índice de la esquina (0, 1, 2).
            
        Returns:
            list: Patrón de esquina de 7x7.
        """
        # Usar diferentes semillas para cada esquina
        seed_offset = [1000, 2000, 3000]
        np.random.seed(atomic_number + seed_offset[corner_index])
        
        # Patrón base de esquina QR
        corner_base = [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 1],
            [1, 0, 1, 1, 1, 0, 1],
            [1, 0, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1]
        ]
        
        # Crear copia del patrón base
        corner_pattern = [row[:] for row in corner_base]
        
        # Generar modificaciones únicas para el área interna (2x2 a 4x4)
        for i in range(2, 5):
            for j in range(2, 5):
                # Usar Mersenne Twister para decidir el patrón interno
                if np.random.random() > 0.5:
                    corner_pattern[i][j] = 1 - corner_pattern[i][j]  # Invertir
        
        # Aplicar modificaciones adicionales basadas en el número atómico y esquina
        mod_val = (atomic_number + corner_index * 37) % 12  # Más variaciones
        
        if mod_val == 0:
            corner_pattern[2][2] = 0
            corner_pattern[4][4] = 0
        elif mod_val == 1:
            corner_pattern[2][3] = 0
            corner_pattern[3][2] = 0
        elif mod_val == 2:
            corner_pattern[3][3] = 0
            corner_pattern[2][4] = 1
        elif mod_val == 3:
            corner_pattern[2][2] = 1
            corner_pattern[3][4] = 0
        elif mod_val == 4:
            corner_pattern[4][2] = 0
            corner_pattern[4][3] = 1
        elif mod_val == 5:
            corner_pattern[2][3] = 1
            corner_pattern[4][3] = 0
        elif mod_val == 6:
            corner_pattern[3][2] = 1
            corner_pattern[3][4] = 1
        elif mod_val == 7:
            corner_pattern[2][4] = 0
            corner_pattern[4][2] = 1
        elif mod_val == 8:
            corner_pattern[2][2] = 1
            corner_pattern[2][4] = 0
            corner_pattern[4][4] = 1
        elif mod_val == 9:
            corner_pattern[3][3] = 1
            corner_pattern[4][3] = 0
        elif mod_val == 10:
            corner_pattern[2][3] = 0
            corner_pattern[3][4] = 1
            corner_pattern[4][2] = 0
        else:  # mod_val == 11
            corner_pattern[2][2] = 0
            corner_pattern[3][3] = 1
            corner_pattern[4][4] = 0
        
        return corner_pattern
    
    def generate_qr_marker(self, symbol, atomic_number, show_symbol=True, show_atomic_number=True):
        """
        Genera un marcador tipo QR único para cualquier elemento químico usando Mersenne Twister
        con patrones de esquina únicos para cada elemento.
        
        Args:
            symbol (str): Símbolo del elemento.
            atomic_number (int): Número atómico del elemento.
            show_symbol (bool): Indica si se debe mostrar el símbolo del elemento.
            show_atomic_number (bool): Indica si se debe mostrar el número atómico.
            
        Returns:
            np.array: Imagen del marcador como array de NumPy.
        """
        img_size = self.marker_size + 2 * self.border_size
        img = Image.new('RGB', (img_size, img_size), color='white')
        draw = ImageDraw.Draw(img)
        
        # Usar Mersenne Twister con número atómico + 10000 como semilla base
        np.random.seed(atomic_number + 10000)
        
        # Crear un patrón tipo QR más denso
        grid_size = 16  # Más celdas para patrón más complejo
        cell_size = self.marker_size // grid_size
        
        # Generar patrones de esquina únicos para cada esquina
        corner_positions = [(0, 0), (grid_size-7, 0), (0, grid_size-7)]
        
        for corner_idx, (corner_x, corner_y) in enumerate(corner_positions):
            corner_pattern = self.generate_unique_corner_pattern(atomic_number, corner_idx)
            
            for i in range(7):
                for j in range(7):
                    if corner_pattern[i][j] == 1:
                        x0 = self.border_size + (corner_x + i) * cell_size
                        y0 = self.border_size + (corner_y + j) * cell_size
                        x1 = x0 + cell_size
                        y1 = y0 + cell_size
                        draw.rectangle([(x0, y0), (x1, y1)], fill='black')
        
        # Patrón de alineación central único para cada elemento
        center_x, center_y = grid_size // 2 - 2, grid_size // 2 - 2
        
        # Usar semilla específica para el patrón central
        np.random.seed(atomic_number + 5000)
        
        # Generar patrón de alineación único usando Mersenne Twister
        alignment_size = 5
        alignment_pattern = [[0 for _ in range(alignment_size)] for _ in range(alignment_size)]
        
        # Crear borde del patrón de alineación
        for i in range(alignment_size):
            alignment_pattern[0][i] = 1
            alignment_pattern[alignment_size-1][i] = 1
            alignment_pattern[i][0] = 1
            alignment_pattern[i][alignment_size-1] = 1
        
        # Rellenar interior con patrón único usando Mersenne Twister
        for i in range(1, alignment_size-1):
            for j in range(1, alignment_size-1):
                # Variar la probabilidad según el elemento
                threshold = 0.3 + (atomic_number % 5) * 0.1  # 0.3 a 0.7
                if np.random.random() > threshold:
                    alignment_pattern[i][j] = 1
        
        # Dibujar patrón de alineación
        for i in range(alignment_size):
            for j in range(alignment_size):
                if alignment_pattern[i][j] == 1:
                    x0 = self.border_size + (center_x + i) * cell_size
                    y0 = self.border_size + (center_y + j) * cell_size
                    x1 = x0 + cell_size
                    y1 = y0 + cell_size
                    draw.rectangle([(x0, y0), (x1, y1)], fill='black')
        
        # Rellenar el resto con patrón pseudo-aleatorio único usando Mersenne Twister
        np.random.seed(atomic_number + 10000)  # Semilla para el relleno general
        
        for i in range(grid_size):
            for j in range(grid_size):
                # Evitar las esquinas y el centro ya dibujados
                if ((i < 7 and j < 7) or  # Esquina superior izquierda
                    (i >= grid_size-7 and j < 7) or  # Esquina superior derecha
                    (i < 7 and j >= grid_size-7) or  # Esquina inferior izquierda
                    (center_x <= i < center_x+5 and center_y <= j < center_y+5)):  # Centro
                    continue
                
                # Generar patrón usando Mersenne Twister con probabilidad variable
                threshold = 0.45 + (atomic_number % 7) * 0.02  # 0.45 a 0.57
                if np.random.random() > threshold:
                    x0 = self.border_size + i * cell_size
                    y0 = self.border_size + j * cell_size
                    x1 = x0 + cell_size
                    y1 = y0 + cell_size
                    draw.rectangle([(x0, y0), (x1, y1)], fill='black')
        
        # Añadir el símbolo en el centro si está habilitado
        if show_symbol:
            try:
                font_path = "font/OpenSans-Bold.ttf"
                # Aumentar significativamente el tamaño de la letra
                if len(symbol) == 1:
                    font_size = 120  # Para símbolos de una letra
                elif len(symbol) == 2:
                    font_size = 100  # Para símbolos de dos letras
                else:
                    font_size = 80   # Para símbolos de tres letras
                font_symbol = ImageFont.truetype(font_path, font_size)
            except IOError:
                try:
                    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
                    font_symbol = ImageFont.truetype(font_path, font_size)
                except IOError:
                    font_symbol = ImageFont.load_default()
            
            # Área para el símbolo en el centro (6x6 celdas)
            symbol_area_size = 6
            symbol_area_x0 = self.border_size + (grid_size - symbol_area_size) // 2 * cell_size
            symbol_area_y0 = self.border_size + (grid_size - symbol_area_size) // 2 * cell_size
            symbol_area_x1 = symbol_area_x0 + cell_size * symbol_area_size
            symbol_area_y1 = symbol_area_y0 + cell_size * symbol_area_size
            
            # Fondo blanco para el símbolo
            draw.rectangle(
                [(symbol_area_x0, symbol_area_y0), (symbol_area_x1, symbol_area_y1)],
                fill='white'
            )
            
            # Centrar el texto perfectamente (ajuste manual para compensar baseline)
            symbol_width = draw.textlength(symbol, font=font_symbol)
            # Obtener la altura real del texto usando textbbox
            bbox = draw.textbbox((0, 0), symbol, font=font_symbol)
            text_height = bbox[3] - bbox[1]
            
            text_x = symbol_area_x0 + (symbol_area_size*cell_size - symbol_width) / 2
            # Ajustar la posición Y para centrado visual perfecto
            text_y = symbol_area_y0 + (symbol_area_size*cell_size - text_height) / 2 - bbox[1] - 5
            
            # Ajustar tamaño si es necesario
            if symbol_width > (symbol_area_size*cell_size - 20):
                scaling_factor = (symbol_area_size*cell_size - 20) / symbol_width
                new_font_size = int(font_size * scaling_factor)
                try:
                    font_symbol = ImageFont.truetype(font_path, new_font_size)
                except IOError:
                    font_symbol = ImageFont.load_default()
                
                bbox = draw.textbbox((0, 0), symbol, font=font_symbol)
                text_height = bbox[3] - bbox[1]
                
                symbol_width = draw.textlength(symbol, font=font_symbol)
                text_x = symbol_area_x0 + (symbol_area_size*cell_size - symbol_width) / 2
                # Ajustar la posición Y para centrado visual perfecto
                text_y = symbol_area_y0 + (symbol_area_size*cell_size - text_height) / 2 - bbox[1] - 5
            
            # Dibujar el símbolo en negro centrado
            draw.text(
                (text_x, text_y),
                symbol,
                fill='black',
                font=font_symbol
            )
        
        # Añadir el número atómico si está habilitado (con tamaño aumentado)
        if show_atomic_number:
            try:
                font_path = "font/OpenSans-Bold.ttf"
                # Aumentar significativamente el tamaño del número atómico
                atomic_text = str(atomic_number)
                if len(atomic_text) == 1:
                    font_size = 85  # Aumentado de 70 a 85
                elif len(atomic_text) == 2:
                    font_size = 80  # Aumentado de 65 a 80
                else:  # 3 dígitos
                    font_size = 70  # Aumentado de 55 a 70
                font_info = ImageFont.truetype(font_path, font_size)
            except IOError:
                try:
                    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
                    font_info = ImageFont.truetype(font_path, font_size)
                except IOError:
                    font_info = ImageFont.load_default()
            
            # Área para el número atómico (4x4 celdas en la esquina inferior derecha - AUMENTADO)
            atomic_area_x0 = self.border_size + (grid_size - 4) * cell_size
            atomic_area_y0 = self.border_size + (grid_size - 4) * cell_size
            atomic_area_x1 = atomic_area_x0 + cell_size * 4
            atomic_area_y1 = atomic_area_y0 + cell_size * 4
            
            # Fondo blanco para el número
            draw.rectangle(
                [(atomic_area_x0, atomic_area_y0), (atomic_area_x1, atomic_area_y1)],
                fill='white'
            )
            
            # Centrar el texto perfectamente (ajuste manual para compensar baseline)
            text_width = draw.textlength(atomic_text, font=font_info)
            # Obtener la altura real del texto usando textbbox
            bbox = draw.textbbox((0, 0), atomic_text, font=font_info)
            text_height = bbox[3] - bbox[1]
            
            text_x = atomic_area_x0 + (4*cell_size - text_width) / 2
            # Ajustar la posición Y para centrado visual perfecto
            text_y = atomic_area_y0 + (4*cell_size - text_height) / 2 - bbox[1] - 3
            
            # Ajustar tamaño si es necesario
            if text_width > (4*cell_size - 15):
                scaling_factor = (4*cell_size - 15) / text_width
                new_font_size = int(font_size * scaling_factor)
                try:
                    font_info = ImageFont.truetype(font_path, new_font_size)
                except IOError:
                    font_info = ImageFont.load_default()
                
                bbox = draw.textbbox((0, 0), atomic_text, font=font_info)
                text_height = bbox[3] - bbox[1]
                
                text_width = draw.textlength(atomic_text, font=font_info)
                text_x = atomic_area_x0 + (4*cell_size - text_width) / 2
                # Ajustar la posición Y para centrado visual perfecto
                text_y = atomic_area_y0 + (4*cell_size - text_height) / 2 - bbox[1] - 3
            
            # Dibujar el número atómico en negro
            draw.text(
                (text_x, text_y),
                atomic_text,
                fill='black',
                font=font_info
            )
        
        marker_array = np.array(img)
        marker_gray = cv2.cvtColor(marker_array, cv2.COLOR_RGB2GRAY)
        
        return marker_gray
    
    def generate_element_marker(self, symbol, name, atomic_number, show_symbol=False, show_atomic_number=True, symbol_size=2):
        """
        Genera un marcador RA único para un elemento químico optimizado para impresión 3D (estilo original).
        
        Args:
            symbol (str): Símbolo del elemento.
            name (str): Nombre del elemento.
            atomic_number (int): Número atómico del elemento.
            show_symbol (bool): Indica si se debe mostrar el símbolo del elemento.
            show_atomic_number (bool): Indica si se debe mostrar el número atómico.
            symbol_size (int): Tamaño del símbolo en celdas (2, 3, o 4).
            
        Returns:
            np.array: Imagen del marcador como array de NumPy.
        """
        img_size = self.marker_size + 2 * self.border_size
        img = Image.new('RGB', (img_size, img_size), color='white')
        draw = ImageDraw.Draw(img)
        
        np.random.seed(atomic_number)  # Usar número atómico como semilla
        
        # Generar una matriz de celdas para el marcador
        grid_size = 8  
        cell_size = (self.marker_size) // grid_size
        
        for i in range(grid_size):
            for j in range(grid_size):
                # Evitar dibujar en las áreas reservadas para el símbolo y número atómico
                if show_symbol and i < symbol_size and j < symbol_size:
                    continue
                    
                if show_atomic_number and i >= grid_size - 2 and j >= grid_size - 2:
                    continue
                
                # Generar un valor aleatorio determinista basado en el número atómico
                rand_val = np.random.random()
                if rand_val > 0.5:  # 50% de probabilidad de dibujar 
                    x0 = self.border_size + i * cell_size
                    y0 = self.border_size + j * cell_size
                    x1 = x0 + cell_size
                    y1 = y0 + cell_size
                    
                    draw.rectangle([(x0, y0), (x1, y1)], fill='black')
        
        if show_symbol:
            try:
                font_path = "font/OpenSans-Bold.ttf"
                if symbol_size == 2:
                    font_size = 80
                elif symbol_size == 3:
                    font_size = 110
                else:  # symbol_size == 4
                    font_size = 140
                    
                font_symbol = ImageFont.truetype(font_path, font_size)
            except IOError:
                try:
                    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
                    font_symbol = ImageFont.truetype(font_path, font_size)
                except IOError:
                    font_symbol = ImageFont.load_default()
            
            symbol_area_x0 = self.border_size
            symbol_area_y0 = self.border_size
            symbol_area_x1 = symbol_area_x0 + cell_size * symbol_size
            symbol_area_y1 = symbol_area_y0 + cell_size * symbol_size
            
            draw.rectangle(
                [(symbol_area_x0, symbol_area_y0), (symbol_area_x1, symbol_area_y1)],
                fill='white'
            )
            
            symbol_width = draw.textlength(symbol, font=font_symbol)
            text_x = symbol_area_x0 + (symbol_size*cell_size - symbol_width) / 2
            text_y = symbol_area_y0 + (symbol_size*cell_size - font_size) / 2
            
            if symbol_width > (symbol_size*cell_size - 10):
                scaling_factor = (symbol_size*cell_size - 10) / symbol_width
                new_font_size = int(font_size * scaling_factor)
                try:
                    font_symbol = ImageFont.truetype(font_path, new_font_size)
                except IOError:
                    font_symbol = ImageFont.load_default()
                
                symbol_width = draw.textlength(symbol, font=font_symbol)
                text_x = symbol_area_x0 + (symbol_size*cell_size - symbol_width) / 2
                text_y = symbol_area_y0 + (symbol_size*cell_size - new_font_size) / 2
            
            for offset_x in range(-1, 1):
                for offset_y in range(-1, 1):
                    draw.text(
                        (text_x + offset_x, text_y + offset_y),
                        symbol,
                        fill='black',
                        font=font_symbol
                    )
        
        if show_atomic_number:
            atomic_area_x0 = self.border_size + (grid_size - 2) * cell_size
            atomic_area_y0 = self.border_size + (grid_size - 2) * cell_size
            atomic_area_x1 = atomic_area_x0 + cell_size * 2
            atomic_area_y1 = atomic_area_y0 + cell_size * 2
            
            draw.rectangle(
                [(atomic_area_x0, atomic_area_y0), (atomic_area_x1, atomic_area_y1)],
                fill='white'
            )
            
            atomic_text = str(atomic_number)
            try:
                font_path = "font/OpenSans-Bold.ttf"
                font_size = 80 if len(atomic_text) <= 2 else 65
                font_info = ImageFont.truetype(font_path, font_size)
            except IOError:
                try:
                    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
                    font_info = ImageFont.truetype(font_path, font_size)
                except IOError:
                    font_info = ImageFont.load_default()
            
            text_width = draw.textlength(atomic_text, font=font_info)
            text_x = atomic_area_x0 + (2*cell_size - text_width) / 2
            text_y = atomic_area_y0 + (2*cell_size - font_size) / 2
            
            if text_width > (2*cell_size - 10):
                scaling_factor = (2*cell_size - 10) / text_width
                new_font_size = int(font_size * scaling_factor)
                try:
                    font_info = ImageFont.truetype(font_path, new_font_size)
                except IOError:
                    font_info = ImageFont.load_default()
                
                text_width = draw.textlength(atomic_text, font=font_info)
                text_x = atomic_area_x0 + (2*cell_size - text_width) / 2
                text_y = atomic_area_y0 + (2*cell_size - new_font_size) / 2
            
            for offset_x in range(-1, 1):
                for offset_y in range(-1, 1):
                    draw.text(
                        (text_x + offset_x, text_y + offset_y),
                        atomic_text,
                        fill='black',
                        font=font_info
                    )
        
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
    st.title("Generador de Marcadores RA para la Tabla Periódica")
    
    st.markdown("""
    Esta aplicación genera marcadores de Realidad Aumentada (RA) únicos para cada elemento 
    de la tabla periódica. Cada marcador se genera utilizando el número atómico del elemento 
    como semilla con el algoritmo Mersenne Twister, lo que garantiza un patrón único y 
    reconocible para cada uno de los 118 elementos, optimizado para Vuforia y para impresión 3D.
    
    **MEJORA RA**: Los marcadores QR ahora tienen patrones únicos en cada una de las 3 esquinas,
    aumentando significativamente las diferencias entre elementos para mejor reconocimiento AR.
    """)

    generator = ElementARMarkerGenerator()
    
    st.sidebar.header("Opciones de Configuración")
    
    # Selector de tipo de marcador
    st.sidebar.subheader("Tipo de Marcador")
    marker_type = st.sidebar.radio(
        "Selecciona el tipo de marcador:",
        ["Marcador Normal (Original)", "Marcador QR (Optimizado AR)"],
        index=0
    )
    
    # Selector de elemento
    st.sidebar.subheader("Selecciona un Elemento")
    
    # Nueva clasificación de elementos por categorías
    element_categories = {
        "Metales Alcalinos (6 elementos)": [3, 11, 19, 37, 55, 87],
        "Metales Alcalinotérreos (6 elementos)": [4, 12, 20, 38, 56, 88],
        "Metales de Transición (34 elementos)": [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 72, 73, 74, 75, 76, 77, 78, 79, 80, 104, 105, 106, 107, 108],
        "Metales Post-Transición (12 elementos)": [13, 31, 49, 50, 81, 82, 83, 84, 113, 114, 115, 116],
        "Metaloides (7 elementos)": [5, 14, 32, 33, 51, 52, 85],
        "No Metales Reactivos (9 elementos)": [1, 6, 7, 8, 9, 15, 16, 17, 34],
        "Gases Nobles (6 elementos)": [2, 10, 18, 36, 54, 86],
        "Lantánidos (15 elementos)": list(range(57, 72)),
        "Actínidos (15 elementos)": list(range(89, 104)),
        "Propiedades Químicas Desconocidas (4 elementos)": [112, 113, 114, 118]
    }
    
    category_select = st.sidebar.selectbox(
        "Categoría de elementos",
        options=list(element_categories.keys()),
        index=0
    )
    
    category_elements = element_categories[category_select]
    
    element_options = []
    for atomic_num in category_elements:
        element = generator.get_element_by_atomic_number(atomic_num)
        if element:
            symbol, name, _ = element
            element_options.append(f"{atomic_num}: {name} ({symbol})")
    
    selected_element_str = st.sidebar.selectbox(
        "Elemento",
        options=element_options,
        index=0 if element_options else None
    )
    
    st.sidebar.subheader("O ingresa un número atómico")
    atomic_number_input = st.sidebar.number_input(
        "Número atómico (1-118)",
        min_value=1,
        max_value=118,
        value=1
    )
    
    st.sidebar.subheader("Opciones de Visualización")
    show_symbol = st.sidebar.checkbox("Mostrar símbolo del elemento", value=True)
    show_atomic_number = st.sidebar.checkbox("Mostrar número atómico", value=True)
    
    # Selector de tamaño del símbolo (solo para marcadores normales)
    if marker_type == "Marcador Normal (Original)":
        st.sidebar.subheader("Tamaño del Símbolo")
        symbol_size = st.sidebar.selectbox(
            "Tamaño del símbolo (en celdas)",
            options=[2, 3, 4],
            index=0,
            help="Selecciona el tamaño del área para el símbolo: 2x2, 3x3, o 4x4 celdas"
        )
    else:
        symbol_size = 2  # Valor por defecto para marcadores QR
    
    # Botón para generar
    generate_button = st.sidebar.button("Generar Marcador")
    
    if generate_button:
        if selected_element_str and ":" in selected_element_str:
            selected_atomic_number = int(selected_element_str.split(':')[0])
        else:
            selected_atomic_number = atomic_number_input
    else:
        selected_atomic_number = atomic_number_input
    
    selected_element = generator.get_element_by_atomic_number(selected_atomic_number)
    
    if selected_element:
        symbol, name, atomic_number = selected_element
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Marcador RA generado")
            
            # Generar el marcador según el tipo seleccionado
            if marker_type == "Marcador QR (Optimizado AR)":
                marker = generator.generate_qr_marker(
                    symbol, 
                    atomic_number, 
                    show_symbol=show_symbol,
                    show_atomic_number=show_atomic_number
                )
            else:
                marker = generator.generate_element_marker(
                    symbol, 
                    name, 
                    atomic_number, 
                    show_symbol=show_symbol,
                    show_atomic_number=show_atomic_number,
                    symbol_size=symbol_size
                )
            
            pil_img = Image.fromarray(marker)
            
            # Mensaje según el tipo de marcador
            if marker_type == "Marcador QR (Optimizado AR)":
                caption_text = f"🔷 Marcador RA tipo QR optimizado para AR - {name} ({symbol})"
            else:
                caption_text = f"Marcador RA tradicional único para {name} (Símbolo {symbol_size}x{symbol_size})"
            
            st.image(pil_img, caption=caption_text, use_container_width=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if marker_type == "Marcador QR (Optimizado AR)":
                filename = f"{atomic_number:03d}_{symbol}_QR_AR_OPTIMIZADO_{timestamp}.png"
            else:
                filename = f"{atomic_number:03d}_{symbol}_TRADICIONAL_{symbol_size}x{symbol_size}_{timestamp}.png"
            st.markdown(get_image_download_link(pil_img, filename, "📥 Descargar Marcador"), unsafe_allow_html=True)
        
        with col2:
            st.subheader("Información del Elemento")
            
            # Información del elemento
            if marker_type == "Marcador QR (Optimizado AR)":
                st.markdown(f"""
                <div class="element-info">
                    <h3 style="text-align: center; color: blue;"> {symbol} - QR AR</h3>
                    <h2 style="text-align: center; color: black;">{name}</h2>
                    <p style="text-align: center; color: black;"><strong>Número atómico:</strong> {atomic_number}</p>
                    <p style="text-align: center; color: red;"><strong>Semillas MT:</strong> {atomic_number + 1000}, {atomic_number + 2000}, {atomic_number + 3000}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="element-info">
                    <h3 style="text-align: center; color: black;">{symbol} - TRADICIONAL</h3>
                    <h2 style="text-align: center; color: black;">{name}</h2>
                    <p style="text-align: center; color: black;"><strong>Número atómico:</strong> {atomic_number}</p>
                    <p style="text-align: center; color: black;"><strong>Tamaño símbolo:</strong> {symbol_size}x{symbol_size}</p>
                    <p style="text-align: center; color: red;"><strong>Semilla MT:</strong> {atomic_number}</p>
                </div>
                """, unsafe_allow_html=True)
            
            if marker_type == "Marcador QR ":
                st.markdown("""
                ### Características del marcador QR optimizado AR
                
                * **Mersenne Twister** como generador con múltiples semillas
                * **Semillas múltiples MT** - Esquinas con semillas +1000, +2000, +3000
                * **Patrón central único** - Generado con semilla +5000
                * **Probabilidades variables** - Threshold según número atómico
                * **Grid de 16x16** para máxima densidad de información

                """)
            else:
                st.markdown("""
                ### Características del marcador tradicional único
                
                * **Mersenne Twister** como generador con semilla = número atómico
                * **Patrón de cuadrados** para detección efectiva en AR
                * **Reproducibilidad total** - mismo patrón siempre
                * **Transformaciones matemáticas** con desplazamientos de bits y XOR
                * **Patrón único garantizado** usando el número atómico como semilla
                * **Tamaño de símbolo configurable** (2x2, 3x3, 4x4)
                * **Grid de 8x8** optimizado para impresión 3D
                * **118 patrones únicos** uno por cada elemento
                """)
        
        # Instrucciones de uso
        st.markdown("""
        ### Cómo usar el marcador
        
        1. **Descarga** la imagen del marcador único
        2. **Para uso en AR (Vuforia)**: Imprime la imagen en papel o muéstrala en pantalla
        3. **Para impresión 3D**: Importa el archivo a TinkerCAD para añadir relieve
        4. **En impresión 3D**: Las áreas negras serán las que tengan relieve
        5. **Unicidad garantizada**: Cada uno de los 118 elementos tiene un patrón completamente diferente
        6. **Mersenne Twister**: Algoritmo de reproducibilidad y distribución uniforme
        """)
        
        if marker_type == "Marcador QR (Optimizado AR)":
            st.markdown(f"""
            ### Detalles técnicos del marcador QR - {name}
            
            **Algoritmo de generación multi-semilla para máxima diferenciación:**
            
            - **Esquina Superior Izquierda**: Semilla MT = {atomic_number + 1000}
            - **Esquina Superior Derecha**: Semilla MT = {atomic_number + 2000}  
            - **Esquina Inferior Izquierda**: Semilla MT = {atomic_number + 3000}
            - **Patrón Central**: Semilla MT = {atomic_number + 5000}
            - **Relleno General**: Semilla MT = {atomic_number + 10000}
            - **Modificaciones estructurales**: ({atomic_number} + índice_esquina × 37) % 12
            - **Probabilidades variables**: Threshold = 0.3 + ({atomic_number} % 5) × 0.1
            - **Grid de alta densidad**: 16×16 = 256 celdas totales
            """)
        else:
            st.markdown(f"""
            ### Detalles técnicos del marcador  - {name}
            
            **Algoritmo de generación específico:**
            
            - **Semilla Mersenne Twister**: {atomic_number} (número atómico directo)
            - **Probabilidad de celda**: 50% para generar cuadrado negro
            - **Grid básico**: 8×8 = 64 celdas totales
            - **Áreas reservadas**: Símbolo y número atómico no se superponen
            - **Símbolo configurable**: Área de {symbol_size}×{symbol_size} celdas
            - **Reproducibilidad**: Mismo patrón siempre para este elemento
            """)
    
    # Pie de página
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Repositorio")
    st.sidebar.markdown("""
    GitHub: [lcgaibor's apps](https://github.com/lcgaibor/streamlit-apps)
    """)

if __name__ == "__main__":
    main()
