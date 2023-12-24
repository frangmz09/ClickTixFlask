import sqlite3


class Empleado:

  def __init__(self, conexion):
    self.conexion = conexion

  def crear_tabla_empleado(self):
    try:
      self.conexion.cursor.execute('''
                CREATE TABLE IF NOT EXISTS EMPLEADO(
                    id INTEGER PRIMARY KEY,
                    nombre TEXT,
                    apellido TEXT,
                    user TEXT,
                    password TEXT,
                    dni INT,
                    id_sucursal INT,
                    is_admin INT,
                    FOREIGN KEY (id_sucursal) REFERENCES sucursal(id)
                )
            ''')
      self.conexion.conexion.commit()
      return True
    except sqlite3.Error as e:
      print(f"Error al crear el nuevo empleado: {e}")
      return False

  def obtener_id_sucursal_por_username(self, username):
    try:
      self.conexion.cursor.execute(
          '''
            SELECT id_sucursal FROM EMPLEADO
            WHERE user = ?
        ''', (username, ))

      id_sucursal = self.conexion.cursor.fetchone()

      if id_sucursal:
        return id_sucursal[0]
      else:
        return None

    except sqlite3.Error as e:
      print(f"Error al obtener ID de sucursal por nombre de usuario: {e}")
      return None

  def obtener_nombre_por_usuario(self, username):
    try:
      self.conexion.cursor.execute(
          '''
            SELECT nombre FROM EMPLEADO
            WHERE user = ?
        ''', (username, ))

      nombre_empleado = self.conexion.cursor.fetchone()

      if nombre_empleado:
        return nombre_empleado[0]
      else:
        return None

    except sqlite3.Error as e:
      print(f"Error al obtener el nombre del empleado por usuario: {e}")
      return None

  def mostrar_empleados(self):
    try:
      self.conexion.cursor.execute("SELECT * FROM EMPLEADO")
      empleados = self.conexion.cursor.fetchall()
      return empleados
    except sqlite3.Error as e:
      print(f"Error al mostrar los empleados: {e}")
      return []

  def traer_empleado_por_id(self, id_empleado):
    try:
      self.conexion.cursor.execute("SELECT * FROM EMPLEADO WHERE id = ?",
                                   (id_empleado, ))
      empleado = self.conexion.cursor.fetchone()
      return empleado
    except sqlite3.Error as e:
      print(f"Error al traer el empleado por ID: {e}")
      return None

  def traerEmpleadpPorId(self, id):
    try:
      self.conexion.cursor.execute(
          "SELECT nombre,apellido FROM EMPLEADO where id=?", (id))
      nombreYApellido = self.conexion.cursor.fetchall()
      return nombreYApellido
    except sqlite3.Error as e:
      print(f"Error al traer empleado: {e}")
      return ""

  def traerIsAdminEmpleadpPorId(self, id):
    try:
      self.conexion.cursor.execute("SELECT is_admin FROM EMPLEADO where id=?",
                                   (id))
      isAdmin = self.conexion.cursor.fetchall()
      return isAdmin
    except sqlite3.Error as e:
      print(f"Error al traer empleados: {e}")
      return ""

  def traerSucursalEmpleadpPorId(self, id):
    try:
      self.conexion.cursor.execute(
          "SELECT id_sucursal FROM EMPLEADO where id=?", (id))
      idSucursal = self.conexion.cursor.fetchall()
      return idSucursal
    except sqlite3.Error as e:
      print(f"Error al traer empleado: {e}")
      return ""

  def ingresar_empleado(self, nombre, apellido, dni, id_sucursal, is_admin,
                        user, password):
    try:
      self.conexion.cursor.execute(
          "INSERT INTO EMPLEADO (nombre, apellido,dni, id_sucursal,is_admin,user,password) VALUES (?,?,?,?,?,?,?)",
          (
              nombre,
              apellido,
              dni,
              id_sucursal,
              is_admin,
              user,
              password,
          ))

      self.conexion.conexion.commit()
      return True
    except sqlite3.Error as e:
      print(f"Error al ingresar el empleado: {e}")
      return False

  def modificar_empleado(self, nombre, apellido, dni, id_sucursal, is_admin,
                         user, password, id):

    try:
      self.conexion.cursor.execute(
          "UPDATE EMPLEADO SET nombre=?, apellido=?, dni=?, id_sucursal=?,is_admin=?,user=?, password=? WHERE id = ?",
          (
              nombre,
              apellido,
              dni,
              id_sucursal,
              is_admin,
              user,
              password,
              id,
          ))
      self.conexion.conexion.commit()
      return True
    except sqlite3.Error as e:
      print(f"Error al modificar el empleado: {e}")
      return False

  def eliminar_empleado(self, id):
    try:
      self.conexion.cursor.execute("DELETE FROM EMPLEADO WHERE id=?", (id, ))
      self.conexion.conexion.commit()
      return True
    except sqlite3.Error as e:
      print(f"Error al eliminar el empleado: {e}")
      return False

  def verificar_credenciales(self, usuario, contrasena):
    try:
      self.conexion.cursor.execute(
          '''
            SELECT * FROM EMPLEADO
            WHERE user = ? AND password = ?
        ''', (usuario, contrasena))
      empleado = self.conexion.cursor.fetchone()

      return bool(empleado)

    except sqlite3.Error as e:
      print(f"Error al verificar credenciales: {e}")
      return False

  def traerIsAdminEmpleado(self, username, password):
    try:
      self.conexion.cursor.execute(
          '''
            SELECT is_admin FROM EMPLEADO
            WHERE user = ? AND password = ?
            ''', (username, password))
      resultado = self.conexion.cursor.fetchone()

      if resultado:
        is_admin = resultado[0]
        return is_admin
      else:
        return None
    except sqlite3.Error as e:
      print(f"Error al traer is_admin: {e}")
      return None
