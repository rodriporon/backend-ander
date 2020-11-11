from flask import Flask, request, jsonify, Markup,render_template,flash,redirect,url_for
from flask_cors import CORS, cross_origin
import json
from registro import Registro 
from login import login
from usuarioCliente import usuarioCliente
import os
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from usuarioAdmin import usuarioAdmin


main = Flask(__name__)
CORS(main)
#-----------------------------------------------------VARIABLES GLOBALES--------------------------------------------------------------
usuarioGlobal = 'usuarioGlobal'
peliculaSeleccionada = 'peliculaSeleccionada'
main.config['UPLOAD_FOLDER'] = "./"
catalogocsv = 'catalogoPeliculas.csv'
peliculaEditar = 'peliculaEditar'
#---------------------------------------SUBIR CSV A SERVIDOR PRIMERA TABLA--------------------------------------
@main.route("/subir", methods=['POST'])
def subir():
    if request.method =="POST":
        archivo = request.files['csv']
        nombreArchivo = secure_filename(archivo.filename)
        archivo.save(os.path.join(main.config['UPLOAD_FOLDER'],nombreArchivo))
        global catalogocsv
        catalogocsv = nombreArchivo
        #ACA DEBO DE COLOCAR EL ENLACE HTTP A ESTA PAGINA EN CONCRETO :3-------------------------------------------------------------
        return redirect('https://frontendipc2proyectoander.herokuapp.com/tablaPeliculasAdmin.html')

# ACA INICIA LO RELACIONADO A EL TEMA DEL REGISTRO DE USUARIOS :3 --------------------------------------------------------------------
registroUsuarios=[]
json_registroUsuarios=[]
@main.route('/AgregarUsuario',methods=['POST'])
def Agregarusuario():
     cuerpoUsuario = request.get_json()
     nombre = cuerpoUsuario['nombre']
     apellido = cuerpoUsuario['apellido']
     usuario = cuerpoUsuario['usuario']
     contraseña = cuerpoUsuario['contraseña']
     confirmacion = cuerpoUsuario['confirmacion']
     nuevoRegistro = Registro(nombre,apellido,usuario,contraseña,confirmacion)   
     if nuevoRegistro.verificarContraseñas()==True and nuevoRegistro.verificarRepetidos()==True and nuevoRegistro.verificarAlfanumerico()==True:
         global registroUsuarios
         global confirmacionRegistro
         confirmacionRegistro = True 
         registroUsuarios.append(nuevoRegistro)
         nuevoRegistro.agregaracsv()
         return jsonify({'mensaje':"¡Felicidades, su registro ha sido exitoso!"})
     else:
         confirmacionRegistro = False
         mens = "No fue posible procesar su registro, porfavor tome en cuenta lo siguiente: \n"\
         "-El nombre de usuario debe iniciar con una letra y no debe contener simbolos ni espacios\n-Asegurese de que la casilla de contraseña y confirmacion de contraseña no sean distintas\n-Si el error continua, intente con un nombre de usuario distinto pueda ser que el ingresado se encuentre en uso"
         return jsonify({'mensaje': mens})

#-----------------------------------------------------LO RELACIONADO AL LOGIN INICIA ACA----------------------------------------------------
@main.route('/Login', methods=['POST'])
def Login():
    cuerpoLogin = request.get_json()
    usuario = cuerpoLogin['usuario']
    contraseña = cuerpoLogin['contraseña']
    verificacion = login(usuario,contraseña)
    if verificacion.verificarDatos()==True:
        global usuarioGlobal
        usuarioGlobal = str(usuario) 
        return jsonify({'mensaje':'si'})
    if verificacion.verificarDatos()=='admin':
        usuarioGlobal = str(usuario)
        return jsonify({'mensaje': 'admin'})
    else:
        return jsonify({'mensaje':'Por favor revise los campos ingresados\n si en dado caso se encuentran correctos\nverifique si se encuentra registrado'})
#------------------------------------------------ALL RELACIONADO CON EL ADMIN---------------------------------------------------------
@main.route('/TablaPeliculas', methods=['GET'])
def TablaPeliculas():
    global usuarioGlobal
    global peliculaEditar
    global catalogocsv
    TablaPeliculas = usuarioAdmin(usuarioGlobal,catalogocsv,peliculaEditar)
    return jsonify(TablaPeliculas.extraerPeliculas())

@main.route('/obtenerNombreEditar',methods=['POST'])
def editMovie(): #:v open english no es, es puro duolingo
    pelicula = request.get_json()
    nombre = pelicula['nombre']
    global peliculaEditar
    peliculaEditar = str(nombre)
    return jsonify({'mensaje':'alright'})

