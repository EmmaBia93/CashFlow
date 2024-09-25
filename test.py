import customtkinter as ctk

class MyApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Redibujar App")
        self.geometry("400x300")

        # Crear la interfaz original
        self.create_widgets()

    def create_widgets(self):
        """Función para crear los widgets iniciales"""
        # Etiqueta y entrada
        self.label = ctk.CTkLabel(self, text="Etiqueta")
        self.label.pack(pady=10)

        self.entry = ctk.CTkEntry(self)
        self.entry.pack(pady=10)

        # Botón para "redibujar" o reiniciar
        self.reset_button = ctk.CTkButton(self, text="Resetear", command=self.reset_app)
        self.reset_button.pack(pady=20)

    def reset_app(self):
        """Función para redibujar toda la interfaz desde cero"""
        # Destruir todos los widgets
        for widget in self.winfo_children():
            widget.destroy()

        # Volver a crear los widgets originales
        self.create_widgets()

# Crear la aplicación
app = MyApp()
app.mainloop()
