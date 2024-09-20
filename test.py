import sys
from PIL import Image
from CTkMessagebox import CTkMessagebox
from database.manage import verificar_credenciales, crear_cajero
from gui.main_windows import Calculadora
from gui.registro import RegistroUsuario
from tkinter import messagebox
from ttkbootstrap import Style
from ttkbootstrap.constants import *
import tkinter as ttk

class InicioSesion:
    def __init__(self):
        self.intentos_fallidos = 0
        self.inicio_exitoso = False
        self.max_intentos = 3  
        self.ventana = None
        self.entry_usuario = None
        self.entry_contrasena = None
        self.ventana_registro = None

        # Estilo ttkbootstrap
        self.style = Style("darkly")

    def mostrar_ventana(self):
        """Muestra la ventana de inicio de sesión y controla el flujo."""
        self.ventana = self.style.master
        self.ventana.title("Inicio de sesión")
        self.ventana.geometry("400x500+500+100")
        self.ventana.resizable(width=False, height=False)

        # Cargar imagen de usuario
        imagen_usuario = Image.open("img/user.png")
        imagen_usuario = imagen_usuario.resize((100, 100))  # Redimensionar la imagen
        label_imagen = ttk.Label(self.ventana, image=imagen_usuario)
        label_imagen.image = imagen_usuario  # Mantener una referencia a la imagen
        label_imagen.pack(pady=30)

        # Campos de entrada
        self.entry_usuario = ttk.Entry(self.ventana, width=30)
        self.entry_contrasena = ttk.Entry(self.ventana, width=30, show="*")

        self.entry_usuario.insert(0, "Usuario")
        self.entry_contrasena.insert(0, "Contraseña")

        self.entry_usuario.pack(pady=10)
        self.entry_contrasena.pack(pady=10)
        self.entry_contrasena.bind("<Return>", self.acept)

        # Botones
        self.btn_login = ttk.Button(self.ventana, text="Iniciar sesión", command=self.iniciar_sesion)
        self.btn_login.pack(pady=15)
        self.btn_login.bind("<Return>", self.acept)

        btn_nuevo_usuario = ttk.Button(self.ventana, text="Registrarse", command=self.abrir_ventana_registro)
        btn_nuevo_usuario.pack(pady=40)

        self.ventana.mainloop()

    def acept(self, event):
        self.btn_login.invoke()

    def abrir_ventana_registro(self):
        self.registro()

    def iniciar_sesion(self):
        """Verifica las credenciales y controla los intentos."""
        usuario = self.entry_usuario.get()
        contrasena = self.entry_contrasena.get()

        if verificar_credenciales(usuario, contrasena):
            self.inicio_exitoso = True
            self.ventana.destroy()
            principal = Calculadora(usuario)
        else:
            self.intentos_fallidos += 1
            self.label_info = ttk.Label(self.ventana, text="Usuario o Contraseña Incorrecto", foreground="#ff5733")
            self.label_info.pack(pady=20)

            if self.intentos_fallidos >= self.max_intentos:
                msg_box = CTkMessagebox(master=self.ventana,
                                         title="Error!!!",
                                         message="Se ha excedido la cantidad de intentos",
                                         option_1="OK",
                                         icon="cancel",
                                         font=("Lato Bold", 16),
                                         icon_size=(60, 60))

                if msg_box.get() == "OK":
                    self.ventana.destroy()  
                    sys.exit()

    def registro(self):
        if self.ventana_registro is None or not self.ventana_registro.winfo_exists():
            self.ventana_registro = ttk.Toplevel(self.ventana)
            self.ventana_registro.title("Registro de nuevo usuario")
            self.ventana_registro.geometry("400x500")
            self.ventana_registro.attributes("-topmost", True)

            # Cargar imagen de usuario
            imagen_usuario = Image.open("img/user.png")
            imagen_usuario = imagen_usuario.resize((100, 100))  # Redimensionar la imagen
            label_imagen = ttk.Label(self.ventana_registro, image=imagen_usuario)
            label_imagen.image = imagen_usuario  # Mantener una referencia a la imagen
            label_imagen.pack(pady=20)

            # Campos de entrada
            self.entry_nnombre = ttk.Entry(self.ventana_registro, width=30)
            self.entry_nusuario = ttk.Entry(self.ventana_registro, width=30)
            self.entry_ncontrasena = ttk.Entry(self.ventana_registro, width=30, show="*")
            self.entry_nconfirmar_contrasena = ttk.Entry(self.ventana_registro, width=30, show="*")

            self.entry_nnombre.insert(0, "Nombre Completo")
            self.entry_nusuario.insert(0, "Usuario")
            self.entry_ncontrasena.insert(0, "Contraseña")
            self.entry_nconfirmar_contrasena.insert(0, "Confirmar Contraseña")

            self.entry_nnombre.pack(pady=10)
            self.entry_nusuario.pack(pady=10)
            self.entry_ncontrasena.pack(pady=10)
            self.entry_nconfirmar_contrasena.pack(pady=10)

            # Botón para registrar
            btn_registrar = ttk.Button(self.ventana_registro, text="Registrar", command=self.registrar_usuario)
            btn_registrar.pack(pady=20)
            self.ventana_registro.focus()

    def registrar_usuario(self):
        nombre = self.entry_nnombre.get()
        usuario = self.entry_nusuario.get()
        contrasena = self.entry_ncontrasena.get()
        confirmar_contrasena = self.entry_nconfirmar_contrasena.get()

        # Validar que los campos no estén vacíos
        if not nombre or not usuario or not contrasena or not confirmar_contrasena:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        # Validar que las contraseñas coincidan
        if contrasena != confirmar_contrasena:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return

        # Intentar registrar al cajero
        if crear_cajero(nombre, usuario, contrasena):
            self.ventana_registro.destroy()
        else:
            messagebox.showerror("Error", "Error al registrar el usuario")

# Para ejecutar el inicio de sesión
if __name__ == "__main__":
    inicio = InicioSesion()
    inicio.mostrar_ventana()
