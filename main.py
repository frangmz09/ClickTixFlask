from flask import Flask, jsonify, redirect, render_template, request, session, url_for
'''
import sys
sys.path.append('/modelo')
'''
from bd import Conexion
from dimension import Dimension
from empleado import Empleado
from funcion import Funcion
from pelicula import Pelicula
from sala import Sala
from sucursal import Sucursal
from turno import Turno

app = Flask(__name__)
app.secret_key = 'clicktixSC'
nombre_bdd = 'ClickTix.db'
conexion = Conexion(nombre_bdd)

dimension = Dimension(conexion)
empleado = Empleado(conexion)
funcion = Funcion(conexion)

pelicula = Pelicula(conexion)
sucursal = Sucursal(conexion)
turno = Turno(conexion)
sala = Sala(conexion)

dimension.crear_tabla_dimension()
empleado.crear_tabla_empleado()
funcion.crear_tabla_funcion()
pelicula.crear_tabla_pelicula()
sucursal.crear_tabla_sucursal()
turno.crear_tabla_turno()
sala.crear_tabla_sala()

conexion.CerrarBD()

## LOGIN


@app.route('/', methods=['GET', 'POST'])
def handle_login():
  if 'nombreEmpleado' in session:
    return redirect(url_for('dashboard'))
  if request.method == 'POST':

    username = request.form.get('username')
    password = request.form.get('password')

    nombre_bdd = 'ClickTix.db'
    conexion = Conexion(nombre_bdd)
    empleado = Empleado(conexion)

    resultado = empleado.verificar_credenciales(username, password)
    print("RESULTADO DE INICIO DE SESION: ", resultado)
    conexion.CerrarBD()

    if resultado:
      nombre_bdd = 'ClickTix.db'
      conexion = Conexion(nombre_bdd)
      empleado = Empleado(conexion)
      session['nombreEmpleado'] = empleado.obtener_nombre_por_usuario(username)
      session['is_admin'] = empleado.traerIsAdminEmpleado(username, password)
      session['id_sucursal'] = empleado.obtener_id_sucursal_por_username(
          username)

      print("SESSION DESPUÉS DEL INICIO DE SESIÓN: ", session)
      return redirect(url_for('dashboard'))

  return render_template('login.html')


## DIRECCION DE LOGOUT


@app.route('/logout')
def logout():
  session.clear()
  return redirect(url_for('handle_login'))


## DASHBOARD


@app.route('/dashboard')
def dashboard():
  if 'nombreEmpleado' not in session:
    return redirect(url_for('handle_login'))
  return render_template('index.html')


##GESTION DE PELICULAS


@app.route('/peliculas')
def peliculas():

  if 'nombreEmpleado' not in session:
    return redirect(url_for('handle_login'))
  if 'is_admin' not in session or session['is_admin'] != 1:
    return redirect(url_for('dashboard'))
  nombre_bdd = 'ClickTix.db'
  conexion = Conexion(nombre_bdd)
  peliculaM = Pelicula(conexion)
  peliculas = peliculaM.mostrar_peliculas()
  print(peliculas)
  conexion.CerrarBD()
  return render_template('tb-peliculas.html', peliculas=peliculas)


@app.route('/agregar_pelicula', methods=['GET', 'POST'])
def agregar_pelicula():
  if 'nombreEmpleado' not in session:
    return redirect(url_for('handle_login'))
  if 'is_admin' not in session or session['is_admin'] != 1:
    return redirect(url_for('dashboard'))
  if request.method == 'POST':
    nombre_bdd = 'ClickTix.db'
    conexion = Conexion(nombre_bdd)

    titulo = request.form['titulo']
    director = request.form['director']
    duracion = int(request.form['duracion'])
    fecha_estreno = request.form['fecha']
    categoria = request.form['categoriaPelicula']
    pelicula = Pelicula(conexion)
    pelicula.ingresar_pelicula(titulo, director, duracion, fecha_estreno,
                               categoria)
    conexion.CerrarBD()
    return redirect(url_for('peliculas'))

  return render_template('agregar-pelicula.html')


