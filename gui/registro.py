import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from database.manage import crear_cajero



class RegistroUsuario:
    def __init__(self):
        self.ventana_registro = None
        self.configurar_ventana()

    def configurar_ventana(self):
        # Configuración de la ventana de registro
        self.ventana_registro = ctk.CTk()
        self.ventana_registro.title("Registro de nuevo usuario")
        self.ventana_registro.geometry("400x500")

        # Cargar imagen de usuario
        # imagen_usuario = ctk.CTkImage(Image.open("img/user.png"), size=(100, 100))
        # label_imagen = ctk.CTkLabel(self.ventana_registro, image=imagen_usuario, text="")
        # label_imagen.pack(pady=20)

        # Campos de entrada
        self.entry_nombre = ctk.CTkEntry(self.ventana_registro, placeholder_text="Nombre Completo", width=200)
        self.entry_usuario = ctk.CTkEntry(self.ventana_registro, placeholder_text="Usuario", width=200)
        self.entry_contrasena = ctk.CTkEntry(self.ventana_registro, placeholder_text="Contraseña", show="*", width=200)
        self.entry_confirmar_contrasena = ctk.CTkEntry(self.ventana_registro, placeholder_text="Confirmar Contraseña", show="*", width=200)

        self.entry_nombre.pack(pady=10)
        self.entry_usuario.pack(pady=10)
        self.entry_contrasena.pack(pady=10)
        self.entry_confirmar_contrasena.pack(pady=10)

        # Botón para registrar
        btn_registrar = ctk.CTkButton(self.ventana_registro, text="Registrar", 
                                      command=self.registrar_usuario)
        btn_registrar.pack(pady=20)

    def registrar_usuario(self):
        nombre = self.entry_nombre.get()
        usuario = self.entry_usuario.get()
        contrasena = self.entry_contrasena.get()
        confirmar_contrasena = self.entry_confirmar_contrasena.get()

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
            messagebox.showinfo("Éxito", "Usuario registrado exitosamente")
            self.ventana_registro.destroy()
        else:
            messagebox.showerror("Error", "Error al registrar el usuario")
            
            
            
            
