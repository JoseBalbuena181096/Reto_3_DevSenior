class StockInsuficienteError(Exception):
    """Excepción lanzada cuando no hay suficiente stock de un producto"""
    def __init__(self, producto, cantidad_solicitada, stock_disponible):
        self.producto = producto
        self.cantidad_solicitada = cantidad_solicitada
        self.stock_disponible = stock_disponible
        self.message = f"Stock insuficiente para {producto}. Solicitado: {cantidad_solicitada}, Disponible: {stock_disponible}"
        super().__init__(self.message)

class CantidadInvalidaError(Exception):
    """Excepción lanzada cuando se ingresa una cantidad inválida"""
    def __init__(self, mensaje="La cantidad debe ser un número entero positivo"):
        self.message = mensaje
        super().__init__(self.message)

class ProductoNoSeleccionadoError(Exception):
    """Excepción lanzada cuando no se selecciona un producto"""
    def __init__(self, mensaje="Debe seleccionar un producto"):
        self.message = mensaje
        super().__init__(self.message)