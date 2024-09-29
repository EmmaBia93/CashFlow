import customtkinter as ctk
from PIL import Image


import customtkinter as ctk
from PIL import Image


def mostrar_ventana():
    """Muestra la ventana de inicio de sesión y controla el flujo."""
    ventana = ctk.CTk()
    ventana.title("Inicio de sesión")
    ventana.geometry("400x600+500+100")
    ventana.resizable(width=False, height=False)

    # Crear un canvas
    canvas = ctk.CTkCanvas(ventana, width=400, height=600)
    canvas.pack(fill="both", expand=True)

  

    # Cargar imagen de usuario
    imagen_usuario = ctk.CTkImage(Image.open("img/gamer.png"), size=(100, 100))
    label_imagen = ctk.CTkLabel(canvas, image=imagen_usuario, text="")
    label_imagen.place(relx=0.5, rely=0.25, anchor="center")

    # Función para cambiar el color del marco
    def on_focus_in(frame):
        frame.configure(fg_color="blue")

    def on_focus_out(frame):
        frame.configure(fg_color="#2E2E2E")  # Color por defecto

    # Campos de entrada
    frame_usuario = ctk.CTkFrame(canvas, fg_color="#2E2E2E")
    frame_contrasena = ctk.CTkFrame(canvas, fg_color="#2E2E2E")

    entry_usuario = ctk.CTkEntry(frame_usuario, 
                                       placeholder_text="Usuario", 
                                       width=300,
                                       height=40,
                                       fg_color="#181818",
                                       font=("Lato Bold", 17))

    entry_contrasena = ctk.CTkEntry(frame_contrasena, 
                                          placeholder_text="Contraseña", 
                                          show="*", 
                                          width=300,
                                          height=40,
                                          fg_color="#181818",
                                          font=("Lato Bold", 17))

    # Empaquetar entradas en sus respectivos marcos
    frame_usuario.pack(pady=10)
    entry_usuario.pack()

    frame_contrasena.pack(pady=10)
    entry_contrasena.pack()

    # Asociar eventos para cambiar el color del marco
    entry_usuario.bind("<FocusIn>", lambda e: on_focus_in(frame_usuario))
    entry_usuario.bind("<FocusOut>", lambda e: on_focus_out(frame_usuario))
    entry_contrasena.bind("<FocusIn>", lambda e: on_focus_in(frame_contrasena))
    entry_contrasena.bind("<FocusOut>", lambda e: on_focus_out(frame_contrasena))

    # Posicionar los marcos
    frame_usuario.place(relx=0.5, rely=0.5, anchor="center")
    frame_contrasena.place(relx=0.5, rely=0.6, anchor="center")
    
    ventana.mainloop()
    
mostrar_ventana()