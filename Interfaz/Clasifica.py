import tkinter as tk
import Funciones.Recibe_archivo
import Funciones.Correo
import Conexion.Conexion_empleado

class Ejecutar(tk.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.pack()
        self.master.title("Clasificar")
        self.config(width="600", heigh="350")
        self.crea_principal()

    def crea_principal(self):
        self.label1 = tk.Label(self, text="Si desea clasificar bases de datos", font=("Arial", 16),padx=5, pady=20)
        self.label1.grid(row=2,column=0)
        self.label1.config()
        

        self.label2 = tk.Label(self, text="ingrese correo y contraseña, el correo que", font=("Arial", 16), padx=5, pady=20)
        self.label2.grid(row=2,column=1)
        self.label2.config()

        self.label3 = tk.Label(self, text="ingrese será utilizado como remitente", font=("Arial", 16), padx=5, pady=20)
        self.label3.grid(row=2,column=2)
        self.label3.config()

        #Label para retornar informacion y algunos errores
        self.label4 = tk.Label(self, text="", font=("Arial", 12), padx=5, pady=10)
        self.label4.grid(row=7,column=1)
        self.label4.config()

        self.label5 = tk.Label(self, text="", font=("Arial", 12), padx=5, pady=10)
        self.label5.grid(row=8,column=1)
        self.label5.config()

        self.label6 = tk.Label(self, text="", font=("Arial", 12), padx=5, pady=10)
        self.label6.grid(row=9,column=1)
        self.label6.config()

        #Genera labels para ingreso decorreo y contraseña
        self.lb_menu = tk.Label(self, text="Correo")
        self.lb_menu.grid(row=4,column=0)
        self.lb_menu.config(padx=5, pady=15, font=("Arial", 14))

        self.lb_user = tk.Label(self, text="Contraseña", justify="left")
        self.lb_user.grid(row=5,column=0)
        self.lb_user.config(padx=5, pady=15, justify="right", font=("Arial", 14))

        #Genera cuadros de texto para ingreso de correo y contraseña
        self.tx_usuario=tk.Entry(self)
        self.tx_usuario.grid(row=4,column=1)
        self.tx_usuario.config(font=("Arial", 14))

        self.tx_pass=tk.Entry(self)
        self.tx_pass.grid(row=5,column=1)
        self.tx_pass.config(show="*", font=("Arial", 14))

        #Define boton
        self.bt_ejecutar=tk.Button(self, text="Ejecutar", command=lambda:[self.codigo_bt_ejecutar(), self.label1.grid_remove()])
        self.bt_ejecutar.grid(row=6,column=1)
        self.bt_ejecutar.config(padx=5, pady=10, font=("Arial", 16))

    def codigo_bt_ejecutar(self):
        self.correo = self.tx_usuario.get()
        self.contrasenia = self.tx_pass.get()

        #Valida correo
        correo_ok = Funciones.Correo.Correo().valida_correo(self.correo, self.contrasenia)

        if correo_ok is True:
            #Rescata archivo JSON desde carpeta
            self.archivo_json = self.carga_archivo=Funciones.Recibe_archivo.Archivo().cargar_json()
            if self.archivo_json != "existe":
                #Rescata arhcivo CSV
                self.archivo_csv = self.carga_archivo=Funciones.Recibe_archivo.Archivo().cargar_csv()

                if self.archivo_csv != "existe":
                    #Realiza tratamiento de información
                    resultado =Funciones.Recibe_archivo.Archivo().valida_json(self.archivo_json, self.archivo_csv, self.correo, self.contrasenia)
                    self.obtenido1 = "Registros leidos (" + str(resultado[0]) + ")" 
                    self.obtenido2 = "Registros insertados o actualizados (" + str(resultado[2]) + ")"
                    self.obtenido3 = "Registros NO insertados NI actualizados (" + str(resultado[1]) + ")"
                    self.label4.config(text=self.obtenido1, fg="black")
                    self.label5.config(text=self.obtenido2, fg="black")
                    self.label6.config(text=self.obtenido3, fg="black")
                else:
                    self.label4.config(text="Archivo CSV no existe", fg="red")
            else:
                self.label4.config(text="Archivo JSON no existe", fg="red")
        else:
            self.label4.config(text="Correo o contraseña erroneos", fg="red")