@app.route('/modificar_pelicula/<int:id_pelicula>', methods=['GET', 'POST'])
def modificar_pelicula(id_pelicula):
  if 'nombreEmpleado' not in session:
    return redirect(url_for('handle_login'))
  if 'is_admin' not in session or session['is_admin'] != 1:
    return redirect(url_for('dashboard'))
  nombre_bdd = 'ClickTix.db'
  conexion = Conexion(nombre_bdd)
  pelicula = Pelicula(conexion)
  pelicula_seleccionada = pelicula.mostrarPeliculaPorId(id_pelicula)

  if request.method == 'POST':
    titulo = request.form['titulo']
    director = request.form['director']
    duracion = int(request.form['duracion'])
    fecha_estreno = request.form['fecha']
    categoria = request.form['categoriaPelicula']

    if pelicula.modificar_pelicula(id_pelicula, titulo, director, duracion,
                                   fecha_estreno, categoria):
      conexion.CerrarBD()
      return redirect(url_for('peliculas'))

  conexion.CerrarBD()
  return render_template('editar-pelicula.html',
                         pelicula=pelicula_seleccionada)


@app.route('/eliminar_pelicula/<int:id_pelicula>')
def eliminar_pelicula(id_pelicula):
  if 'nombreEmpleado' not in session:
    return redirect(url_for('handle_login'))
  if 'is_admin' not in session or session['is_admin'] != 1:
    return redirect(url_for('dashboard'))
  nombre_bdd = 'ClickTix.db'
  conexion = Conexion(nombre_bdd)
  peliculaM = Pelicula(conexion)
  peliculaM.eliminar_pelicula(id_pelicula)
  conexion.CerrarBD()
  return redirect(url_for('peliculas'))


# GESTION DE FUNCIONES


@app.route('/funciones')
def funciones():
  if 'nombreEmpleado' not in session:
    return redirect(url_for('handle_login'))
  if 'is_admin' not in session or session['is_admin'] != 1:
    return redirect(url_for('dashboard'))
  nombre_bdd = 'ClickTix.db'
  conexion = Conexion(nombre_bdd)
  funcionM = Funcion(conexion)
  funciones = funcionM.mostrar_funcionesTEXT()
  print("las funciones son:", funciones)
  conexion.CerrarBD()
  return render_template('tb-funciones.html', funciones=funciones)


@app.route('/agregar_funcion', methods=['GET', 'POST'])
def agregar_funcion():
  if 'nombreEmpleado' not in session:
    return redirect(url_for('handle_login'))
  if 'is_admin' not in session or session['is_admin'] != 1:
    return redirect(url_for('dashboard'))
  if request.method == 'POST':
    nombre_bdd = 'ClickTix.db'
    conexion = Conexion(nombre_bdd)

    if 'fecha' in request.form and 'dimension' in request.form and 'pelicula' in request.form and 'sucursal' in request.form and 'sala' in request.form and 'idioma' in request.form and 'turno' in request.form:
      fecha = request.form['fecha']
      id_dimension = request.form['dimension']
      id_pelicula = int(request.form['pelicula'])
      id_sucursal = int(request.form['sucursal'])
      id_sala = int(request.form['sala'])
      idioma_funcion = request.form['idioma']
      turno_id = int(request.form['turno'])
    else:
      print("Campos requeridos no presentes en la solicitud")
      return redirect(url_for('agregar_funcion'))

    funcion = Funcion(conexion)
    if funcion.ingresar_funcion(fecha, id_dimension, id_pelicula, id_sucursal,
                                id_sala, idioma_funcion, turno_id):
      print("Función ingresada correctamente")
    else:
      print("Error al ingresar la función")

    conexion.CerrarBD()
    return redirect(url_for('funciones'))

  nombre_bdd = 'ClickTix.db'
  conexion = Conexion(nombre_bdd)
  sucursales = Sucursal(conexion).mostrar_sucursales()
  peliculas = Pelicula(conexion).mostrar_peliculas()
  turnos = Turno(conexion).mostrar_turnos()
  salas = Sala(conexion).mostrar_salas()

  conexion.CerrarBD()

  return render_template('agregar-funcion.html',
                         sucursales=sucursales,
                         peliculas=peliculas,
                         salas=salas,
                         turnos=turnos)


@app.route('/obtener_salas/<sucursal_id>')
def obtener_salas(sucursal_id):
  nombre_bdd = 'ClickTix.db'
  conexion = Conexion(nombre_bdd)
  salas = Sala(conexion).mostrar_salas_sucursal(sucursal_id)

  return jsonify(salas)


