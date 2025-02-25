import sqlite3
import os

class DatabaseManager:
    """Clase singleton para gestionar la conexión a la base de datos"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance.conn = None
            cls._instance.initialize_db()
        return cls._instance
    
    def initialize_db(self):
        """Inicializa la base de datos si no existe"""
        # Verificar si existe el directorio data
        if not os.path.exists('data'):
            os.makedirs('data')
            
        self.conn = sqlite3.connect('data/fruber.db')
        self.create_tables()
    
    def create_tables(self):
        """Crea las tablas necesarias si no existen"""
        cursor = self.conn.cursor()
        
        # Tabla de productos
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
        ''')
        
        # Tabla de ventas
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            total REAL NOT NULL
        )
        ''')
        
        # Tabla de detalles de venta (relación muchos a muchos)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS detalle_ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            venta_id INTEGER NOT NULL,
            producto_id INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            precio_unitario REAL NOT NULL,
            subtotal REAL NOT NULL,
            FOREIGN KEY (venta_id) REFERENCES ventas (id),
            FOREIGN KEY (producto_id) REFERENCES productos (id)
        )
        ''')
        
        # Verificar si ya hay productos, si no, insertar algunos por defecto
        cursor.execute("SELECT COUNT(*) FROM productos")
        if cursor.fetchone()[0] == 0:
            self.insertar_productos_default()
            
        self.conn.commit()
    
    def insertar_productos_default(self):
        """Inserta productos predeterminados en la base de datos"""
        productos_default = [
            ("Manzana", 2.50, 100),
            ("Plátano", 1.80, 150),
            ("Naranja", 1.20, 120),
            ("Pera", 2.00, 80),
            ("Fresa", 3.50, 50),
            ("Lechuga", 1.50, 60),
            ("Tomate", 1.80, 90),
            ("Zanahoria", 1.20, 110),
            ("Cebolla", 1.00, 100),
            ("Papa", 0.90, 200)
        ]
        
        cursor = self.conn.cursor()
        cursor.executemany(
            "INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)",
            productos_default
        )
        self.conn.commit()
    
    def get_connection(self):
        """Retorna la conexión a la base de datos"""
        if self.conn is None:
            self.initialize_db()
        return self.conn
    
    def close_connection(self):
        """Cierra la conexión a la base de datos"""
        if self.conn:
            self.conn.close()
            self.conn = None
    


db = DatabaseManager()
db.insertar_productos_default()

