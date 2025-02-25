import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Then use your import
from models.database import DatabaseManager

from datetime import datetime

class VentaModel:
    """ Modelo para gestionar las ventas """
    
    @staticmethod
    def registrar_venta(items_carrito, total):
        """Registra una nueva venta con sus detalles"""
        db = DatabaseManager()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Insertar la venta
        cursor.execute(
            "INSERT INTO ventas (fecha, total) VALUES (?, ?)",
            (fecha_actual, total)
        )
        
        # Obtener el ID de la venta recién insertada
        venta_id = cursor.lastrowid
        
        # Insertar los detalles de la venta
        for item in items_carrito:
            producto_id = item['producto_id']
            cantidad = item['cantidad']
            precio_unitario = item['precio']
            subtotal = item['subtotal']
            
            cursor.execute(
                """INSERT INTO detalle_ventas 
                   (venta_id, producto_id, cantidad, precio_unitario, subtotal) 
                   VALUES (?, ?, ?, ?, ?)""",
                (venta_id, producto_id, cantidad, precio_unitario, subtotal)
            )
        
        conn.commit()
        return venta_id

    @staticmethod
    def obtener_historial():
        """ Obtiene el historial de ventas con sus detalles """
        db = DatabaseManager()
        conn = db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT v.id, v.fecha, v.total, 
                   p.nombre, dv.cantidad, dv.precio_unitario, dv.subtotal
            FROM ventas v
            JOIN detalle_ventas dv ON v.id = dv.venta_id
            JOIN productos p ON dv.producto_id = p.id
            ORDER BY v.fecha DESC
        """)

        resultados = cursor.fetchall()
        
        # Organizar los resultados por venta
        historial = {}
        for venta_id, fecha, total, producto, cantidad, precio, subtotal in resultados:
            if venta_id not in historial:
                historial[venta_id] = {
                    'id' : venta_id,
                    'fecha' : fecha,
                    'total' : total,
                    'items' : []
                }
            historial[venta_id]['items'].append({
                'producto': producto,
                'cantidad': cantidad,
                'precio': precio,
                'subtotal': subtotal 
            })
        return list(historial.values())

    @staticmethod
    def obtener_ganancia_total():
        """ Obtiene la ganancia total de todas las ventas """
        db = DatabaseManager()
        conn = db.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT SUM(total) FROM ventas")
        resultado = cursor.fetchone()[0]

        return resultado if resultado else 0.0

# carrito = [
#     {
#         'producto_id': 1,
#         'cantidad': 10,
#         'precio': 2.5,
#         'subtotal': 25        
#     },
#     {
#         'producto_id': 2,
#         'cantidad': 10,
#         'precio': 1.8,
#         'subtotal': 18        
#     }
# ]


# #print(VentaModel.obtener_historial())
# print(VentaModel.obtener_ganancia_total())