@app.route('/modificar_funcion<int:id_funcion>', methods=['GET', 'POST'])
def modificar_funcion(id_funcion):
  if 'nombreEmpleado' not in session:
    return redirect(url_for('handle_login'))
  if 'is_admin' not in session or session['is_admin'] != 1:
    return redirect(url_for('dashboard'))
  nombre_bdd = 'ClickTix.db'
  conexion = Conexion(nombre_bdd)

  funcion = Funcion(conexion)
  funcionSeleccionada = funcion.mostrarFuncionPorId(id_funcion)

  if request.method == 'POST':
    fecha = request.form['fecha']
    id_dimension = request.form['dimension']
    id_pelicula = int(request.form['pelicula'])
    id_sucursal = int(request.form['sucursal'])
    id_sala = int(request.form['sala'])
    idioma_funcion = request.form['idioma']
    id_turno = int(request.form['turno'])
    if funcion.modificar_funcion(fecha, id_dimension, id_pelicula, id_sucursal,
                                 id_sala, idioma_funcion, id_turno,
                                 id_funcion):

      conexion.CerrarBD()
      return redirect(url_for('funciones'))

  nombre_bdd = 'ClickTix.db'
  conexion = Conexion(nombre_bdd)
  sucursales = Sucursal(conexion).mostrar_sucursales()
  peliculas = Pelicula(conexion).mostrar_peliculas()
  turnos = Turno(conexion).mostrar_turnos()
  salas = Sala(conexion).mostrar_salas()

  conexion.CerrarBD()
  return render_template('editar-funcion.html',
                         funcion=funcionSeleccionada,
                         peliculas=peliculas,
                         salas=salas,
                         sucursales=sucursales,
                         turnos=turnos)


@app.route('/eliminar_funcion/<int:id_funcion>')
def eliminar_funcion(id_funcion):
  if 'nombreEmpleado' not in session:
    return redirect(url_for('handle_login'))
  if 'is_admin' not in session or session['is_admin'] != 1:
    return redirect(url_for('dashboard'))
  nombre_bdd = 'ClickTix.db'
  conexion = Conexion(nombre_bdd)
  FuncionM = Funcion(conexion)
  FuncionM.eliminar_funcion(id_funcion)
  conexion.CerrarBD()
  return redirect(url_for('funciones'))


# GESTION DE SALAS
@app.route('/salas')
def salas():
  if 'nombreEmpleado' not in session:
    return redirect(url_for('handle_login'))
  if 'is_admin' not in session or session['is_admin'] != 1:
    return redirect(url_for('dashboard'))
  nombre_bdd = 'ClickTix.db'
  conexion = Conexion(nombre_bdd)
  salasM = Sala(conexion)
  salas = salasM.mostrar_salas()
  print(salas)
  conexion.CerrarBD()
  return render_template('tb-salas.html', salas=salas)


@app.route('/agregar_sala', methods=['GET', 'POST'])
def agregar_sala():
  if 'nombreEmpleado' not in session:
    return redirect(url_for('handle_login'))
  if 'is_admin' not in session or session['is_admin'] != 1:
    return redirect(url_for('dashboard'))
  if request.method == 'POST':
    nombre_bdd = 'ClickTix.db'
    conexion = Conexion(nombre_bdd)

    capacidad = int(request.form['capacidad'])
    sucursal = int(request.form['sucursal'])

    sala = Sala(conexion)
    max_numero_sala = sala.obtener_max_numero_sala_por_sucursal(sucursal)

    if isinstance(max_numero_sala, int):
      numero = max_numero_sala + 1
      sala.ingresar_sala(numero, capacidad, int(sucursal))
    else:
      print("No se pudo obtener un número de sala válido.")
    conexion.CerrarBD()
    return redirect(url_for('salas'))
  nombre_bdd = 'ClickTix.db'
  conexion = Conexion(nombre_bdd)
  sucursales = Sucursal(conexion).mostrar_sucursales()
  conexion.CerrarBD()

  return render_template('agregar-sala.html', sucursales=sucursales)


@app.route('/modificar_sala/<int:id_sala>', methods=['GET', 'POST'])
def modificar_sala(id_sala):
  if 'nombreEmpleado' not in session:
    return redirect(url_for('handle_login'))
  if 'is_admin' not in session or session['is_admin'] != 1:
    return redirect(url_for('dashboard'))
  nombre_bdd = 'ClickTix.db'
  conexion = Conexion(nombre_bdd)
  sala = Sala(conexion)
  salaSeleccionada = sala.traer_sala_por_id(id_sala)

  if request.method == 'POST':
    capacidad = int(request.form['capacidad'])

    if sala.modificar_sala(id_sala, capacidad):
      conexion.CerrarBD()
      return redirect(url_for('salas'))

  conexion.CerrarBD()
  return render_template('editar-sala.html', sala=salaSeleccionada)


