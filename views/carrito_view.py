import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import ttk, messagebox

class CarritoFrame(ttk.LabelFrame):
    """ Frame para mostrar el carrito de compras """
    
    def __init__(self, parent, venta_controller, finalizar_callback):
        super().__init__(parent, text="Carrito de Compras")
        self.venta_controller = venta_controller
        self.finalizar_callback = finalizar_callback

        # Crear elementos de la interfaz
        self.crear_widgets()

        # Actualizar carrito
        self.actualizar_carrito()

    def crear_widgets(self):
        """Crea los widgets del carrito"""
        # Frame para la tabla
        self.table_frame = ttk.Frame(self)
        self.table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Crear tabla de carrito
        self.crear_tabla_carrito()
        
        # Frame para botones y total
        self.actions_frame = ttk.Frame(self)
        self.actions_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Etiqueta para mostrar el total
        self.total_label = ttk.Label(
            self.actions_frame, 
            text="Total: $0.00", 
            font=("Arial", 12, "bold")
        )
        self.total_label.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Botón para eliminar item
        self.eliminar_button = ttk.Button(
            self.actions_frame,
            text="Eliminar Seleccionado",
            command=self.eliminar_item
        )
        self.eliminar_button.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Botón para finalizar compra
        self.finalizar_button = ttk.Button(
            self,
            text="Finalizar Compra",
            command=self.finalizar_callback
        )
        self.finalizar_button.pack(side=tk.BOTTOM, padx=5, pady=10, fill=tk.X)
        
        # Botón para limpiar carrito
        self.limpiar_button = ttk.Button(
            self,
            text="Limpiar Carrito",
            command=self.limpiar_carrito
        )
        self.limpiar_button.pack(side=tk.BOTTOM, padx=5, pady=5, fill=tk.X)


    def crear_tabla_carrito(self):
        """Crea la tabla para mostrar los items del carrito"""
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.table_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview (tabla)
        columns = ("producto", "precio", "cantidad", "subtotal")
        self.carrito_tree = ttk.Treeview(
            self.table_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set
        )
        
        # Configurar columnas
        self.carrito_tree.heading("producto", text="Producto")
        self.carrito_tree.heading("precio", text="Precio")
        self.carrito_tree.heading("cantidad", text="Cantidad")
        self.carrito_tree.heading("subtotal", text="Subtotal")
        
        # Ajustar ancho de columnas
        self.carrito_tree.column("producto", width=200)
        self.carrito_tree.column("precio", width=100)
        self.carrito_tree.column("cantidad", width=100)
        self.carrito_tree.column("subtotal", width=100)
        
        # Empaquetar Treeview
        self.carrito_tree.pack(fill=tk.BOTH, expand=True)
        
        # Configurar scrollbar
        scrollbar.config(command=self.carrito_tree.yview)

    def actualizar_carrito(self):
        """Actualiza la vista del carrito"""
        # Limpiar tabla
        for item in self.carrito_tree.get_children():
            self.carrito_tree.delete(item)
        
        # Obtener items del carrito
        items = self.venta_controller.obtener_carrito()
        
        # Insertar items en la tabla
        for item in items:
            self.carrito_tree.insert(
                "", tk.END, 
                values=(
                    item['nombre'],
                    f"${item['precio']:.2f}",
                    item['cantidad'],
                    f"${item['subtotal']:.2f}"
                )
            )
        
        # Actualizar total
        total = self.venta_controller.obtener_total()
        self.total_label.config(text=f"Total: ${total:.2f}")

    def eliminar_item(self):
        """ Eliminar un item seleccionado del carrito """
        seleccion = self.carrito_tree.selection()
        if not seleccion:
            messagebox.showinfo('Aviso', 'Seleccione u producto para eliminar')
            return
        
        # obtener indice del item seleccionado
        indice = self.carrito_tree.index(seleccion[0])

        # Eliminar del controlador
        self.venta_controller.eliminar_del_carrito(indice)

        # Actualizar vista
        self.actualizar_carrito()

    def limpiar_carrito(self):
        """ Limpia todo el carrito """
        if not self.venta_controller.obtener_carrito():
            return

        confirmacion =  messagebox.askyesno(
            "Confirmar acción",
            "¿Está seguro de limpiar el carrito?"
        )

        if confirmacion:
            self.venta_controller.lipiar_carrito()
            self.actualizar_carrito()
        
        