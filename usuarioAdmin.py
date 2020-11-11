import csv
import re
from os import remove
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import pdfkit

class usuarioAdmin():
    def __init__(self,usuario,catalogocsv,seleccionadaEditar):
        self.usuario = usuario
        self.seleccionadaEditar=seleccionadaEditar
        self.catalogoPeliculas = []
        self.peliculaEditarjson = []
        self.catalogocsv = catalogocsv
    
    def extraerPeliculas(self):
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
    
    def buscarSeleccionadaEditar(self):
        for columna in self.catalogoPeliculas:
            if self.seleccionadaEditar == columna['Titulo']:
                self.peliculaEditarjson.append({
                'Titulo': columna['Titulo'],
                'URL_Imagen': columna['URL_Imagen'],
                'Puntuacion': columna['Puntuacion'],
                'Duracion': columna['Duracion'],
                'Sinopsis': columna['Sinopsis'],
                'Estado': columna['Estado']
                })
        return self.peliculaEditarjson

    def eliminarPeliculaEditar(self):
        recuperar = self.catalogoPeliculas.copy()
        self.catalogoPeliculas.clear()
        for dato in recuperar:
            for i in self.peliculaEditarjson:
                if i['Titulo'] != dato['Titulo'] and i['URL_Imagen']!=dato['URL_Imagen'] and i['Puntuacion']!=dato['Puntuacion'] and i['Duracion']!=dato['Duracion'] and i['Sinopsis']!=dato['Sinopsis']:
                    self.catalogoPeliculas.append({
                    'Titulo': dato['Titulo'],
                    'URL_Imagen': dato['URL_Imagen'],
                    'Puntuacion': dato['Puntuacion'],
                    'Duracion': dato['Duracion'],
                    'Sinopsis': dato['Sinopsis'],
                    'Estado': dato['Estado']
                }) 
        return('si')
    
    def datosModificados(self,Titulo,URL_Imagen,Puntuacion,Duracion,Sinopsis,Estado):
        self.catalogoPeliculas.append({
            'Titulo': Titulo,
            'URL_Imagen': URL_Imagen,
            'Puntuacion': Puntuacion,
            'Duracion': Duracion,
            'Sinopsis': Sinopsis,
            'Estado': Estado
        })
        remove(self.catalogocsv)
        crear = open(self.catalogocsv,'x')
        crear.close
        escribir = open(self.catalogocsv,'a')
        for columnas in self.catalogoPeliculas:
            linea = columnas['Titulo']+','+columnas['URL_Imagen']+','+columnas['Puntuacion']+','+columnas['Duracion']+','+columnas['Sinopsis']+','+'\n'
            escribir.write(linea)
            escribir.flush()
        escribir.close()
        return('si')
    
    

           





     