@app.route('/eliminar_sala/<int:id_sala>')
def eliminar_sala(id_sala):
  if 'nombreEmpleado' not in session:
    return redirect(url_for('handle_login'))
  if 'is_admin' not in session or session['is_admin'] != 1:
    return redirect(url_for('dashboard'))
  nombre_bdd = 'ClickTix.db'
  conexion = Conexion(nombre_bdd)
  salasM = Sala(conexion)
  salasM.eliminarSala(id_sala)
  conexion.CerrarBD()
  return redirect(url_for('salas'))


# GESTION DE SUCURSALES
@app.route('/sucursales')
def sucursales():
  if 'nombreEmpleado' not in session:
    return redirect(url_for('handle_login'))
  if 'is_admin' not in session or session['is_admin'] != 1:
    return redirect(url_for('dashboard'))
  nombre_bdd = 'ClickTix.db'
  conexion = Conexion(nombre_bdd)
  sucursales = Sucursal(conexion).mostrar_sucursales()
  conexion.CerrarBD()

  return render_template('tb-sucursales.html', sucursales=sucursales)


@app.route('/agregar_sucursal', methods=['GET', 'POST'])
def agregar_sucursal():
  if 'nombreEmpleado' not in session:
    return redirect(url_for('handle_login'))
  if 'is_admin' not in session or session['is_admin'] != 1:
    return redirect(url_for('dashboard'))
  if request.method == 'POST':
    nombre_bdd = 'ClickTix.db'
    conexion = Conexion(nombre_bdd)

    nombre = request.form['nombre']
    cuit = int(request.form['cuit'])
    direccion = request.form['direccion']

    sucursal = Sucursal(conexion)
    sucursal.ingresar_sucursal(nombre, cuit, direccion)
    conexion.CerrarBD()
    return redirect(url_for('sucursales'))

  return render_template('agregar-sucursal.html')


@app.route('/modificar_sucursal/<int:id_sucursal>', methods=['GET', 'POST'])
def modificar_sucursal(id_sucursal):
  if 'nombreEmpleado' not in session:
    return redirect(url_for('handle_login'))
  if 'is_admin' not in session or session['is_admin'] != 1:
    return redirect(url_for('dashboard'))
  nombre_bdd = 'ClickTix.db'
  conexion = Conexion(nombre_bdd)
  sucursal = Sucursal(conexion)
  sucursal_seleccionada = sucursal.mostrarSucursalPorId(id_sucursal)

  if request.method == 'POST':
    nombre = request.form['nombre']
    cuit = int(request.form['cuit'])
    direccion = request.form['direccion']

    if sucursal.editar_sucursal(id_sucursal, nombre, direccion, cuit):
      conexion.CerrarBD()
      return redirect(url_for('sucursales'))

  conexion.CerrarBD()
  return render_template('editar-sucursal.html',
                         sucursal=sucursal_seleccionada)


@app.route('/eliminar_sucursal/<int:id_sucursal>')
def eliminar_sucursal(id_sucursal):
  if 'nombreEmpleado' not in session:
    return redirect(url_for('handle_login'))
  if 'is_admin' not in session or session['is_admin'] != 1:
    return redirect(url_for('dashboard'))
  nombre_bdd = 'ClickTix.db'
  conexion = Conexion(nombre_bdd)
  sucursal = Sucursal(conexion)
  sucursal.eliminar_sucursal(id_sucursal)
  conexion.CerrarBD()
  return redirect(url_for('sucursales'))


## GESTION DE EMPLEADOS
@app.route('/empleados')
def empleados():
  if 'nombreEmpleado' not in session:
    return redirect(url_for('handle_login'))
  if 'is_admin' not in session or session['is_admin'] != 1:
    return redirect(url_for('dashboard'))
  nombre_bdd = 'ClickTix.db'
  conexion = Conexion(nombre_bdd)
  empleadosM = Empleado(conexion)
  empleados = empleadosM.mostrar_empleados()
  conexion.CerrarBD()
  return render_template('tb-empleados.html', empleados=empleados)


@app.route('/agregar_empleado', methods=['GET', 'POST'])
def agregar_empleado():
  if 'nombreEmpleado' not in session:
    return redirect(url_for('handle_login'))
  if 'is_admin' not in session or session['is_admin'] != 1:
    return redirect(url_for('dashboard'))
  if request.method == 'POST':
    nombre_bdd = 'ClickTix.db'
    conexion = Conexion(nombre_bdd)
    empleado = Empleado(conexion)

    nombre = request.form['nombre']
    apellido = request.form['apellido']
    dni = request.form['dni']
    admin = request.form['admin']
    sucursal = request.form['sucursal']
    user = request.form['user']
    password = request.form['password']

    empleado.ingresar_empleado(nombre, apellido, dni, sucursal, admin, user,
                               password)
    conexion.CerrarBD()
    return redirect(url_for('empleados'))
  nombre_bdd = 'ClickTix.db'
  conexion = Conexion(nombre_bdd)
  sucursales = Sucursal(conexion).mostrar_sucursales()
  conexion.CerrarBD()
  return render_template('agregar-empleado.html', sucursales=sucursales)


