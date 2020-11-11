import csv
import re
from os import remove
from os import path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import pdfkit
class usuarioCliente():
    def __init__(self,usuario,peliculaSeleccionada,catalogocsv):
        self.usuario = usuario
        self.peliculaSeleccionada = peliculaSeleccionada
        self.catalogoPeliculas = []
        self.peliculaSeleccionadajson = []
        self.catalogocsv = catalogocsv
        self.comentarios = []

    def extrarPeliculas(self):
        with open (self.catalogocsv,'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for columna in csv_reader:
                self.catalogoPeliculas.append({
                    'Titulo': columna[0],
                    'URL_Imagen': columna[1],
                    'Puntuacion': columna[2],
                    'Duracion': columna[3],
                    'Sinopsis': columna[4],
                    'Estado': 'Disponible'
                })
        return self.catalogoPeliculas
     
    def buscarSeleccionada(self):
        with open (self.catalogocsv,'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for columna in csv_reader:
                if self.peliculaSeleccionada == columna[0]:
                    self.peliculaSeleccionadajson.append({
                    'Titulo': columna[0],
                    'URL_Imagen': columna[1],
                    'Puntuacion': columna[2],
                    'Duracion': columna[3],
                    'Sinopsis': columna[4]
                     })
        return self.peliculaSeleccionadajson

    def extraercomentarios(self):
        self.comentarios.clear()
        nombre= self.peliculaSeleccionada.split('.')
        if path.exists(nombre[0]+'comentarios.csv')==True:
            with open (nombre[0]+'comentarios.csv','r') as csv_file:
                csv_reader = csv.reader(csv_file)
                for columna in csv_reader:
                    self.comentarios.append({
                    'comentarios': columna[0]
                })
            return self.comentarios
        else:
            return 'no'

    



    def comentariosNuevos(self,comentarioNuevo):
        self.comentarios.clear()
        nombre = self.peliculaSeleccionada.split('.')
        if(path.exists(nombre[0]+'comentarios.csv')==True):
            with open (nombre[0]+'comentarios.csv','r') as csv_file:
                csv_reader = csv.reader(csv_file)
                for columna in csv_reader:
                    self.comentarios.append({
                    'comentarios': columna[0],
                    })
            csv_file.close()
            remove(nombre[0]+'comentarios.csv')
        self.comentarios.append({'comentarios':comentarioNuevo})
        nuevo = open(nombre[0]+'comentarios.csv','x')
        nuevo.close()
        escribir = open(nombre[0]+'comentarios.csv','a')
        for coment in self.comentarios:
            escribir.write(coment['comentarios']+'\n')
            escribir.flush()
        escribir.close()
        return 'si'

        
        
                

                
