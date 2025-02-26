import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.producto import ProductoModel
from utils.excepciones import StockInsuficienteError, CantidadInvalidaError

class ProductoController:
    """ Controlador para gestionar las operaciones con productos """

    @staticmethod
    def obtener_productos():
        """ Obtener todos los productos disponibles """
        return ProductoModel.obtener_todos()

    @staticmethod
    def verificar_disponibilidad(producto_id, cantidad):
        """ Verifica si hay sufuciente stock de un producto """
        try:
            cantidad = int(cantidad)
            if cantidad <= 0:
                raise CantidadInvalidaError()
            
            producto = ProductoModel.obtener_por_id(producto_id)
            if not producto:
                return False
            if producto[3] < cantidad:
                raise StockInsuficienteError(producto[1], cantidad, producto[3])
            return True

        except ValueError:
            raise CantidadInvalidaError()
    
    @staticmethod
    def obtener_info_producto(producto_id):
        """ Obtiene la información de un producto por su ID """
        return ProductoModel.obtener_por_id(producto_id)

    @staticmethod
    def actualizar_stock(producto_id, cantidad):
        """ Actualiza el stock de un producto """
        ProductoModel.actualizar_stock(producto_id, cantidad)
    
    @staticmethod
    def buscar_productos(nombre):
        """ Buscar productos por nombre """
        return ProductoModel.buscar_por_nombre(nombre)

# print(ProductoController.obtener_productos())
# print(ProductoController.verificar_disponibilidad(1, 10))
# print(ProductoController.obtener_info_producto(1))
# print(ProductoController.actualizar_stock(1, -100))
# print(ProductoController.obtener_info_producto(1))
# print(ProductoController.buscar_productos('Tomate'))