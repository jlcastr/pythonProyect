
import sqlite3
from config.db_setup import crear_conexion_y_tablas
from View.menu import menubar
import Controller.utils as utils
from View.Screen import crear_pantalla_principal

# Crear la base de datos y las tablas si no existen
crear_conexion_y_tablas("config/sqliteDB.db")

# Conexión a la base de datos
conn = sqlite3.connect("config/sqliteDB.db")
cursor = conn.cursor()

crear_pantalla_principal(conn, cursor, menubar)
conn.close()
#test
#te