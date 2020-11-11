import csv 
import re
class login():
    def __init__(self,usuario,contraseña):
        self.usuario = usuario 
        self.contraseña = contraseña
    
    def verificarDatos(self):
        with open ('Registro.csv','r') as csv_file:
            csv_reader = csv.reader(csv_file)
            validacion=False
            for columnas in csv_reader:
                if columnas[2]==str(self.usuario) and columnas[3]==str(self.contraseña):
                    if str(self.usuario)=='admin' and str(self.contraseña)=='admin':
                        validacion ='admin'
                    else:
                        validacion =True
            return validacion
                   
               



