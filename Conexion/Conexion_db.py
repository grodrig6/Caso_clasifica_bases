import sqlite3 

class Base_datos:
    def __init__(self):
        self.conexion_clasifica = sqlite3.connect("CLASIFICACION.db")

#Busca si existe registro en tabla base de datos
    def buscar(self, id_):
        try:
            self.cursor_busca=self.conexion_clasifica.cursor()
            self.cursor_busca.execute("""SELECT IDEN_NOMBRE_DB FROM BASE_DE_DATOS WHERE IDEN_ID_BASE_DE_DATOS = """ + str(id_))
            self.encuentra=self.cursor_busca.fetchone()

            if self.encuentra  != None:
                self.cursor_busca_b=self.conexion_clasifica.cursor()
                self.cursor_busca_b.execute("""SELECT IDEN_ID_BASE_DE_DATOS, IDEN_NOMBRE_DB, IDEN_DESCRIPCION,
                    u.US_NOMBRE_USUARIO, c.CL_NIVEL_CLASIFICACION
                    FROM BASE_DE_DATOS b
                    JOIN USUARIOS u ON b.FK_US_ID_USUARIO = u.US_ID_USUARIO
                    JOIN CLASIFICACIONES c ON b.FK_CL_ID_CLASIFICACION = c.CL_ID_CLASIFICACION
                    WHERE b.IDEN_ID_BASE_DE_DATOS = """ + str(id_))
            
                self.resultado=self.cursor_busca_b.fetchone()
                self.cierra_conexion()
                return self.resultado
            else:
                return " "
        except Exception:
            self.cierra_conexion()
            return " " 

#Busca usuario por nombre
    def buscar_usuario(self, usuario):
        try:
            self.cursor_busca=self.conexion_clasifica.cursor()
            self.cursor_busca.execute("SELECT US_ID_USUARIO FROM USUARIOS WHERE US_NOMBRE_USUARIO = '"+ usuario +"'")
    
            self.resultado=self.cursor_busca.fetchone()
            self.cierra_conexion()
            return self.resultado
        except Exception:
            self.cierra_conexion()
            return " "  
    
#Busca clasificacion por nivel (bajo, medio, alto)
    def buscar_clasificacion(self, clasificacion):
        try:
            self.cursor_busca=self.conexion_clasifica.cursor()
            self.cursor_busca.execute("""SELECT CL_ID_CLASIFICACION FROM CLASIFICACIONES 
                WHERE CL_NIVEL_CLASIFICACION = '""" + clasificacion + """'""")
    
            self.resultado=self.cursor_busca.fetchone()
            self.cierra_conexion()
            return self.resultado
        except Exception:
            self.cierra_conexion()
            return " "    

#Actualiza tabla base de datos    
    def actualiza_base(self, id_, descripcion, usuario, clasificacion):
        #try:
            self.cursor_actualiza_base=self.conexion_clasifica.cursor()
            self.cursor_actualiza_base.execute("""UPDATE BASE_DE_DATOS SET IDEN_DESCRIPCION = '""" + descripcion + """', FK_US_ID_USUARIO = '""" + usuario + """', FK_CL_ID_CLASIFICACION = """ + str(clasificacion) + """ WHERE IDEN_ID_BASE_DE_DATOS = """ + str(id_))
        
            self.conexion_clasifica.commit()
            self.cierra_conexion()
            return True
        #except Exception :
            self.cierra_conexion()
            return False
        
#Ingresa registro a tabla base de datos
    def ingresa_base(self, id_,  nombre, descripcion, usuario, clasificacion):
        try:
            datos = [(id_, nombre, descripcion, usuario, str(clasificacion))]
            self.cursor_ingresa_base = self.conexion_clasifica.cursor()
            self.cursor_ingresa_base.executemany("""INSERT INTO BASE_DE_DATOS (IDEN_ID_BASE_DE_DATOS, IDEN_NOMBRE_DB, IDEN_DESCRIPCION, 
            FK_US_ID_USUARIO, FK_CL_ID_CLASIFICACION) VALUES (?,?,?,?,?)""", datos)

            self.conexion_clasifica.commit()
            self.cierra_conexion()
            return True
        except Exception:
            self.cierra_conexion()
            return False


    def consulta_csv(self, usuario, manager):
        try:
            self.cursor_busca_csv=self.conexion_clasifica.cursor()
            self.cursor_busca_csv.execute("""SELECT US_NOMBRE_USUARIO FROM USUARIOS WHERE US_ID_USUARIO =  '""" + str(usuario) + """'
            AND FK_MA_ID_MANAGER = '""" + str(manager) + """'""")
            self.resultado=self.cursor_busca_csv.fetchone()

            self.encuentra = True

            if self.resultado is None:
                self.encuentra = False
            
            self.cierra_conexion()
            #Evalua si se encontro registros
            return self.encuentra
        except Exception:
            self.cierra_conexion()
            return False

#Busca correo de manager
    def envia_correo(self, user_id):
        try:
            self.cursor_busca=self.conexion_clasifica.cursor()

            self.cursor_busca.execute("""SELECT m.MA_CORREO_MANAGER 
                FROM MANAGERS m JOIN USUARIOS u 
                ON m.MA_ID_MANAGER = u.FK_MA_ID_MANAGER
                WHERE  u.US_ID_USUARIO = '""" + str(user_id[0])+ """'""")
            
            self.resultado=self.cursor_busca.fetchone()
            self.cierra_conexion()
            #Evalua si se encontro registros
            return self.resultado[0]
        except Exception:
            self.cierra_conexion()
            return " "
  

    def cierra_conexion(self):
        self.conexion_clasifica.close()
