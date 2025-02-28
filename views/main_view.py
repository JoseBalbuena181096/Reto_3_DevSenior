import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import ttk, messagebox
from controllers.producto_controller import ProductoController
from controllers.venta_controller import VentaController
from utils.excepciones import StockInsuficienteError, CantidadInvalidaError, ProductoNoSeleccionadoError
from views.carrito_view import CarritoFrame
from views.historial_view import HistorialVentasWindow

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

        # Frame de búsqueda 
        self.search_frame = ttk.Frame(self.productos_frame)
        self.search_frame.pack(fill=tk.X, padx=5, pady=5)

        # Campo de búsqueda
        ttk.Label(self.search_frame, text='Buscar:').pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self.search_frame, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Botón de búsquda
        self.search_button = ttk.Button(self.search_frame, text="Buscar", command=self.buscar_productos)
        self.search_button.pack(side=tk.LEFT, padx=5)

        # Frame para mostrar los productos
        self.productos_list_frame = ttk.Frame(self.productos_frame)
        self.productos_list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Crear Treeview para mostrar productos
        self.crear_tabla_productos()

        # Frame para cantidad y botón agregar
        self.cantidad_frame = ttk.Frame(self.productos_frame)
        self.cantidad_frame.pack(fill=tk.X, padx=5, pady=5)

        # Entrada para cantidad
        ttk.Label(self.cantidad_frame, text='Cantidad').pack(side=tk.LEFT, padx=5)
        self.cantidad_var = tk.StringVar(value='1')
        self.cantidad_entry = ttk.Entry(self.cantidad_frame, textvariable=self.cantidad_var,  width=5)
        self.cantidad_entry.pack(side=tk.LEFT, padx=5)

        # Botón para agregar al carrito
        self.agregar_button = ttk.Button(
            self.cantidad_frame,
            text="Agregar al carrito",
            command=self.agregar_al_carrito
        )
        self.agregar_button.pack(side=tk.LEFT, padx=5)

        # Botón para ver historial
        self.historial_button = ttk.Button(
            self.productos_frame,
            text="Ver historial de Ventas",
            command=self.ver_historial
        )
        self.historial_button.pack(side=tk.BOTTOM, padx=5, pady=10, anchor=tk.E)



        
    def agregar_al_carrito(self):
        """Agrega un producto al carrito"""
        try:
            # Obtener producto seleccionado
            seleccion = self.productos_tree.selection()
            if not seleccion:
                raise ProductoNoSeleccionadoError()
            
            # Obtener ID del producto seleccionado
            producto_id = self.productos_tree.item(seleccion[0], "values")[0]
            
            # Obtener cantidad
            cantidad = self.cantidad_var.get()
            
            # Agregar al carrito (esto validará el stock)
            self.venta_controller.agregar_al_carrito(producto_id, cantidad)
            
            # Actualizar vista del carrito
            self.carrito_frame.actualizar_carrito()
            
            # Limpiar selección
            self.productos_tree.selection_remove(seleccion)
            
            # Recargar productos para mostrar stock actualizado
            self.cargar_productos()
            
                        # Restablecer cantidad a 1
            self.cantidad_var.set("1")
            
        except (StockInsuficienteError, CantidadInvalidaError, ProductoNoSeleccionadoError) as e:
            messagebox.showerror("Error", str(e.message))
        except Exception as e:
             messagebox.showerror("Error", f"Ocurrió un error inesperado: {str(e)}")

    def crear_tabla_productos(self):
        """Crea la tabla para mostrar los productos"""
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.productos_list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview (tabla)
        columns = ("id", "nombre", "precio", "stock")
        self.productos_tree = ttk.Treeview(
            self.productos_list_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set
        )
        
        # Configurar columnas
        self.productos_tree.heading("id", text="ID")
        self.productos_tree.heading("nombre", text="Producto")
        self.productos_tree.heading("precio", text="Precio")
        self.productos_tree.heading("stock", text="Stock")
        
        # Ajustar ancho de columnas
        self.productos_tree.column("id", width=50)
        self.productos_tree.column("nombre", width=200)
        self.productos_tree.column("precio", width=100)
        self.productos_tree.column("stock", width=100)
        
        # Empaquetar Treeview
        self.productos_tree.pack(fill=tk.BOTH, expand=True)
        
        # Configurar scrollbar
        scrollbar.config(command=self.productos_tree.yview)


    def ver_historial(self):
        """  Abre la ventana del historial de ventas """
        HistorialVentasWindow(self)

    def cargar_productos(self):
        """Carga los productos en la tabla"""
        # Limpiar tabla
        for item in self.productos_tree.get_children():
            self.productos_tree.delete(item)
        
        # Obtener productos del controlador
        productos = ProductoController.obtener_productos()
        
        # Insertar productos en la tabla
        for producto in productos:
            self.productos_tree.insert("", tk.END, values=producto)

    def buscar_productos(self):
        """Busca productos por nombre"""
        texto_busqueda = self.search_var.get()
        
        # Si está vacío, mostrar todos los productos
        if not texto_busqueda:
            self.cargar_productos()
            return
        
        # Limpiar tabla
        for item in self.productos_tree.get_children():
            self.productos_tree.delete(item)
        
        # Buscar productos
        productos = ProductoController.buscar_productos(texto_busqueda)
        
        # Insertar productos en la tabla
        for producto in productos:
            self.productos_tree.insert("", tk.END, values=producto)


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

# iniciar_aplicacion()