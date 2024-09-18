import sys
import customtkinter as ctk
from PIL import Image
from CTkMessagebox import CTkMessagebox
from database.manage import verificar_credenciales
from gui.main_windows import Calculadora

class InicioSesion:
    def __init__(self):
        self.intentos_fallidos = 0
        self.inicio_exitoso = False
        self.max_intentos = 3  # Número máximo de intentos permitidos
        self.ventana = None
        self.entry_usuario = None
        self.entry_contrasena = None

    def mostrar_ventana(self):
        """Muestra la ventana de inicio de sesión y controla el flujo."""
        self.ventana = ctk.CTk()
        self.ventana.title("Inicio de sesión")
        self.ventana.geometry("400x400")

        # Cargar imagen de usuario (asegúrate de tener una imagen llamada 'usuario.png')
        imagen_usuario = ctk.CTkImage(Image.open("img/user.png"), size=(100, 100))
        label_imagen = ctk.CTkLabel(self.ventana, image=imagen_usuario, text="")
        label_imagen.pack(pady=20)

        # Campos de entrada
        self.entry_usuario = ctk.CTkEntry(self.ventana, placeholder_text="Usuario", width=200)
        self.entry_contrasena = ctk.CTkEntry(self.ventana, placeholder_text="Contraseña", show="*", width=200)

        self.entry_usuario.pack(pady=10)
        self.entry_contrasena.pack(pady=10)

        # Botones
        btn_login = ctk.CTkButton(self.ventana, text="Iniciar sesión", command=self.iniciar_sesion)
        btn_login.pack(pady=10)

        btn_nuevo_usuario = ctk.CTkButton(self.ventana, text="Registrarse como nuevo usuario", command=self.abrir_ventana_registro)
        btn_nuevo_usuario.pack(pady=10)

        self.ventana.mainloop()
    
    def abrir_ventana_registro(self):
        """Aquí puedes abrir la ventana para registrar un nuevo usuario."""
        pass  # Implementar según sea necesario

    def iniciar_sesion(self):
        """Verifica las credenciales y controla los intentos."""
        usuario = self.entry_usuario.get()
        contrasena = self.entry_contrasena.get()

        if verificar_credenciales(usuario, contrasena):
           
            self.inicio_exitoso = True
            self.ventana.destroy()
            principal = Calculadora()
            
        else:
            self.intentos_fallidos += 1
            CTkMessagebox(title="Error", message=f"Usuario o contraseña incorrectos. Intento {self.intentos_fallidos}/{self.max_intentos}", icon="cancel")
            
            if self.intentos_fallidos >= self.max_intentos:
                CTkMessagebox(title="Error", message="Número máximo de intentos alcanzado. Cerrando el programa.", icon="cancel")
                self.inicio_exitoso = False
                self.ventana.destroy()  # Cierra la ventana de inicio de sesión
                sys.exit()  # Cierra toda la aplicación

    def verificar_credenciales(self, usuario, contrasena):
        """Aquí implementas la lógica para verificar las credenciales del usuario."""
        # Simulación: reemplaza esto con tu lógica de autenticación real
        usuarios_validos = {"admin": "1234", "user": "password"}
        return usuarios_validos.get(usuario) == contrasena

    def es_inicio_exitoso(self):
        """Devuelve el estado del inicio de sesión."""
        return self.inicio_exitoso