@main.route('/EditarPelicula',methods=['GET'])
def enviarDetallesPeliculaEditar():
    global usuarioGlobal
    global peliculaEditar
    global catalogocsv
    detalles = usuarioAdmin(usuarioGlobal,catalogocsv,peliculaEditar)
    detalles.extraerPeliculas()
    return jsonify(detalles.buscarSeleccionadaEditar())

@main.route('/EliminarPelicula',methods=['POST'])
def eliminarPelicula():
    global usuarioGlobal
    global peliculaEditar
    global catalogocsv
    eliminar = usuarioAdmin(usuarioGlobal,catalogocsv,peliculaEditar)
    eliminar.extraerPeliculas()
    eliminar.buscarSeleccionadaEditar()
    eliminar.eliminarPeliculaEditar()
    datosmodificados = request.get_json()
    Titulonuevo = str(datosmodificados['Titulo'])
    URLnuevo = str(datosmodificados['URL_Imagen'])
    puntuacionNueva = str(datosmodificados['Puntuacion'])
    DuracionNueva = str(datosmodificados['Duracion'])
    SinopsisNueva = str(datosmodificados['Sinopsis'])
    EstadoNuevo = str(datosmodificados['Estado'])
    eliminar.datosModificados(Titulonuevo,URLnuevo,puntuacionNueva,DuracionNueva,SinopsisNueva,EstadoNuevo)
    return jsonify({'mensaje':'si'})

@main.route('/pdfPeliculas',methods=['GET'])
def crearPdf():
    global catalogocsv
    global peliculaEditar
    global usuarioGlobal
    crear = usuarioAdmin(usuarioGlobal,catalogocsv,peliculaEditar)
    return jsonify(crear.extraerPeliculas())
    





#----------------------------------------------PAGINA PRINCIPAL Y EL RESTO DEL USUARIO CLIENTE----------------------------------------------------------
#ESTE METODO LO QUE HARA ES QUE LLENARA EL CATALOGO DE PELICULAS CON LAS PELICULAS QUE EL USUARIO CONTENGA EN EL CSV
@main.route('/catalogoPeliculas', methods=['GET'])
def catalogoPeliculas():
    global usuarioGlobal
    global peliculaSeleccionada
    global catalogocsv
    catalogo = usuarioCliente(usuarioGlobal,peliculaSeleccionada,catalogocsv)
    return jsonify(catalogo.extrarPeliculas())

#ESTE METODO GUARDARA EN UNA VARIABLE GLOBAL DE LA API EL NOMBRE DE LA PELICULA SELCCIONADA LO CUAL SERVIRA PARA MOSTRAR LOS DETALLES 
#DE LA MISMA DENTRO DE LA PAGINA DE DETALLES :3 ME FUNCIONO A LA PRIMERA POR CIERTO 
@main.route('/obtenerNombreSeleccionada',methods=['POST'])
def SelectedMovie(): #:v open english no es, es puro duolingo
    pelicula = request.get_json()
    nombre = pelicula['nombre']
    global peliculaSeleccionada
    peliculaSeleccionada = str(nombre)
    return jsonify({'mensaje':'alright'})

@main.route('/detallesPelicula',methods=['GET'])
def enviarDetallesPelicula():
    global usuarioGlobal
    global peliculaSeleccionada
    global catalogocsv
    detalles = usuarioCliente(usuarioGlobal,peliculaSeleccionada,catalogocsv)
    return jsonify(detalles.buscarSeleccionada())
    
@main.route('/extraercomentarios',methods=['GET'])
def enviarcomentarios():
    global usuarioGlobal
    global peliculaSeleccionada
    global catalogocsv
    coment = usuarioCliente(usuarioGlobal,peliculaSeleccionada,catalogocsv)
    if(coment.extraercomentarios()!='no'):
        return jsonify(coment.extraercomentarios())
    else: 
        return jsonify({'comentarios':'sin comentarios'})

@main.route('/comentariosnuevos',methods=['POST'])
def guardarcomentarios():
    comentario = request.get_json()
    comentarioNuevo = comentario['comentario']
    global usuarioGlobal
    global peliculaSeleccionada
    global catalogocsv
    comentarios = usuarioCliente(usuarioGlobal,peliculaSeleccionada,catalogocsv)
    comentarios.comentariosNuevos(comentarioNuevo)
    return jsonify({'mensaje':'si'})


#-------------------------------------------------------MAIN-----------------------------------------------------------------------------

if __name__ == "__main__":
    main.run(threaded=True, host="0.0.0.0", port=5000, debug=True)