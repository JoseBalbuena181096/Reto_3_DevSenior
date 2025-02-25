import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Then use your import
from models.database import DatabaseManager

class ProductoModel:
    """ Modelo para gestionar los productos """

    @staticmethod
    def obtener_todos():
        """" Obtiene todos los productos de la base de datos """
        db = DatabaseManager()
        conn = db.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id, nombre, precio, stock FROM productos ORDER BY nombre")
        productos = cursor.fetchall()
        return productos

    @staticmethod
    def obtener_por_id(producto_id):
        """ Obtiene un producto por su ID """
        db = DatabaseManager()
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, precio, stock FROM productos WHERE id = ?", (producto_id,))
        producto = cursor.fetchone()
        return producto
    
    @staticmethod
    def actualizar_stock(producto_id, cantidad):
        """ Actualiza el stock de un producto """
        db = DatabaseManager()
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE productos SET stock = stock - ? WHERE id = ?", (cantidad, producto_id))
        conn.commit()

    @staticmethod
    def buscar_por_nombre(nombre):
        """ Buscar productos por nombre (parcial) """
        db = DatabaseManager()
        conn = db.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id, nombre, precio, stock FROM productos WHERE nombre LIKE ?", (f'%{nombre}%',))
        productos = cursor.fetchall()
        return productos

    @staticmethod
    def Verificar_stock(producto_id, cantidad):
        """ Verifica si hay suficiente stock de un producto """
        producto = ProductoModel.obtener_por_id(producto_id)
        if producto:
            return producto[3] >= cantidad
        return False
        


# productos = ProductoModel.obtener_todos()
# print(productos)

# producto = ProductoModel.obtener_por_id(1)
# print(producto)

# ProductoModel.actualizar_stock(1, 10)

# producto = ProductoModel.obtener_por_id(1)
# print(producto)

# producto = ProductoModel.buscar_por_nombre('Fresa')
# print(producto)