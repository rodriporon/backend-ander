import csv
import re
class Registro():
    def __init__(self,nombre,apellido,usuario,contraseña, confirmacion): 
        self.nombre = nombre 
        self.apellido = apellido 
        self.usuario = usuario 
        self.contraseña = contraseña 
        self.confirmacion = confirmacion
    
    def verificarContraseñas(self):
        if self.contraseña == self.confirmacion:
            return True
        else:
            return False
    
    def verificarRepetidos(self):
        with open ('Registro.csv','r') as csv_file:
            csv_reader = csv.reader(csv_file)
            validacion = False
            for columna in csv_reader:
                if columna[2]==str(self.usuario):
                    validacion = False
                else:
                    validacion = True
            csv_file.close()
        return validacion 
    
    def verificarAlfanumerico(self):
        validacion = True 
        letras = []
        for letra in str(self.usuario):
            letras.append(letra)    
        if self.conocerDigito(letras[0])==True or letras[0]==' ':
            validacion = False
        if validacion == True and self.conocerAlfanumerico(str(self.usuario))==True: 
            validacion = True
        else: 
            validacion = False
        return validacion

    def conocerDigito(self,letra):
        numeros = '^[0-9]+$'
        return bool(re.search(numeros,letra))
    
    def conocerAlfanumerico(self,palabra):
        alfa = '^[a-zA-Z0-9ñÑ]+$'
        return bool(re.search(alfa,palabra))
     
                
    def agregaracsv(self):
        registrocsv = open('Registro.csv','a')
        registrocsv.write('\n')
        registrocsv.write(str(self.nombre)+','+str(self.apellido)+','+str(self.usuario)+','+str(self.contraseña)+','+str(self.confirmacion))
        registrocsv.close()
