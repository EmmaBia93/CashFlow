import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from database.manage import crear_cajero

# Funciones para la UI de registro
def registrar_usuario(entry_nombre, entry_usuario, entry_contrasena, entry_confirmar_contrasena):
    nombre = entry_nombre.get()
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()
    confirmar_contrasena = entry_confirmar_contrasena.get()

    if not nombre or not usuario or not contrasena or not confirmar_contrasena:
        messagebox.showerror("Error", "Todos los campos son obligatorios")
        return

    if contrasena != confirmar_contrasena:
        messagebox.showerror("Error", "Las contraseñas no coinciden")
        return

    if crear_cajero(nombre, usuario, contrasena):
        return True
    else:
        return False

def abrir_ventana_registro(ventana_registro):
    # Configuración de la ventana de registro
    ventana_registro.title("Registro de nuevo usuario")
    ventana_registro.geometry("400x500")

    # Cargar imagen de usuario
    imagen_usuario = ctk.CTkImage(Image.open("img/user.png"), size=(100, 100))
    label_imagen = ctk.CTkLabel(ventana_registro, image=imagen_usuario,text="")
    label_imagen.pack(pady=20)

    # Campos de entrada
    entry_nombre = ctk.CTkEntry(ventana_registro, placeholder_text="Nombre Completo",width=200)
    entry_usuario = ctk.CTkEntry(ventana_registro, placeholder_text="Usuario",width=200)
    entry_contrasena = ctk.CTkEntry(ventana_registro, placeholder_text="Contraseña", show="*",width=200)
    entry_confirmar_contrasena = ctk.CTkEntry(ventana_registro, placeholder_text="Confirmar Contraseña", show="*",width=200)

    entry_nombre.pack(pady=10)
    entry_usuario.pack(pady=10)
    entry_contrasena.pack(pady=10)
    entry_confirmar_contrasena.pack(pady=10)

    # Botón para registrar
    btn_registrar = ctk.CTkButton(ventana_registro, text="Registrar", 
                                  command=lambda: registrar_usuario(entry_nombre, entry_usuario, entry_contrasena, entry_confirmar_contrasena))
    btn_registrar.pack(pady=20)
