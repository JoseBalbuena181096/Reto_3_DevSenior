import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as  tk
from tkinter import ttk
from controllers.venta_controller import VentaController

class HistorialVentasWindow(tk.Toplevel):
    """Ventana para mostrar el historial de ventas"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Historial de Ventas")
        self.geometry("800x600")
        self.resizable(True, True)
        
        # Hacer ventana modal
        self.transient(parent)
        self.grab_set()
        
        # Configurar la ventana para mostrar el historial
        self.crear_widgets()
        
        # Cargar datos
        self.cargar_historial()

    def crear_widgets(self):
        """Crea los widgets de la ventana"""
        # Frame principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Label de título
        titulo_label = ttk.Label(
            main_frame, 
            text="Historial de Ventas", 
            font=("Arial", 16, "bold")
        )
        titulo_label.pack(pady=10)
        
        # Frame para tabla
        table_frame = ttk.Frame(main_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Crear tabla
        self.crear_tabla_ventas(table_frame)
        
        # Frame para detalles
        self.detalle_frame = ttk.LabelFrame(main_frame, text="Detalles de Venta")
        self.detalle_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Crear tabla de detalles
        self.crear_tabla_detalles(self.detalle_frame)
        
        # Etiqueta para ganancia total
        self.ganancia_label = ttk.Label(
            main_frame, 
            text="Ganancia Total: $0.00", 
            font=("Arial", 12, "bold")
        )
        self.ganancia_label.pack(side=tk.RIGHT, padx=5, pady=10)
        
        # Botón para cerrar
        cerrar_button = ttk.Button(main_frame, text="Cerrar", command=self.destroy)
        cerrar_button.pack(side=tk.RIGHT, padx=5, pady=10)
        
