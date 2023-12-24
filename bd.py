import sqlite3


class Conexion:

  def __init__(self, nombreBD):
    self.conexion = sqlite3.connect(nombreBD)
    self.cursor = self.conexion.cursor()

  def CerrarBD(self):
    self.cursor.close()
    self.conexion.close()
    
