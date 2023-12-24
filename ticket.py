import sqlite3


class Ticket:

    def __init__(self, conexion):
        self.conexion = conexion

    def crear_tabla_ticket(self):
        try:
            self.conexion.cursor.execute('''
                CREATE TABLE IF NOT EXISTS TICKET(
                    id INTEGER PRIMARY KEY,
                    id_funcion INTEGER,
                    monto_total REAL,
                    cantidad_entradas INTEGER,
                    fecha TEXT,
                    FOREIGN KEY (id_funcion) REFERENCES FUNCION(id)
                )
            ''')
            self.conexion.conexion.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error al crear la tabla de Tickets: {e}")
            return False

    def ingresar_ticket(self, id_funcion, fecha):
        if not isinstance(id_funcion, int):
            return False

        try:
            self.conexion.cursor.execute(
                "INSERT INTO TICKET (id_funcion, fecha) VALUES (?, ?)",
                (id_funcion, fecha))
            self.conexion.conexion.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error al ingresar el ticket: {e}")
            return False

    def mostrar_tickets(self):
        try:
            self.conexion.cursor.execute("SELECT * FROM TICKET")
            tickets = self.conexion.cursor.fetchall()
            return tickets
        except sqlite3.Error as e:
            print(f"Error al mostrar tickets: {e}")
            return []

    def eliminar_ticket(self, id):
        if not isinstance(id, int):
            return False

        try:
            self.conexion.cursor.execute("DELETE FROM TICKET WHERE id=?", (id, ))
            self.conexion.conexion.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error al eliminar el ticket: {e}")
            return False

    def menu_ticket(self):
        opcion_ticket = 0

        while opcion_ticket != "3":
            opcion_ticket = input(
                "Menú Tickets\n1- Ingresar Ticket\n2- Mostrar Tickets\n3- Volver al Menú Principal\n"
            )

            if opcion_ticket == "1":
                id_funcion = int(input("Ingrese ID de la función: "))
                fecha = input("Ingrese la fecha: ")
                if self.ingresar_ticket(id_funcion, fecha):
                    print("Ticket ingresado con éxito.")
                else:
                    print("Error al ingresar el ticket.")
            elif opcion_ticket == "2":
                tickets = self.mostrar_tickets()
                if tickets:
                    for ticket in tickets:
                        print(f"ID: {ticket[0]}, Función: {ticket[1]}, Fecha: {ticket[2]}")
                else:
                    print("No hay tickets registrados.")
            elif opcion_ticket == "3":
                print("Volviendo al Menú Principal.")
            else:
                print("Opción no válida. Inténtalo de nuevo.")

