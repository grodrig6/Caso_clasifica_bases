import tkinter as tk
import Conexion.Conexion_db
import Conexion.Conexion_empleado
import Funciones.Desencripta
from Interfaz import Clasifica

class Principal(tk.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.pack()
        self.master.title("Menu")
        self.config(width="600", heigh="350")
        self.crea_principal()

    def crea_principal(self):
        #Genera labels para inicio de programa
        self.lb_menu = tk.Label(self, text="Clasificación de bases de datos")
        self.lb_menu.grid(row=1,column=2)
        self.lb_menu.config(padx=5, pady=15, font=("Arial", 18))

        self.lb_user = tk.Label(self, text="Usuario", justify="left")
        self.lb_user.grid(row=3,column=1)
        self.lb_user.config(padx=5, pady=15, justify="right", font=("Arial", 14))
        
        self.lb_pass = tk.Label(self, text="Contraseña")
        self.lb_pass.grid(row=5,column=1)
        self.lb_pass.config(padx=5, pady=15,font=("Arial", 14))

        self.lb_mensaje = tk.Label(self,text="")
        self.lb_mensaje.grid(row=8,column=3)
        self.lb_mensaje.config(padx=50, pady=15)

        #Genera cuadros de texto
        self.tx_usuario=tk.Entry(self)
        self.tx_usuario.grid(row=3,column=2)
        self.tx_usuario.config(font=("Arial", 14))

        self.tx_pass=tk.Entry(self)
        self.tx_pass.grid(row=5,column=2)
        self.tx_pass.config(show="*", font=("Arial", 14))
        
        #Genera boton de login
        self.bt_login=tk.Button(self, text="Entrar", command=self.codigo_bt_entrar)
        self.bt_login.grid(row=7,column=2)
        self.bt_login.config(font=("Arial", 16))

    def codigo_bt_entrar(self):
        #toma valores de caja de texto usuario y contraseña
        self.usuario = self.tx_usuario.get()
        self.contrasenia = self.tx_pass.get()

        #Evalua datos de usuario y contraseña 
        self.valida_pass = Conexion.Conexion_empleado.Empleado().buscar(self.usuario, self.contrasenia)

        #Si los datos son correctos, muestra contenido, sino, infomarma error
        if self.valida_pass is True:
            self.master.destroy()
            root1 = tk.Tk()
            appE = Clasifica.Ejecutar(master=root1)
            appE.mainloop()
        else:
            if self.valida_pass is False:
                self.lb_mensaje.config(text="Usuario o contraseña invalidados")
            else:
                self.lb_mensaje.config(text="Error de conexión ")
        
        
