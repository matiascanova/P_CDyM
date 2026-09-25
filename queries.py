import sqlite3

def conectar():
    return sqlite3.connect("app.db")

def insertarGasto(monto,fecha,categoria_id):
    conexion = conectar()
    cursor = conexion.cursor()

    query ="""
        INSERT INTO gasto (monto,fecha,categoria_id)
        VALUES (:monto, :fecha, :categoria_id)
    """
    parametros= {"monto": monto, "fecha":fecha, "categoria_id":categoria_id}

    cursor.execute(query, parametros)
    conexion.commit()
    conexion.close()

def actualizarGasto(id,monto,fecha,categoria_id):
    conexion = conectar()
    cursor = conexion.cursor()
    query ="""
            UPDATE gasto
            SET monto= :monto,
                fecha= :fecha,
                categoria_id= :categoria_id
            WHERE id=:id
        """
    parametros= {"id": id,"monto": monto, "fecha":fecha, "categoria_id":categoria_id}
    cursor.execute(query, parametros)
    conexion.commit()
    conexion.close()

def eliminarGasto(id):
    conexion = conectar()
    cursor = conexion.cursor()

    query ="""
        DELETE FROM gasto
        WHERE id=:id
    """
    parametros= {"id":id}

    cursor.execute(query, parametros)
    conexion.commit()
    conexion.close()

def listarGastosIntervalo(fecha1,fecha2):
    conexion = conectar()
    cursor = conexion.cursor()

    query = """
        SELECT id, monto, fecha, categoria_id
        FROM gasto
        WHERE fecha BETWEEN :fecha1 AND :fecha2
        ORDER BY fecha DESC
    """
    parametros= {"fecha1":fecha1, "fecha2":fecha2}

    cursor.execute(query, parametros)
    res= cursor.fetchall()
    conexion.close()
    return [dict(fila) for fila in res]

def insertarCategoria(nombre):
    conexion = conectar()
    cursor = conexion.cursor()

    query = """
        INSERT INTO categoria (nombre)
        VALUES (:nombre)
    """
    parametros = {"nombre": nombre}

    cursor.execute(query, parametros)
    conexion.commit()
    conexion.close()

def actualizarCategoria(id, nombre):
    conexion = conectar()
    cursor = conexion.cursor()

    query = """
        UPDATE categoria
        SET nombre = :nombre
        WHERE id = :id
    """
    parametros = {"id": id, "nombre": nombre}

    cursor.execute(query, parametros)
    conexion.commit()
    conexion.close()

def eliminarCategoria(id):
    conexion = conectar()
    cursor = conexion.cursor()

    # Nota: Si una categoría tiene gastos asociados se enoja sql y no permite
    
    query = """
        DELETE FROM categoria
        WHERE id = :id
    """
    parametros = {"id": id}

    cursor.execute(query, parametros)
    conexion.commit()
    conexion.close()

def listarCategorias():
    conexion = conectar()
    cursor = conexion.cursor()

    query = """
        SELECT id, nombre
        FROM categoria
        ORDER BY nombre ASC
    """

    cursor.execute(query)
    res = cursor.fetchall()
    conexion.close()

    return [dict(fila) for fila in res]