import sqlite3


class Turno:

  def __init__(self, conexion):
    self.conexion = conexion

  def crear_tabla_turno(self):
    try:
      self.conexion.cursor.execute('''
                CREATE TABLE IF NOT EXISTS TURNO(
                    id INTEGER PRIMARY KEY,
                    horario TEXT
                )
            ''')
      self.conexion.conexion.commit()
      return True
    except sqlite3.Error as e:
      print(f"Error al crear la tabla de Turno: {e}")
      return False

  def mostrar_turnos(self):
    try:
      self.conexion.cursor.execute("SELECT * FROM TURNO")
      turnos = self.conexion.cursor.fetchall()
      return turnos
    except sqlite3.Error as e:
      print(f"Error al mostrar turnos: {e}")
      return []

  def traerHorarioPorId(self, id):
    try:
      self.conexion.cursor.execute("SELECT horario FROM TURNO where id=?",
                                   (id))
      turno = self.conexion.cursor.fetchall()
      return turno
    except sqlite3.Error as e:
      print(f"Error al traer horario turnos: {e}")
      return ""

  def ingresar_turno(self, horario):
    try:
      self.conexion.cursor.execute("INSERT INTO TURNO (horario) VALUES (?)",
                                   (horario, ))
      self.conexion.conexion.commit()
      return True
    except sqlite3.Error as e:
      print(f"Error al ingresar el turno: {e}")
      return False

  def modificar_turno(self, id, horario):
    try:
      self.conexion.cursor.execute("UPDATE TURNO SET horario=? WHERE id=?",
                                   (horario, id))
      self.conexion.conexion.commit()
      return True
    except sqlite3.Error as e:
      print(f"Error al modificar el turno: {e}")
      return False

  def eliminar_turno(self, id):
    try:
      self.conexion.cursor.execute("DELETE FROM TURNO WHERE id=?", (id, ))
      self.conexion.conexion.commit()
      return True
    except sqlite3.Error as e:
      print(f"Error al eliminar el turno: {e}")
      return False

  def menu_turno(self):
    opcion_turno = 0

    while opcion_turno != "5":
      opcion_turno = input(
          "Menú Turno\n1- Ingresar Turno\n2- Mostrar Turnos\n3- Modificar Turno\n4- Eliminar Turno\n5- Volver al Menú Principal\n"
      )

      if opcion_turno == "1":
        horario = input("Ingrese el horario: ")
        if self.ingresar_turno(horario):
          print("Turno ingresado con éxito.")
        else:
          print("Error al ingresar el turno.")
      elif opcion_turno == "2":
        turnos = self.mostrar_turnos()
        if turnos:
          for turno in turnos:
            print(f"ID: {turno[0]}, Horario: {turno[1]}")
        else:
          print("No hay turnos registrados.")
      elif opcion_turno == "3":
        id_turno = input("Ingrese ID del turno a modificar: ")
        nuevo_horario = input("Ingrese nuevo horario: ")
        if self.modificar_turno(id_turno, nuevo_horario):
          print("Turno modificado con éxito.")
        else:
          print("Error al modificar el turno.")
      elif opcion_turno == "4":
        id_turno = input("Ingrese ID del turno a eliminar: ")
        if self.eliminar_turno(id_turno):
          print("Turno eliminado con éxito.")
        else:
          print("Error al eliminar el turno.")
      elif opcion_turno == "5":
        print("Volviendo al Menú Principal.")
      else:
        print("Opción no válida. Inténtalo de nuevo.")