@app.route('/modificar_empleado/<int:id_empleado>', methods=['GET', 'POST'])
def modificar_empleado(id_empleado):
  if 'nombreEmpleado' not in session:
    return redirect(url_for('handle_login'))
  if 'is_admin' not in session or session['is_admin'] != 1:
    return redirect(url_for('dashboard'))

  nombre_bdd = 'ClickTix.db'
  conexion = Conexion(nombre_bdd)
  empleado = Empleado(conexion)
  empleado_seleccionado = empleado.traer_empleado_por_id(id_empleado)

  if request.method == 'POST':
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    dni = request.form['dni']
    admin = request.form['admin']
    sucursal = request.form['sucursal']
    user = request.form['user']
    password = request.form['password']

    if empleado.modificar_empleado(nombre, apellido, dni, sucursal, admin,
                                   user, password, id_empleado):
      conexion.CerrarBD()
      return redirect(url_for('empleados'))

  sucursales = Sucursal(conexion).mostrar_sucursales()
  conexion.CerrarBD()
  return render_template('editar-empleado.html',
                         empleado=empleado_seleccionado,
                         sucursales=sucursales)


@app.route('/eliminar_empleado/<int:id_empleado>')
def eliminar_empleado(id_empleado):
  if 'nombreEmpleado' not in session:
    return redirect(url_for('handle_login'))
  if 'is_admin' not in session or session['is_admin'] != 1:
    return redirect(url_for('dashboard'))
  nombre_bdd = 'ClickTix.db'
  conexion = Conexion(nombre_bdd)
  empleado = Empleado(conexion)
  empleado.eliminar_empleado(id_empleado)
  conexion.CerrarBD()
  return redirect(url_for('empleados'))


################ PASARELA COMPRAS ##############################
################ PASARELA COMPRAS ##############################
################ PASARELA COMPRAS ##############################


@app.route('/elegir_funcion')
def elegir_funcion():
  if 'nombreEmpleado' not in session:
    return redirect(url_for('handle_login'))
  nombre_bdd = 'ClickTix.db'
  conexion = Conexion(nombre_bdd)
  funciones = Funcion(conexion).mostrar_funcionesTEXT_por_sucursal(
      session['id_sucursal'])
  conexion.CerrarBD()

  return render_template('elegir-funcion.html', funciones=funciones)


@app.route('/ticket', methods=['GET', 'POST'])
def ticket():
  if 'nombreEmpleado' not in session:
    return redirect(url_for('handle_login'))
  if request.method == 'POST':
    print("Formulario Completo:", request.form)

    id_funcion = request.form.get('idFuncion')
    monto_total = float(request.form.get('montoTotal'))
    cantidad_entradas = int(request.form.get('cantidadEntradas'))
    nombre_bdd = 'ClickTix.db'
    conexion = Conexion(nombre_bdd)
    funcion = Funcion(conexion)
    funcion.restarDisponibilidad(id_funcion, cantidad_entradas)
    funcionEncontrada = funcion.mostrar_funcion_por_idTEXT(id_funcion)
    fecha=0
    titulo=0
    idioma=0
    dimension=0
    horario=0
    sala=0
    nombreSucursal=0
    sucursalCuit=0
    
    if funcionEncontrada:
      fecha = funcionEncontrada[4]
      titulo = funcionEncontrada[1]
      idioma = funcionEncontrada[2]
      dimension = funcionEncontrada[3]
      horario = funcionEncontrada[5]
      sala = funcionEncontrada[6]
      nombreSucursal = funcionEncontrada[8]
      sucursalCuit = 0
      sucursales = Sucursal(conexion)
      sucursalCuit = sucursales.traer_cuit_por_nombre_sucursal(
          funcionEncontrada[8])

    conexion.CerrarBD()
    return render_template('ticket.html',
                           id_funcion=id_funcion,
                           monto_total=monto_total,
                           cantidad_entradas=cantidad_entradas,
                           fecha=fecha,
                           titulo=titulo,
                           idioma=idioma,
                           dimension=dimension,
                           horario=horario,
                           sala=sala,
                           nombreSucursal=nombreSucursal,
                           sucursalCuit=sucursalCuit)

  return render_template('ticket.html')


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)
