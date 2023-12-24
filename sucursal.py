import sqlite3


class Sucursal:

  def __init__(self, conexion):
    self.conexion = conexion

  def crear_tabla_sucursal(self):
    try:
      self.conexion.cursor.execute('''
                CREATE TABLE IF NOT EXISTS SUCURSAL (
                    id INTEGER PRIMARY KEY,
                    nombre TEXT,
                    direccion TEXT,
                    cuit INTEGER
                )
            ''')

      self.conexion.conexion.commit()
      return True
    except sqlite3.Error as e:
      print(f"Error al crear la tabla de Sucursales: {e}")
      return False

  def traer_cuit_por_nombre_sucursal(self, nombre_sucursal):
    try:
      self.conexion.cursor.execute(
          '''
            SELECT cuit FROM SUCURSAL WHERE nombre = ?
        ''', (nombre_sucursal, ))
      cuit = self.conexion.cursor.fetchone()
      return cuit[0] if cuit else None
    except sqlite3.Error as e:
      print(f"Error al traer el CUIT por nombre de Sucursal: {e}")
      return None

  def obtener_id_sucursal_por_username(self, username):
    try:
      cursor = self.conexion.cursor()
      cursor.execute(
          '''
            SELECT id_sucursal FROM EMPLEADO
            WHERE user = ?
        ''', (username, ))

      id_sucursal = cursor.fetchone()

      if id_sucursal:
        return id_sucursal[0]
      else:
        return None

    except sqlite3.Error as e:
      print(f"Error al obtener ID de sucursal por nombre de usuario: {e}")
      return None

  def traer_cuit_por_id_sucursal(self, id_sucursal):
    try:
      self.conexion.cursor.execute(
          '''
            SELECT cuit FROM SUCURSAL WHERE id = ?
        ''', (id_sucursal, ))
      cuit = self.conexion.cursor.fetchone()
      return cuit[0] if cuit else None
    except sqlite3.Error as e:
      print(f"Error al traer el CUIT por ID de Sucursal: {e}")
      return None

  def mostrar_sucursales(self):
    try:
      self.conexion.cursor.execute("SELECT * FROM SUCURSAL")
      sucursales = self.conexion.cursor.fetchall()
      return sucursales
    except sqlite3.Error as e:
      print(f"Error al mostrar las sucursales: {e}")
      return []

  def ingresar_sucursal(self, nombre, direccion, cuit):
    if not all(
        isinstance(arg, (str, int)) for arg in (nombre, direccion, cuit)):
      return False

    try:
      query = "INSERT INTO SUCURSAL (nombre, cuit, direccion) VALUES (?, ?, ?)"
      self.conexion.cursor.execute(query, (nombre, cuit, direccion))
      self.conexion.conexion.commit()
      return True
    except sqlite3.Error as e:
      print(f"Error al ingresar la sucursal: {e}")
      return False

  def mostrarSucursalPorId(self, id):
    try:
      self.conexion.cursor.execute("SELECT * FROM SUCURSAL where id=?", (id, ))
      pelicula = self.conexion.cursor.fetchone()
      return pelicula
    except sqlite3.Error as e:
      print(f"Error al mostrar el nombre de las sucursales: {e}")
      return []

  def editar_sucursal(self, id, nombre, direccion, cuit):
    if not (isinstance(nombre, str) and isinstance(direccion, str)
            and isinstance(cuit, int)):
      return False
    try:
      self.conexion.cursor.execute(
          "UPDATE SUCURSAL SET nombre=?, direccion=?, cuit=? WHERE id=?", (
              nombre,
              direccion,
              cuit,
              id,
          ))
      self.conexion.conexion.commit()
      return True
    except sqlite3.Error as e:
      print(f"Error al modificar la sucursal: {e}")
      return False

  def eliminar_sucursal(self, id):
    try:
      self.conexion.cursor.execute("DELETE FROM SUCURSAL WHERE id = ?", (id, ))
      self.conexion.conexion.commit()
      return True
    except sqlite3.Error as e:
      print(f"Error al eliminar la sucursal: {e}")
      return False
