import sqlite3

conexion = sqlite3.connect("app.db")
cursor = conexion.cursor()

# Se corrigen los ADD CONSTRAINT del esquema original para ser válidos en SQLite
cursor.executescript("""
CREATE TABLE IF NOT EXISTS categoria(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS gasto(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    monto INT NOT NULL,
    fecha DATE NOT NULL,
    categoria_id INT NOT NULL,
    CONSTRAINT gasto_fk FOREIGN KEY (categoria_id) REFERENCES categoria (id) ON DELETE RESTRICT ON UPDATE CASCADE
);
""")

# Insertamos una categoría de prueba para que tengas algo que mostrar
cursor.execute("INSERT INTO categoria (nombre) VALUES ('Comida'), ('Transporte')")

conexion.commit()
conexion.close()
print("Base de datos creada exitosamente.")