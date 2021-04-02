import base64


class Desencripta_pass():
    #def __init__(self):
    #    print("constru")
        #self.ejecuta_encritado(contrasenia)
        
    #Encripta contraseña del usuario
    def ejecuta_encriptado(self, contrasenia):
        self.resultado = base64.b64encode(bytes(contrasenia, 'utf-8'))
        self.pass_1 = base64.b64encode(self.resultado)
        return self.pass_1 