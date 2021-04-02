import sqlite3 
import Funciones.Desencripta

class Empleado:
    def __init__(self):
        self.conexion_empleado = sqlite3.connect("EMPLEADO.db")

    def buscar(self, usuario, contrasenia):
        try:
            #Encripta contraseña pasada por parametro desde interfaz grafica
            self.pass_enc = Funciones.Desencripta.Desencripta_pass().ejecuta_encriptado(contrasenia)

            #Genera cursor y realiza consulta a tabla
            self.cursor_busca=self.conexion_empleado.cursor()
            self.cursor_busca.execute("SELECT TR_USUARIO, TR_CONTRASENIA FROM TRABAJADORES WHERE TR_USUARIO = '" + usuario + "'")
            
            #Asigna elresultado se la consulta a una variable
            self.resultado=self.cursor_busca.fetchone()

            #Evalua si usuario y contraseña retornada de la base de datos coincide con los datos ingresados
            if self.resultado == None:
                return False
            else:
                if str(self.pass_enc) == self.resultado[1].strip():
                    return True
                else:
                    return False
            self.cierra_conexion()
        except sqlite3.OperationalError:
            #servidor.quit()
            return "Error en conexion"             

    def cierra_conexion(self):
        self.conexion_empleado.close()
        

