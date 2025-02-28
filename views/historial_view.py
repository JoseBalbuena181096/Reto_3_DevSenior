import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import ttk
from controllers.venta_controller import VentaController

class HistorialVentasWindow(tk.Toplevel):
    """Ventana para mostrar el historial de ventas"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Historial de Ventas")
        self.geometry("800x700")
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
    
    def crear_tabla_ventas(self, parent):
        """Crea la tabla para mostrar las ventas"""
        # Frame para table + scrollbar
        frame_table = ttk.Frame(parent)
        frame_table.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_table)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview (tabla)
        columns = ("id", "fecha", "total", "items")
        self.ventas_tree = ttk.Treeview(
            frame_table,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set
        )
        
        # Configurar columnas
        self.ventas_tree.heading("id", text="ID")
        self.ventas_tree.heading("fecha", text="Fecha")
        self.ventas_tree.heading("total", text="Total")
        self.ventas_tree.heading("items", text="Items")
        
        # Ajustar ancho de columnas
        self.ventas_tree.column("id", width=50)
        self.ventas_tree.column("fecha", width=150)
        self.ventas_tree.column("total", width=100)
        self.ventas_tree.column("items", width=400)
        
        # Empaquetar Treeview
        self.ventas_tree.pack(fill=tk.BOTH, expand=True)
        
        # Configurar scrollbar
        scrollbar.config(command=self.ventas_tree.yview)
        
        # Vincular evento de selección
        self.ventas_tree.bind("<<TreeviewSelect>>", self.mostrar_detalles)
    
    def crear_tabla_detalles(self, parent):
        """Crea la tabla para mostrar los detalles de venta"""
        # Frame para table + scrollbar
        frame_table = ttk.Frame(parent)
        frame_table.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_table)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview (tabla)
        columns = ("producto", "cantidad", "precio", "subtotal")
        self.detalles_tree = ttk.Treeview(
            frame_table,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set
        )
        
        # Configurar columnas
        self.detalles_tree.heading("producto", text="Producto")
        self.detalles_tree.heading("cantidad", text="Cantidad")
        self.detalles_tree.heading("precio", text="Precio Unitario")
        self.detalles_tree.heading("subtotal", text="Subtotal")
        
        # Ajustar ancho de columnas
        self.detalles_tree.column("producto", width=200)
        self.detalles_tree.column("cantidad", width=100)
        self.detalles_tree.column("precio", width=100)
        self.detalles_tree.column("subtotal", width=100)
        
        # Empaquetar Treeview
        self.detalles_tree.pack(fill=tk.BOTH, expand=True)
        
        # Configurar scrollbar
        scrollbar.config(command=self.detalles_tree.yview)
    
    def cargar_historial(self):
        """Carga el historial de ventas en la tabla"""
        # Obtener historial
        historial = VentaController.obtener_historial_ventas()
        
        # Limpiar tabla
        for item in self.ventas_tree.get_children():
            self.ventas_tree.delete(item)
        
        # Insertar ventas en la tabla
        for venta in historial:
            # Contar items
            num_items = len(venta['items'])
            
            # Insertar en tabla
            self.ventas_tree.insert(
                "", tk.END, 
                values=(
                    venta['id'],
                    venta['fecha'],
                    f"${venta['total']:.2f}",
                    f"{num_items} producto(s)"
                ),
                tags=(str(venta['id']),)
            )
        
        # Actualizar ganancia total
        ganancia_total = VentaController.obtener_ganancia_total()
        self.ganancia_label.config(text=f"Ganancia Total: ${ganancia_total:.2f}")
    
    def mostrar_detalles(self, event):
        """Muestra los detalles de una venta seleccionada"""
        # Obtener item seleccionado
        seleccion = self.ventas_tree.selection()
        if not seleccion:
            return
        
        # Obtener ID de la venta
        venta_id = self.ventas_tree.item(seleccion[0], "tags")[0]
        
        # Obtener historial completo
        historial = VentaController.obtener_historial_ventas()
        
        # Buscar la venta seleccionada
        venta_seleccionada = None
        for venta in historial:
            if str(venta['id']) == venta_id:
                venta_seleccionada = venta
                break
        
        if not venta_seleccionada:
            return
        
        # Limpiar tabla de detalles
        for item in self.detalles_tree.get_children():
            self.detalles_tree.delete(item)
        
        # Insertar detalles
        for item in venta_seleccionada['items']:
            self.detalles_tree.insert(
                "", tk.END, 
                values=(
                    item['producto'],
                    item['cantidad'],
                    f"${item['precio']:.2f}",
                    f"${item['subtotal']:.2f}"
                )
            )
        
    