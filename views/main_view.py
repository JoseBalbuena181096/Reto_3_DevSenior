import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import ttk, messagebox
from controllers.producto_controller import ProductoController
from controllers.venta_controller import VentaController
from utils.excepciones import StockInsuficienteError, CantidadInvalidaError, ProductoNoSeleccionadoError
from views.carrito_view import CarritoFrame

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
        """ Crea el layout princial de la aplicación """
        # Frame izquierdo para lista de productos
        self.productos_frame = ttk.Labelframe(self.main_frame, text="Productos Disponibles")
        self.productos_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        # Frame derecho para carrito
        # Frame derecho para carrito
        self.carrito_frame = CarritoFrame(self.main_frame, self.venta_controller, self.finalizar_compra)
        self.carrito_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        
        # Configurar peso de las columnas
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

    def cargar_productos(self):
        pass

    def finalizar_compra(self):
        """Finaliza la compra actual"""
        if not self.venta_controller.obtener_carrito():
            messagebox.showinfo("Aviso", "El carrito está vacío")
            return
        
        total = self.venta_controller.obtener_total()
        confirmacion = messagebox.askyesno(
            "Confirmar compra", 
            f"¿Desea finalizar la compra por un total de ${total:.2f}?"
        )
        
        if confirmacion:
            try:
                self.venta_controller.finalizar_compra()
                messagebox.showinfo(
                    "Compra finalizada", 
                    f"La compra se ha registrado correctamente. Total: ${total:.2f}"
                )
                # Actualizar carrito
                self.carrito_frame.actualizar_carrito()
                # Recargar productos
                self.cargar_productos()
            except Exception as e:
                messagebox.showerror("Error", f"Error al finalizar la compra: {str(e)}")


# Función par iniciar la apñicación
def iniciar_aplicacion():
    app = MainView()
    app.mainloop()

iniciar_aplicacion()