import Conexion.Conexion_db
import Funciones.Correo
import json
import csv
from csv import reader

class Archivo():
    def __init__(self):
        self.name=("Tratamiento archivos")

    def cargar_json(self):
        try:
            #Se define ruta del archivo json
            self.ruta = "archivo.json"
            #Arbre el archivo
            with open(self.ruta) as contenido:
                #carga el contenido del archivo en clasificacion
                self.clasificacion = json.load(contenido)
                return self.clasificacion
        except FileNotFoundError:
            return "existe"

    def cargar_csv(self):
        try:
        #Se define ruta del archivo
            self.ruta = "usuario_manager.csv"
            with open(self.ruta) as contenido:
                self.read = reader(contenido, delimiter=";")
                self.lista = list(self.read)
                return self.lista
        except FileNotFoundError:
            return "existe"


    def valida_json(self, archivo_json, archivo_csv, correo, contrasenia):
        self.registros_completos = 0
        self.total_registros = 0
        self.registros_faltantes = 0
    #Comienza ciclo para revision de datos en archivo JSON y que se realicen las actividades del programa según corresponda
        for self.clasifica in archivo_json:
            self.total_registros = self.total_registros + 1
            self.id_ = self.clasifica.get("id"," ")
            self.nombre = self.clasifica.get("nombre_base_datos"," ")
            self.descripcion = self.clasifica.get("descripcion"," ")
            self.usuario = self.clasifica.get("usuario"," ")
            self.clasificacion = self.clasifica.get("clasificacion"," ")

    ##Valida si el archivo viene completo, si faltan datos retorna error
            if self.id_ == " " or self.nombre == " " or self.descripcion == " " or self.descripcion == " " or self.usuario == " " or self.clasificacion == " " or str(self.id_).isdigit() is False:
                self.registros_faltantes = self.registros_faltantes + 1
            else:
    #Se asume que la clasificacion viene como string, por lo que va a buscar el ID correspondiente a la tabla
                self.clas_formato = self.clasificacion.ljust(5)
                self.encuentra_c = Conexion.Conexion_db.Base_datos().buscar_clasificacion(self.clas_formato.upper())
                self.formato_cls = str(self.encuentra_c[0])

    #Se asume que en el archivo json viene nombre d eusuario y no ID por lo que va a buscar el ID correspondiente a la tabla 
                self.encuentra_u = Conexion.Conexion_db.Base_datos().buscar_usuario(self.usuario.strip().lower())
                self.formato_usr = str(self.encuentra_u[0])   
    #Verifica si clasificacion y usuario existen en base de datos, de ser así continua el flujo (debido a dependencias en la base de datos)
                if self.encuentra_u != None and self.encuentra_c != None:
    #Busca si existe base de datos ingresada (con su respectiva clasificacion)
                    self.encuentra = Conexion.Conexion_db.Base_datos().buscar(self.id_)
    #Si no existe la base de datos, inserta un nuevo registro
                    if self.encuentra == " ":
                        self.no_esta = 1
                        for self.csv in archivo_csv:
                            self.estado_ok=Conexion.Conexion_db.Base_datos().consulta_csv(self.csv[1], self.csv[3])

                        self.ingresa = Conexion.Conexion_db.Base_datos().ingresa_base(self.id_, self.nombre, self.descripcion, self.formato_usr, self.formato_cls)

                        if self.ingresa is True:
                            self.registros_completos = self.registros_completos + 1
    #Si registro se realiza de forma correcta, ingresa evaluar clasificacion, sino sale del flujo
                            self.envia_correo(self.encuentra_u, self.clas_formato, self.nombre, correo, contrasenia, archivo_csv)
                        else:
                            self.registros_faltantes= self.registros_faltantes + 1   
                    else:  
    #Si la base de datos existe, la actualiza
                        self.actualiza  = Conexion.Conexion_db.Base_datos().actualiza_base(self.id_, self.descripcion, self.encuentra_u[0], self.encuentra_c[0])
                        if self.actualiza is True:
                            self.registros_completos = self.registros_completos + 1
    #Si la base de datos fue actualizada correctamente, evalua clasificacion
                            self.envia_correo(self.encuentra_u, self.clas_formato, self.nombre, correo, contrasenia, archivo_csv)
                        else:
                            self.registros_faltantes = self.registros_faltantes + 1
                else:
                    self.registros_faltantes = self.registros_faltantes + 1   
    #Retorna la cantidad de registros totales encontradas en archivo JSON, los registros grabados y los registros no grabados  
        return self.total_registros, self.registros_faltantes, self.registros_completos


    def envia_correo(self, user_id, clasificacion, nombre, correo, contrasenia, archivo_csv):
        #Si la clasificacion es alta, envia un correo con nombre de tabla, clasificacion, estado del usuario asignado y solicita Ok 
        if clasificacion.strip().upper() == 'HIGH':
                correo_manager = Conexion.Conexion_db.Base_datos().envia_correo(user_id)
        #Busca estado de usuario en archivo CSV
                for self.csv in archivo_csv:
                    self.user_formato = "".join(user_id[0])
                    if str(self.csv[1]) == user_id[0]:
                        estado = self.csv[2]

                        self.mensaje = ("""La clasificación de la base de datos """ + nombre + """ fue: 'HIGH', favor enviar ok.
                        El estado del usuario asignado """ + str(user_id[0]) + """ es: """ + estado)

                        #Enviar correo
                        self.estado_correo = Funciones.Correo.Correo().env_notifica_correo(correo, contrasenia, self.mensaje, correo_manager)