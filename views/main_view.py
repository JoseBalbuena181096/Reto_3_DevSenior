import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import ttk, messagebox
from controllers.producto_controller import ProductoController
from controllers.venta_controller import VentaController
from utils.excepciones import StockInsuficienteError, CantidadInvalidaError, ProductoNoSeleccionadoError

class MainView(tk.Tk):
    """Vista principal de la aplicación"""
    
    def __init__(self):
        super().__init__()
        self.title("Sistema de Caja Registradora - Fruber")
        self.geometry("1000x600")
        self.resizable(True, True)
        
        # Controlador de ventas (maneja el carrito)
        self.venta_controller = VentaController()
        
        # Configurar estilos
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Usar un tema moderno
        
        # Configurar colores y estilos
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('Header.TLabel', font=('Arial', 14, 'bold'), background='#f0f0f0')
        self.style.configure('TButton', font=('Arial', 10), background='#4CAF50')
        
        # Frame principal
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Crear layout de dos columnas
        self.crear_layout()
        
        # Cargar productos iniciales
        self.cargar_productos()

    def crear_layout(self):
        pass

    def cargar_productos(self):
        pass