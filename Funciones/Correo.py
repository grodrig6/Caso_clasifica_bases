import smtplib
from email.mime.text import MIMEText
from email.header import Header

class Correo:
    def __init__(self):
        self.mensaje1 = 'Asunto: Reváldas de bases de datos año en curso' 

    def env_notifica_correo(self, usuario, contrasenia, mensaje, destinatario):
        try:
            self.message = MIMEText(mensaje, 'plain', 'utf-8')
            self.message['From'] = Header(usuario, 'utf-8')
            self.message['To'] =  Header(destinatario, 'utf-8')

            self.subject = 'Asunto: Reváldas de bases de datos año en curso' 
            self.message['Subject'] = Header(self.subject, 'utf-8')


            #conecta, correo y puerto 
            self.servidor = smtplib.SMTP(host='smtp.gmail.com', port=587)
            self.servidor.ehlo()

            self.servidor.starttls()

            #inicia sesion
            self.servidor.login(user=usuario, password=contrasenia)
        
            self.servidor.sendmail(usuario, destinatario, self.message.as_string())
            return True
        except smtplib.SMTPAuthenticationError:
            return "Error en correo o contraseña "
        finally:
            self.servidor.quit()

    def valida_correo(self, correo, contrasenia):
        try:
            #conecta, correo y puerto 
            servidor = smtplib.SMTP(host='smtp.gmail.com', port=587)
            servidor.ehlo()
            servidor.starttls()
            #inicia sesion
            servidor.login(user=correo, password=contrasenia)
            return True
        except smtplib.SMTPAuthenticationError:
            return False
        except Exception:
            return False
        finally:
            servidor.quit()