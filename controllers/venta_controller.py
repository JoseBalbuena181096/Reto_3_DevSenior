import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.venta import VentaModel
from controllers.producto_controller import ProductoController

class VentaController:
    """Controlador para gestionar las operaciones de ventas"""
    
    def __init__(self):
        self.carrito = []
        self.total = 0.0
    
    def agregar_al_carrito(self, producto_id, cantidad):
        """Agrega un producto al carrito de compras"""
        # Verificar disponibilidad (lanzará excepción si no hay stock)
        ProductoController.verificar_disponibilidad(producto_id, cantidad)
        
        # Obtener información del producto
        producto = ProductoController.obtener_info_producto(producto_id)
        
        # Verificar si el producto ya está en el carrito
        for item in self.carrito:
            if item['producto_id'] == producto_id:
                item['cantidad'] += int(cantidad)
                item['subtotal'] = round(item['cantidad'] * item['precio'], 2)
                self._actualizar_total()
                return
        
        # Agregar nuevo item al carrito
        nuevo_item = {
            'producto_id': producto_id,
            'nombre': producto[1],
            'precio': producto[2],
            'cantidad': int(cantidad),
            'subtotal': round(producto[2] * int(cantidad), 2)
        }
        
        self.carrito.append(nuevo_item)
        self._actualizar_total()
    
    def eliminar_del_carrito(self, indice):
        """Elimina un producto del carrito de compras"""
        if 0 <= indice < len(self.carrito):
            self.carrito.pop(indice)
            self._actualizar_total()
    
    def _actualizar_total(self):
        """Actualiza el total de la compra"""
        self.total = sum(item['subtotal'] for item in self.carrito)
        self.total = round(self.total, 2)
    
    def obtener_carrito(self):
        """Obtiene los items del carrito"""
        return self.carrito
    
    def obtener_total(self):
        """Obtiene el total de la compra"""
        return self.total
    
    def finalizar_compra(self):
        """Finaliza la compra actual"""
        if not self.carrito:
            return False
        
        # Actualizar stock de productos
        for item in self.carrito:
            ProductoController.actualizar_stock(item['producto_id'], item['cantidad'])
        
        # Registrar la venta
        venta_id = VentaModel.registrar_venta(self.carrito, self.total)
        
        # Limpiar el carrito
        self.carrito = []
        self._actualizar_total()
        
        return venta_id
    
    def limpiar_carrito(self):
        """Limpia el carrito de compras"""
        self.carrito = []
        self._actualizar_total()
    
    @staticmethod
    def obtener_historial_ventas():
        """Obtiene el historial de ventas"""
        return VentaModel.obtener_historial()
    
    @staticmethod
    def obtener_ganancia_total():
        """Obtiene la ganancia total de todas las ventas"""
        return VentaModel.obtener_ganancia_total()

# venta = VentaController()
# venta.agregar_al_carrito(1, 10)
# venta.agregar_al_carrito(1, 20)
# venta.agregar_al_carrito(1, 10)
# print(venta.obtener_carrito())
# venta.eliminar_del_carrito(1)
# print(venta.obtener_carrito())
# venta.finalizar_compra()

# print(VentaController.obtener_historial_ventas())
# print(VentaController.obtener_ganancia_total())