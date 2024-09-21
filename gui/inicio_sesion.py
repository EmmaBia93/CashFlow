import sys
import customtkinter as ctk
from PIL import Image
from CTkMessagebox import CTkMessagebox
from database.manage import verificar_credenciales
from gui.main_windows import Calculadora
from tkinter import messagebox
from database.manage import crear_cajero
import re

class InicioSesion:
    def __init__(self):
        self.hidden=True
        self.intentos_fallidos = 0
        self.inicio_exitoso = False
        self.max_intentos = 3  
        self.ventana = None
        self.entry_usuario = None
        self.entry_contrasena = None
        self.ventana_registro=None

    def mostrar_ventana(self):
        """Muestra la ventana de inicio de sesión y controla el flujo."""
        self.ventana = ctk.CTk()
        self.ventana.title("Inicio de sesión")
        self.ventana.geometry("400x550+500+100")
        self.ventana.resizable(width=False,height=False)

        # Cargar imagen de usuario (asegúrate de tener una imagen llamada 'usuario.png')
        imagen_usuario = ctk.CTkImage(Image.open("img/gamer.png"), size=(100, 100))
        label_imagen = ctk.CTkLabel(self.ventana, image=imagen_usuario, text="")
        label_imagen.pack(pady=30)

        # Campos de entrada
        self.entry_usuario = ctk.CTkEntry(self.ventana, 
                                          placeholder_text="Usuario", 
                                          width=200,
                                          height=40,
                                          fg_color="#181818",
                                          font=("Lato Bold",17))
        
        self.entry_contrasena = ctk.CTkEntry(self.ventana, 
                                             placeholder_text="Contraseña", 
                                             show="*", 
                                             width=200,
                                             height=40,
                                             fg_color="#181818",
                                             font=("Lato Bold",17))

        
        
        self.entry_usuario.pack(pady=10)
        self.entry_contrasena.pack(pady=10)
        self.entry_contrasena.bind("<Return>", self.acept)
        
        self.close_eye = ctk.CTkImage(Image.open("img/hide.png"), size=(20, 20))
        self.eye = ctk.CTkImage(Image.open("img/vision.png"), size=(20, 20))
        
        self.btn_eye = ctk.CTkButton(self.ventana,image=self.close_eye,bg_color="#181818",fg_color="#181818", 
                            hover_color="#181818",text="",width=10,height=20,command=self.visible_hidden)
        self.btn_eye.place(x=262,y=237)
        
        # Botones
        self.btn_login = ctk.CTkButton(self.ventana, 
                                       text="Iniciar sesión", 
                                       command=self.iniciar_sesion,
                                       fg_color="#956dae",
                                       hover_color="#755689",
                                       border_color="#46225b",
                                       border_width=2,
                                       font=("Lato Bold",15),
                                       height=40)
        self.btn_login.pack(pady=15)
        self.btn_login.bind("<Return>",self.acept)
        btn_nuevo_usuario = ctk.CTkButton(self.ventana, 
                                          text="Registrarse", 
                                          command=self.abrir_ventana_registro,
                                          fg_color="#8cbc66",
                                        hover_color="#65884a",
                                        border_color="#4d7a2a",
                                        border_width=2,
                                        font=("Lato Bold",15),
                                        height=40)
        btn_nuevo_usuario.pack(pady=40)
        
        
        
        
        self.ventana.mainloop()
    
    
    def visible_hidden(self):
        if self.hidden:
            self.btn_eye.configure(image=self.eye)
            self.entry_contrasena.configure(show="")
            self.hidden=False
        else:
            self.btn_eye.configure(image=self.close_eye)
            self.entry_contrasena.configure(show="*")
            self.hidden=True
            
    
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
            self.label_info = ctk.CTkLabel(self.ventana,text="Usuario o Contraseña Incorrecto",text_color="#ff5733")
            self.label_info.pack(pady=20)
            
            if self.intentos_fallidos >= self.max_intentos:
                msg_box = CTkMessagebox(master=self.ventana,
                                        title="Error!!!",
                                        message="Se he excedido la cantidad de intentos",
                                        option_1="OK",
                                        icon="cancel",
                                        font=("Lato Bold",16),
                                        icon_size=(60, 60))
                
                if msg_box.get() == "OK":
                    self.ventana.destroy()  
                    sys.exit()  



   


    def registro(self):
        if self.ventana_registro is None or not self.ventana_registro.winfo_exists():
            self.ventana_registro = ctk.CTkToplevel()
            self.ventana_registro.title("Registro de nuevo usuario")
            self.ventana_registro.geometry("400x600+0+0")
            self.ventana_registro.attributes("-topmost", True)
            self.ventana_registro.resizable(width=False,height=False)
            # Cargar imagen de usuario
            imagen_usuario = ctk.CTkImage(Image.open("img/user.png"), size=(100, 100))
            label_imagen = ctk.CTkLabel(self.ventana_registro, image=imagen_usuario, text="")
            label_imagen.pack(pady=40)

            # Campos de entrada
            self.entry_nnombre = ctk.CTkEntry(self.ventana_registro, 
                                              placeholder_text="Nombre Completo",
                                              width=300,
                                              height=40,
                                              fg_color="#181818",
                                              font=("Lato Bold",17))
            self.entry_nusuario = ctk.CTkEntry(self.ventana_registro,
                                               placeholder_text="Usuario",
                                               width=300,
                                               height=40,
                                              fg_color="#181818",
                                              font=("Lato Bold",17))
            self.entry_ncontrasena = ctk.CTkEntry(self.ventana_registro,
                                                  placeholder_text="Contraseña",
                                                  show="*",
                                                  width=300,
                                                  height=40,
                                                fg_color="#181818",
                                                font=("Lato Bold",17))
            self.entry_nconfirmar_contrasena = ctk.CTkEntry(self.ventana_registro,
                                                            placeholder_text="Confirmar Contraseña",
                                                            show="*",
                                                            width=300,
                                                            height=40,
                                                            fg_color="#181818",
                                                            font=("Lato Bold",17))

            self.entry_nnombre.pack(pady=10)
            self.entry_nusuario.pack(pady=10)
            self.entry_ncontrasena.pack(pady=10)
            self.entry_nconfirmar_contrasena.pack(pady=10)

            # Botón para registrar
            btn_registrar = ctk.CTkButton(self.ventana_registro,
                                          text="Registrar",
                                          fg_color="#445f9b",
                                          hover_color="#2f426d",
                                          border_color="#11285f",
                                          border_width=2,
                                          height=40, 
                                        command=self.registrar_usuario,
                                        font=("Lato Bold",15))
            btn_registrar.pack(pady=50)
            self.ventana_registro.focus()
    
    def registrar_usuario(self):
        regex_pass = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$"
        regex_user =  r"^[a-zA-Z0-9]([._]?[a-zA-Z0-9]+)*$" 
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
        
        if not re.match(regex_user,nombre):
            CTkMessagebox(
                          title="ATENCIÓN!!",
                          message=f"Nombre de usuario no válido",
                          font=("Lato Bold",15),
                          icon="warning"
                          )
            return
        
        if not re.match(regex_pass, contrasena):
            CTkMessagebox(width=400,
                          height=300,
                          title="ATENCIÓN!!",
                          message=f"""Contraseña poco segura, la contraseña debe contener al menos un mayúscula,una minúscula,un número y un carácter especial, y una longitud de 8 como mínimo""",
                          font=("Lato Bold",15),
                          icon="warning"
                          )
            return
        
        
        if crear_cajero(nombre, usuario, contrasena):
            
            self.ventana_registro.destroy()
            
        else:
           CTkMessagebox(title="ATENCIÓN!!",
                          message=f"Nombre de usuario ya registado",
                          font=("Lato Bold",15),
                          icon="cancel")
        