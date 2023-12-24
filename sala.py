import sqlite3


class Sala:

  def __init__(self, conexion):
    self.conexion = conexion

  def crear_tabla_sala(self):
    try:
      self.conexion.cursor.execute('''
              CREATE TABLE IF NOT EXISTS SALA(
                  id INTEGER PRIMARY KEY,
                  numero INTEGER,
                  capacidad INTEGER,
                  id_sucursal INTEGER,
                  FOREIGN KEY (id_sucursal) REFERENCES sucursal(id)
              )
          ''')

      self.conexion.conexion.commit()
      return True
    except sqlite3.Error as e:
      print(f"Error al crear la tabla de Salas: {e}")
      return False

  def obtener_max_numero_sala_por_sucursal(self, id_sucursal):
    try:
      self.conexion.cursor.execute(
          "SELECT MAX(numero) FROM sala WHERE id_sucursal = ?",
          (id_sucursal, ))
      max_numero_sala = self.conexion.cursor.fetchone()
      if max_numero_sala is not None:
        return max_numero_sala[0] or 0
      else:
        print(f"No se encontraron salas para la sucursal con ID {id_sucursal}")
        return 0
    except sqlite3.Error as e:
      print(f"Error al obtener el máximo número de sala: {e}")
      return 0

  def mostrar_salas(self):
    try:
      self.conexion.cursor.execute("SELECT * FROM SALA")
      salas = self.conexion.cursor.fetchall()
      return salas
    except sqlite3.Error as e:
      print(f"Error al mostrar salas: {e}")
      return []

  def ingresar_sala(self, numero, capacidad, id_sucursal):
    if not (isinstance(numero, int) and isinstance(capacidad, int)
            and isinstance(id_sucursal, int)):
      return False

    try:
      self.conexion.cursor.execute(
          "INSERT INTO SALA (numero,capacidad,id_sucursal) VALUES (?, ?, ?)",
          (numero, capacidad, id_sucursal))
      self.conexion.conexion.commit()
      return True
    except sqlite3.Error as e:
      print(f"Error al ingresar la sala: {e}")
      return False

  def modificar_sala(self, id, capacidad):
    if not (isinstance(id, int) and isinstance(capacidad, int)):
      return False
    try:
      self.conexion.cursor.execute("UPDATE SALA SET capacidad=? WHERE id=?",
                                   (capacidad, id))
      self.conexion.conexion.commit()
      return True
    except sqlite3.Error as e:
      print(f"Error al modificar la sala: {e}")
      return False

  def eliminarSala(self, id_sala):
    try:
      self.conexion.cursor.execute("DELETE FROM SALA WHERE id = ?",
                                   (id_sala, ))
      self.conexion.conexion.commit()
      return True
    except sqlite3.Error as e:
      print(f"Error al eliminar la sala: {e}")
      return False

  def traerNumeroSalaPorId(self, id_sala):
    try:
      self.conexion.cursor.execute("SELECT numero FROM sala WHERE id = ?",
                                   (id_sala, ))
      numero_sala = self.conexion.cursor.fetchone()
      return numero_sala[0] if numero_sala else "Sala no encontrada"
    except sqlite3.Error as e:
      print(f"Error al obtener el número de sala: {e}")
      return None

  def obtener_capacidad_por_id_sala(self, id_sala):
    try:
      cursor = self.conexion.cursor()
      cursor.execute("SELECT capacidad FROM sala WHERE id = ?", (id_sala, ))
      capacidad = cursor.fetchone()
      if capacidad is not None:
        return capacidad[0]
      else:
        print(f"No se encontró una sala con ID {id_sala}")
        return None
    except sqlite3.Error as e:
      print(f"Error al obtener la capacidad de la sala: {e}")
      return None

  def traer_sala_por_id(self, id_sala):
    try:
      self.conexion.cursor.execute("SELECT * FROM sala WHERE id = ?",
                                   (id_sala, ))
      sala = self.conexion.cursor.fetchone()

      if sala is not None:
        return list(sala)
      else:
        print(f"No se encontró una sala con ID {id_sala}")
        return None
    except sqlite3.Error as e:
      print(f"Error al obtener la sala por ID: {e}")
      return None

  def mostrar_salas_sucursal(self, id_sucursal):
    try:
        self.conexion.cursor.execute(
            "SELECT id, numero FROM sala WHERE id_sucursal = ?", (id_sucursal, ))
        salas = self.conexion.cursor.fetchall()

       
        salas_dict = {str(sala[0]): sala[1] for sala in salas}

        return salas_dict
    except sqlite3.Error as e:
        print(f"Error al obtener las salas por ID de sucursal: {e}")
        return None
