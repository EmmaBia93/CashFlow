import customtkinter as ctk
from ttkbootstrap import Style
from ttkbootstrap.tableview import Tableview
from tkinter import messagebox
from ttkbootstrap.constants import *
import tkinter.font as tkFont
from database.manage import get_last_sesions

class VentanaTabla(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana
        self.title("Tabla de Cierre de Caja")
        self.geometry("1320x700+0+0")
        
        # # Estilo ttkbootstrap
        # self.style = Style("darkly")  
        
        # self.font_heading = tkFont.Font(family="Lato Bold", size=12, weight="bold")  
        # self.font_cell = tkFont.Font(family="Lato", size=10, weight="normal")
        
        # # Aplicar fuente personalizada a los encabezados y celdas
        # self.style.configure("Treeview.Heading", font=self.font_heading)  
        # self.style.configure("Treeview", font=self.font_cell)  

        # Crear frame para la tabla
        self.frame_tabla = ctk.CTkFrame(self)
        self.frame_tabla.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Columnas de la tabla
        self.columnas = [
            {"text": "Cajero", "stretch": True},
            {"text": "Fecha de Sesión", "stretch": True},
            {"text": "Monto Final Wisphub", "stretch": True},
            {"text": "Monto Final Caja", "stretch": True},
            {"text": "Estado", "stretch": True},
            {"text": "Observaciones", "stretch": True}
        ]
        
        # Crear tabla
        self.tabla = Tableview(
            master=self.frame_tabla,
            coldata=self.columnas,
            paginated=False,
            searchable=True,
            
        )
       
        self.tabla.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        
        # Crear frame para los botones
        self.frame_botones = ctk.CTkFrame(self)
        self.frame_botones.pack(pady=10)
        
        # Botón Traer
        self.boton_traer = ctk.CTkButton(self.frame_botones, text="Traer", command=self.traer_datos)
        self.boton_traer.pack(side="left", padx=10)
        
        # Botón Cancelar
        self.boton_cancelar = ctk.CTkButton(self.frame_botones, text="Cancelar", command=self.cancelar)
        self.boton_cancelar.pack(side="left", padx=10)
    

    def align_headings_center(self):
        """Función para alinear los encabezados de todas las columnas al centro"""
        for i in range(len(self.columnas)):
            self.tabla.align_heading_center(cid=i)

    def traer_datos(self):
        sesiones = get_last_sesions()
        for sesion in sesiones:
            print(sesion.cajero.nombre)

    def cancelar(self):
        """Función que se ejecuta al presionar el botón 'Cancelar'."""
        self.destroy()  # Cierra la ventana