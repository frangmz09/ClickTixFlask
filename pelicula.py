import sqlite3


class Pelicula:

  def __init__(self, conexion):
    self.conexion = conexion

  def crear_tabla_pelicula(self):
    try:
      self.conexion.cursor.execute('''
                CREATE TABLE IF NOT EXISTS PELICULA(
                    id INTEGER PRIMARY KEY,
                    titulo TEXT,
                    director TEXT,
                    duracion INT,
                    fecha_estreno TEXT,
                    categoria TEXT
                )
            ''')
      self.conexion.conexion.commit()
      return True
    except sqlite3.Error as e:
      print(f"Error al crear la tabla de Películas: {e}")
      return False

  def mostrar_peliculas(self):
    try:
      self.conexion.cursor.execute("SELECT * FROM PELICULA")
      peliculas = self.conexion.cursor.fetchall()
      return peliculas
    except sqlite3.Error as e:
      print(f"Error al mostrar películas: {e}")
      return []

  def mostrarNombrePelicula(self, id):
    try:
      self.conexion.cursor.execute("SELECT nombre FROM PELICULA where id=?",
                                   (id, ))
      peliculas = self.conexion.cursor.fetchall()
      return peliculas
    except sqlite3.Error as e:
      print(f"Error al mostrar el nombre de las películas: {e}")
      return []

  def mostrarPeliculaPorId(self, id):
    try:
      self.conexion.cursor.execute("SELECT * FROM PELICULA where id=?", (id, ))
      pelicula = self.conexion.cursor.fetchone()
      return pelicula
    except sqlite3.Error as e:
      print(f"Error al mostrar el nombre de las películas: {e}")
      return []

  def ingresar_pelicula(self, titulo, director, duracion, fecha_estreno,
                        categoria):
    if not (isinstance(titulo, str) and isinstance(duracion, int)
            and isinstance(fecha_estreno, str) and isinstance(categoria, str)):
      return False

    try:
      self.conexion.cursor.execute(
          "INSERT INTO PELICULA (titulo, director,duracion, fecha_estreno,categoria) VALUES (?,?,?,?,?)",
          (titulo, director, duracion, fecha_estreno, categoria))

      self.conexion.conexion.commit()
      return True
    except sqlite3.Error as e:
      print(f"Error al ingresar la película: {e}")
      return False

  def filtrar_peliculas_por_categoria(self, categoria):
    try:
      self.conexion.cursor.execute(
          "SELECT * FROM PELICULA WHERE categoria = ?", (categoria, ))
      peliculas = self.conexion.cursor.fetchall()
      return peliculas
    except sqlite3.Error as e:
      print(f"Error al filtrar películas por categoría: {e}")
      return []

  def modificar_pelicula(self, id, titulo, director, duracion, fecha_estreno,
                         categoria):
    if not (isinstance(titulo, str) and isinstance(director, str)
            and isinstance(duracion, int) and isinstance(fecha_estreno, str)
            and isinstance(categoria, str)):
      return False
    try:
      self.conexion.cursor.execute(
          "UPDATE PELICULA SET titulo=?, director=?, duracion=?, fecha_estreno=?, categoria=? WHERE id = ?",
          (titulo, director, duracion, fecha_estreno, categoria, id))
      self.conexion.conexion.commit()
      return True
    except sqlite3.Error as e:
      print(f"Error al modificar la película: {e}")
      return False

  def eliminar_pelicula(self, id):
    if not isinstance(id, int):
      return False

    try:
      self.conexion.cursor.execute("DELETE FROM PELICULA WHERE id = ?", (id, ))
      self.conexion.conexion.commit()
      return True
    except sqlite3.Error as e:
      print(f"Error al eliminar la película: {e}")
      return False

  def menu_pelicula(self):
    opcion_pelicula = 0

    while opcion_pelicula != "6":
      opcion_pelicula = input(
          "Menú Película\n1- Ingresar Película\n2- Mostrar Película\n3- Modificar Película\n4- Eliminar Película\n5- Filtrar por categoría\n6- Volver al Menú Principal: "
      )

      if opcion_pelicula == "1":
        nombre = input("Ingrese nombre de la Película: ")
        descripcion = input("Ingrese la descripción de la Película: ")
        idioma = input("Ingrese el idioma de la Película: ")
        duracion = int(input("Ingrese la duración de la Película: "))
        fecha_estreno = input("Ingrese la fecha de estreno de la Película: ")
        precio = float(input("Ingrese precio de la Película: "))
        categoria = input("Ingrese la categoría: ")
        if self.ingresar_pelicula(nombre, descripcion, idioma, duracion,
                                  fecha_estreno, precio, categoria):
          print("Pelicula ingresada con éxito.")
        else:
          print("Error al ingresar la película.")
      elif opcion_pelicula == "2":
        peliculas = self.mostrar_peliculas()
        if peliculas:
          for pelicula in peliculas:
            print(
                f"Nombre: {pelicula[1]}, Descripción: {pelicula[2]}, Idioma: {pelicula[3]}, Duración: {pelicula[4]}, Fecha de Estreno: {pelicula[5]}, Precio: {pelicula[6]}, Categoria: {pelicula[7]}, ID: {pelicula[0]}"
            )
        else:
          print("No hay películas registradas.")
      elif opcion_pelicula == "3":
        id_pelicula = input("Ingrese ID de la película a modificar: ")
        nombre = input("Ingrese nuevo nombre: ")
        descripcion = input("Ingrese nueva descripción: ")
        idioma = input("Ingrese nuevo idioma: ")
        duracion = int(input("Ingrese nueva duración: "))
        fecha_estreno = input("Ingrese nueva fecha de estreno: ")
        categoria = input("Ingrese la categoría: ")
        precio = float(input("Ingrese nuevo precio: "))
        if self.modificar_pelicula(id_pelicula, nombre, descripcion, idioma,
                                   duracion, fecha_estreno, precio, categoria):
          print("Película modificada con éxito.")
        else:
          print("Error al modificar la película.")
      elif opcion_pelicula == "4":
        id_pelicula = input("Ingrese ID de la película a eliminar: ")
        if self.eliminar_pelicula(id_pelicula):
          print("Película eliminada con éxito.")
        else:
          print("Error al eliminar la película.")
      elif opcion_pelicula == "5":
        categoria_filtrada = input("Ingrese la categoría a filtrar: ")
        peliculas_filtradas = self.filtrar_peliculas_por_categoria(
            categoria_filtrada)
        if peliculas_filtradas:
          print("Películas en la categoría seleccionada:")
          for pelicula in peliculas_filtradas:
            print(
                f"Nombre: {pelicula[1]}, Descripción: {pelicula[2]}, Idioma: {pelicula[3]}, Duración: {pelicula[4]}, Fecha de Estreno: {pelicula[5]}, Precio: {pelicula[6]}, ID: {pelicula[0]}"
            )
        else:
          print("No se encontraron películas en la categoría especificada.")
      elif opcion_pelicula == "6":
        print("Volviendo al Menú Principal.")
      else:
        print("Opción no válida. Inténtalo de nuevo.")
