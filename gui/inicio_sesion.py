import sys
import customtkinter as ctk
from bcrypt import checkpw
from PIL import Image
from CTkMessagebox import CTkMessagebox
from database.manage import verificar_credenciales
from gui.main_windows import Calculadora
from tkinter import messagebox
from database.manage import crear_cajero,get_cajero,change_password
import re
from threading import Thread

class InicioSesion:
    def __init__(self):
        self.hidden_login=True
        self.hidden_reg_1=True
        self.hidden_reg_2=True
        self.hidden_recover1=True
        self.hidden_recover2=True
        self.windows_pass=None
        self.intentos_fallidos = 0
        self.error=None
        self.inicio_exitoso = False
        self.max_intentos = 3  
        self.ventana = None
        self.entry_usuario = None
        self.entry_contrasena = None
        self.ventana_registro=None
        self.close_eye = ctk.CTkImage(Image.open("img/hide.png"), size=(25, 25))
        self.eye = ctk.CTkImage(Image.open("img/vision.png"), size=(25, 25))
       




    def mostrar_ventana(self):
        """Muestra la ventana de inicio de sesión y controla el flujo."""
        self.ventana = ctk.CTk()
        self.ventana.title("Inicio de sesión")
        self.ventana.geometry("400x600+500+100")
        self.ventana.resizable(width=False,height=False)

        # Cargar imagen de usuario (asegúrate de tener una imagen llamada 'usuario.png')
        imagen_usuario = ctk.CTkImage(Image.open("img/gamer.png"), size=(100, 100))
        label_imagen = ctk.CTkLabel(self.ventana, image=imagen_usuario, text="")
        label_imagen.pack(pady=30)

        # Campos de entrada
        self.entry_usuario = ctk.CTkEntry(self.ventana, 
                                          placeholder_text="Usuario", 
                                          width=300,
                                          height=40,
                                          fg_color="#181818",
                                          font=("Lato Bold",17))
        
        self.entry_contrasena = ctk.CTkEntry(self.ventana, 
                                             placeholder_text="Contraseña", 
                                             show="*", 
                                             width=300,
                                             height=40,
                                             fg_color="#181818",
                                             font=("Lato Bold",17))

        
        
        self.entry_usuario.pack(pady=10)
        self.entry_contrasena.pack(pady=20)
        self.entry_contrasena.bind("<Return>", self.acept)
        
        
        
        self.btn_eye = ctk.CTkButton(self.ventana,
                                     image=self.close_eye,
                                     bg_color="#181818",
                                     fg_color="#181818", 
                                     hover_color="#181818",
                                     text="",width=10,height=30,
                                     command=lambda:self.visible_hidden(self.entry_contrasena,
                                                                        self.btn_eye,
                                                                        "hidden_login"))
        self.btn_eye.place(x=304,y=243)
        
        olvidar_pass = ctk.CTkLabel(self.ventana,
                                         text="Olvidé mi contraseña",
                                         text_color="#e78a21",
                                         font=("Lato Bold",13))
        olvidar_pass.place(x=220,y=285)
        olvidar_pass.bind("<Enter>", lambda e: olvidar_pass.configure(cursor="hand2"))
        olvidar_pass.bind("<Leave>", lambda e: olvidar_pass.configure(cursor=""))
        olvidar_pass.bind("<Button-1>", self.ventana_pass)
        
        # Botones
        self.btn_login = ctk.CTkButton(self.ventana, 
                                       text="Iniciar sesión", 
                                       command=self.iniciar_sesion,
                                       fg_color="#117a65",
                                       hover_color="#0b5345",
                                       border_color="#042a23",
                                       border_width=2,
                                       font=("Lato Bold",15),
                                       height=40)
        
        self.btn_login.pack(pady=70)
        self.btn_login.bind("<Return>",self.acept)
        
        registro = ctk.CTkLabel(self.ventana,
                                text="Registrarse",
                                text_color="#464c89",
                                font=("Lato Bold",15)
                                )
        registro.pack()
        registro.bind("<Enter>", lambda e: registro.configure(cursor="hand2"))
        registro.bind("<Leave>", lambda e: registro.configure(cursor=""))
        registro.bind("<Button-1>", self.abrir_ventana_registro)
        
        
        self.ventana.mainloop()
    
    
    def visible_hidden(self,entry,btn,hidden_attr_name):
        hidden = getattr(self, hidden_attr_name)
        
        if hidden:
            btn.configure(image=self.eye)
            entry.configure(show="")
            setattr(self, hidden_attr_name, False)
        else:
            btn.configure(image=self.close_eye)
            entry.configure(show="*")
            setattr(self, hidden_attr_name, True)
            
    
    def acept(self, event):
        self.btn_login.invoke()
    
    
    def abrir_ventana_registro(self,event):
        self.registro()
        

    def iniciar_sesion(self):
        """Verifica las credenciales y controla los intentos."""
        usuario = self.entry_usuario.get()
        contrasena = self.entry_contrasena.get()

        if verificar_credenciales(usuario, contrasena):
           
            self.inicio_exitoso = True
            self.ventana.destroy()
            
            Calculadora(usuario)
            
        else:
            self.intentos_fallidos += 1
            self.label_info = ctk.CTkLabel(self.ventana,
                                           text="Usuario o Contraseña Incorrecto",
                                           text_color="#ff5733",
                                           font=("Lato Bold",13))
            self.label_info.pack(side="bottom")
            
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
            self.ventana_registro.geometry("400x700+0+0")
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
            self.btn_reg1_eye = ctk.CTkButton(self.ventana_registro,
                                              image=self.close_eye,
                                              bg_color="#181818",
                                            fg_color="#181818", 
                                            hover_color="#181818",
                                            text="",width=10,height=30,
                                            command=lambda:self.visible_hidden(self.entry_ncontrasena,
                                                                        self.btn_reg1_eye,
                                                                        "hidden_reg_1"))
            self.btn_reg1_eye.place(x=304,y=314)
            
            self.entry_nconfirmar_contrasena = ctk.CTkEntry(self.ventana_registro,
                                                            placeholder_text="Confirmar Contraseña",
                                                            show="*",
                                                            width=300,
                                                            height=40,
                                                            fg_color="#181818",
                                                            font=("Lato Bold",17))
            
            self.btn_reg2_eye = ctk.CTkButton(self.ventana_registro,
                                              image=self.close_eye,
                                              bg_color="#181818",
                                            fg_color="#181818", 
                                            hover_color="#181818",
                                            text="",width=10,height=30,
                                            command=lambda:self.visible_hidden(self.entry_nconfirmar_contrasena,
                                                                        self.btn_reg2_eye,
                                                                        "hidden_reg_1"))
            self.btn_reg2_eye.place(x=304,y=374)
           

            self.entry_nnombre.pack(pady=10)
            self.entry_nusuario.pack(pady=10)
            self.entry_ncontrasena.pack(pady=10)
            self.entry_nconfirmar_contrasena.pack(pady=10)
            
            label_pregunta_seguridad = ctk.CTkLabel(self.ventana_registro, text="Pregunta de seguridad", font=("Lato Bold", 15))
            label_pregunta_seguridad.pack(pady=10)

            self.combobox_pregunta_seguridad = ctk.CTkComboBox(self.ventana_registro,
                                                            values=["Nombre de su primer hijo", 
                                                                    "Ciudad de nacimiento", 
                                                                    "Nombre de su mascota",
                                                                    "Juego Favorito",
                                                                    "Libro Favorito",
                                                                    "Película Favorita",
                                                                    "Comida favorita"],
                                                            width=300,
                                                            height=40,
                                                            font=("Lato Bold", 17),
                                                            fg_color="#181818",
                                                            button_color="#445f9b",
                                                            button_hover_color="#2f426d",
                                                            dropdown_font=("Lato Bold", 12),
                                                            dropdown_fg_color="#181818",
                                                            dropdown_hover_color="#366e9d",
                                                            )
            self.combobox_pregunta_seguridad.pack(pady=10)

            # Entry para la respuesta de la pregunta de seguridad
            self.entry_respuesta_seguridad = ctk.CTkEntry(self.ventana_registro,
                                                        placeholder_text="Respuesta de seguridad",
                                                        width=300,
                                                        height=40,
                                                        fg_color="#181818",
                                                        font=("Lato Bold", 17))
            self.entry_respuesta_seguridad.pack(pady=10)

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
            btn_registrar.pack(pady=30)
            self.ventana_registro.focus()
    
    def registrar_usuario(self):
        regex_pass = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$"
        regex_user =  r"^[a-zA-Z0-9]([._]?[a-zA-Z0-9]+)*$" 
        nombre = self.entry_nnombre.get()
        usuario = self.entry_nusuario.get()
        contrasena = self.entry_ncontrasena.get()
        confirmar_contrasena = self.entry_nconfirmar_contrasena.get()
        pregunta_seguridad = self.combobox_pregunta_seguridad.get()
        respuesta_seguridad = self.entry_respuesta_seguridad.get()
        # Validar que los campos no estén vacíos
        if not nombre or not usuario or not contrasena or not confirmar_contrasena or not respuesta_seguridad:
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
        
        
        if crear_cajero(nombre, usuario, contrasena,pregunta=pregunta_seguridad,respuesta=respuesta_seguridad):
            
            self.ventana_registro.destroy()
            
        else:
           CTkMessagebox(title="ATENCIÓN!!",
                          message=f"Nombre de usuario ya registado",
                          font=("Lato Bold",15),
                          icon="cancel")
        
        
    def ventana_pass(self,event):
        if self.windows_pass is None or not self.windows_pass.winfo_exists():
            self.windows_pass = ctk.CTkToplevel()
            self.windows_pass.title("Recuperación de contraseña")
            self.windows_pass.geometry("400x700+0+0")
            self.windows_pass.attributes("-topmost", True)
            self.windows_pass.resizable(width=False,height=False)
            lock = ctk.CTkImage(Image.open("img/unlocked.png"), size=(100, 100))
            label_imagen = ctk.CTkLabel(self.windows_pass, image=lock, text="")
            label_imagen.pack(pady=40)
            self.recovery_user = ctk.CTkEntry(self.windows_pass, 
                                          placeholder_text="Usuario", 
                                          width=300,
                                          height=40,
                                          fg_color="#181818",
                                          font=("Lato Bold",17))
            self.recovery_user.pack(pady=10)
            
            self.label_pregunta_seguridad = ctk.CTkLabel(self.windows_pass, text="Pregunta de seguridad", font=("Lato Bold", 15))
            self.label_pregunta_seguridad.pack(pady=10)

            self.combobox_rpregunta_seguridad = ctk.CTkComboBox(self.windows_pass,
                                                            values=["Nombre de su primer hijo", 
                                                                    "Ciudad de nacimiento", 
                                                                    "Nombre de su mascota",
                                                                    "Juego Favorito",
                                                                    "Libro Favorito",
                                                                    "Película Favorita",
                                                                    "Comida favorita"],
                                                            width=300,
                                                            height=40,
                                                            font=("Lato Bold", 17),
                                                            fg_color="#181818",
                                                            button_color="#445f9b",
                                                            button_hover_color="#2f426d",
                                                            dropdown_font=("Lato Bold", 12),
                                                            dropdown_fg_color="#181818",
                                                            dropdown_hover_color="#366e9d",
                                                            )
            self.combobox_rpregunta_seguridad.pack(pady=10)

            # Entry para la respuesta de la pregunta de seguridad
            self.entry_rrespuesta_seguridad = ctk.CTkEntry(self.windows_pass,
                                                        placeholder_text="Respuesta de seguridad",
                                                        width=300,
                                                        height=40,
                                                        fg_color="#181818",
                                                        font=("Lato Bold", 17))
            self.entry_rrespuesta_seguridad.pack(pady=10)

            self.btn_search = ctk.CTkButton(self.windows_pass,
                                            text="Siguiente",
                                          fg_color="#cb4335",
                                          hover_color="#943126",
                                          border_color="#641e16",
                                          border_width=2,
                                          height=40, 
                                            command=self.recovery_password,
                                            font=("Lato Bold",15))
            self.btn_search.pack(pady=30)
            
    def recovery_password(self):
        
        if self.recovery_user.get().strip() and self.entry_rrespuesta_seguridad.get().strip():
            self.cajero = get_cajero(usuario=self.recovery_user.get())
            
            if self.cajero:
                if self.combobox_rpregunta_seguridad.get() == self.cajero.pregunta_seguridad and  checkpw(self.entry_rrespuesta_seguridad.get().encode('utf-8'),self.cajero.respuesta_seguridad_hash):
                        self.recovery_user.configure(state="disabled",text_color="#545454",justify="center")
                        self.label_pregunta_seguridad.forget()
                        self.combobox_rpregunta_seguridad.forget()
                        self.entry_rrespuesta_seguridad.forget()
                        
                        if self.error != None:
                            self.error.forget()
                        self.btn_search.configure(command=self.change_password)
                        self.new_pass = ctk.CTkEntry(self.windows_pass,
                                                    placeholder_text="Nueva Contraseña", 
                                                    show="*", 
                                                    width=300,
                                                    height=40,
                                                    fg_color="#181818",
                                                    font=("Lato Bold",17))
                        self.new_pass.pack(pady=10,after=self.recovery_user)
                        self.new_conf_pass = ctk.CTkEntry(self.windows_pass,
                                                    placeholder_text="Confirmar Nueva Contraseña", 
                                                    show="*", 
                                                    width=300,
                                                    height=40,
                                                    fg_color="#181818",
                                                    font=("Lato Bold",17))
                        self.new_conf_pass.pack(pady=10,after=self.new_pass)
                        self.new_conf_pass.bind("<Return>",self.dar_click)
                else:
                    self.error = ctk.CTkLabel(self.windows_pass,
                                                text_color="#ff5733",
                                                font=("Lato Bold",13),
                                                text="Pregunta o Respuesta de seguridad incorrectas"
                                              )
                    self.error.pack(side="bottom",after=self.btn_search)
            else:
                CTkMessagebox(title="ERROR!!",
                            message=f"El Usuario no se encuentra registrado",
                            font=("Lato Bold",15),
                                icon="cancel")
        else:

            CTkMessagebox(title="ATENCIÓN",
                            message=f"Debe Completar todos los campos.",
                            font=("Lato Bold",15),
                                icon="warning")

    def change_password(self):
        contrasena = self.new_pass.get()
        confirmacion_contraseña = self.new_conf_pass.get()
        regex_pass = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$"
        

        
        
        if not re.match(regex_pass, contrasena):
            CTkMessagebox(width=400,
                          height=300,
                          title="ATENCIÓN!!",
                          message=f"""Contraseña poco segura, la contraseña debe contener al menos un mayúscula,una minúscula,un número y un carácter especial, y una longitud de 8 como mínimo""",
                          font=("Lato Bold",15),
                          icon="warning"
                          )
            return

        if contrasena != confirmacion_contraseña:
           
            CTkMessagebox(title="ERROR!!",
                          message=f"Las Contraseñas no coinciden.",
                          font=("Lato Bold",15),
                          icon="cancel")
            return
        
        if change_password(self.cajero.id,new_password=contrasena):
                CTkMessagebox(title="EXITO!!!",
                          message=f"Se Modificó la contraseña del usuario.",
                          font=("Lato Bold",15),
                          icon="check")
                self.windows_pass.destroy()
        else:
                CTkMessagebox(title="ERROR!!",
                          message=f"Ocurrio un problema al cambiar la contraseña.",
                          font=("Lato Bold",15),
                          icon="cancel")
                return
        
    def dar_click(self,event):
        self.btn_search.invoke()
