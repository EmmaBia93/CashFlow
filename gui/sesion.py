import customtkinter as ctk
from sqlalchemy.orm import sessionmaker
from tkinter import messagebox
from PIL import Image
from database.manage import crear_cajero, verificar_credenciales
from gui.registro import abrir_ventana_registro



ventana_registro_abierta = None

def abrir_ventana_registro_unica():
    global ventana_registro_abierta

    if ventana_registro_abierta is None or not ventana_registro_abierta.winfo_exists():
        # Si la ventana de registro no existe o ha sido cerrada, se abre una nueva
        ventana_registro_abierta = ctk.CTkToplevel()
        abrir_ventana_registro(ventana_registro_abierta)
    else:
        # Si la ventana ya está abierta, la llevamos al frente
        ventana_registro_abierta.focus()


# Funciones de la UI
def iniciar_sesion():
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()

    if verificar_credenciales(usuario, contrasena):
        messagebox.showinfo("Éxito", "Inicio de sesión exitoso")
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")






# Configuración de la interfaz
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Inicio de sesión")
root.geometry("400x400")

# Cargar imagen de usuario (asegúrate de tener una imagen llamada 'usuario.png')
imagen_usuario = ctk.CTkImage(Image.open("img/user.png"), size=(100, 100))
label_imagen = ctk.CTkLabel(root, image=imagen_usuario,text="")
label_imagen.pack(pady=20)

# Campos de entrada

entry_usuario = ctk.CTkEntry(root, placeholder_text="Usuario",width=200)
entry_contrasena = ctk.CTkEntry(root, placeholder_text="Contraseña", show="*",width=200)

entry_usuario.pack(pady=10)
entry_contrasena.pack(pady=10)

# Botones
btn_login = ctk.CTkButton(root, text="Iniciar sesión", command=iniciar_sesion)
btn_login.pack(pady=10)

btn_nuevo_usuario = ctk.CTkButton(root, text="Registrarse como nuevo usuario",  command=abrir_ventana_registro_unica)
btn_nuevo_usuario.pack(pady=10)



root.mainloop()