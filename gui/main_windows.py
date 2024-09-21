import customtkinter as ctk
import re
import os
from io import open
from PIL import Image
from rapidfuzz import fuzz
from CTkMessagebox import CTkMessagebox
import requests
from datetime import datetime
from dotenv import load_dotenv
from collections import Counter
from database.manage import get_cajero,save_sesion
import tkinter as tk
from tkinter import ttk

import locale
from database.manage import get_last_sesions
from CTkTable import *

class Calculadora():
    color = "#8CC65C"
    font_fira = ("Lato Bold", 22)
    font_sans_20 = ("Lato Bold", 20)
    font_sans_16 = ("Lato Bold", 16)

    def __init__(self,user:str) -> None:
        self.user=user
        self.save_ok=False
        self.lista_virtuales = []
        self.lista_wisphub = []
        self.validate_entry = lambda text: text.isdecimal()
        self.tabletix=None
        self.master = ctk.CTk(fg_color="#1a1a1a")
            
        self.master.geometry(f"1320x700+12+0")
        self.total_wisphub=self.obtener_total_wisphub()


            # self.master.iconbitmap("C:\\Users\\PC\\Documents\\repositorio\\FindeCaja\\img\\cash.ico")
            # self.master.update()

        self.master.title("Cierre de Caja")
            
        self.master.resizable(width=False, height=False)
            
        self.colocar_frames()
        self.colocar_widgets_framedown()
        self.colocar_widgets_frameup()
        self.colocal_widgets_frameright()

        self.master.mainloop()
        

    def obtener_total_wisphub(self):
        load_dotenv()
        url = os.getenv("URL_FACTURAS")
        fecha_actual = datetime.now()

        
        fecha_formateada = fecha_actual.strftime('%Y-%m-%d')
        headers = {'Authorization': os.getenv("API")}

        params = {
                    'fecha_pago__range_0':fecha_formateada,
                    'fecha_pago__range_1':fecha_formateada,
                    'estado': 2,
                    'limit': 300,
                    'offset':0
                }
        
        results=[]
        total_cobrado=0
     
        while True:
                                
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                results.extend(data.get('results', []))
                
                if not len(results)==300:
                    break
                    
                params['offset']+=300
                 
            else:
                results=[]


        if results:
            for result in results:
               total_cobrado+=int(result.get('total_cobrado',0))
            return total_cobrado
        else:
            return total_cobrado
    

    def colocar_frames(self):
        
        self.frame_up = ctk.CTkFrame(
            self.master,
            width=430,
            height=400,
            border_color="#2E86C1",
            border_width=2
            )
        self.frame_up.place(x=10, y=10)

        self.frame_down = ctk.CTkFrame(
            self.master,
            width=430,
            height=270,
            border_color="#2E86C1",
            border_width=2)
        self.frame_down.place(x=10, y=420)

        self.frame_right = ctk.CTkFrame(
            self.master,
            width=860,
            height=680,
            border_color="#2E86C1",
            border_width=2)
        self.frame_right.place(x=450, y=10)



    def refresh_entry(self,entry:ctk.CTkEntry):
        entry.delete(first_index="0", last_index=ctk.END)
        entry.insert(0,f"{self.obtener_total_wisphub()}")

    def colocar_widgets_frameup(self):
        
        ancho = 300
        alto = 30
        posx = 0.17
        color_text = "#dedede"
        
        self.txt_wisphub = ctk.CTkEntry(master=self.frame_up,
                                        width=335,
                                        height=42,
                                        fg_color="#232323",
                                        border_width=3,
                                        text_color="#dedede",
                                        placeholder_text="Final Wisphub",
                                        placeholder_text_color="#616A6B",
                                        border_color="#3D91CB",
                                        font=("Lato Bold", 22),
                                        justify="center")
        
        
        self.txt_wisphub.place(relx=0.05, rely=0.035)
        
        if self.total_wisphub:
            self.txt_wisphub.insert(0,f"{self.total_wisphub}")


        img_refresh = ctk.CTkImage(dark_image=Image.open("img/refresh.png"),
                            size=(40, 40))
        
        self.btn_refresh = ctk.CTkButton(
                            master=self.frame_up,
                            width=40,
                            height=40,
                            text="",
                            fg_color="#2b2b2b", 
                            hover_color="#2b2b2b",        
                            border_width=0,    
                            bg_color="transparent",  
                            image=img_refresh,
                            command=lambda:self.refresh_entry(self.txt_wisphub)  
                        )
        
        self.btn_refresh.place(relx=0.84,rely=0.028)


        billetes = [
            ("Billetes de 100", "txt_billete100"),
            ("Billetes de 200", "txt_billete200"),
            ("Billetes de 500", "txt_billete500"),
            ("Billetes de 1000", "txt_billete1000"),
            ("Billetes de 2000", "txt_billete2000"),
            ("Billetes de 10000", "txt_billetediezmil")
        ]

        for i, (label_text, attr_name) in enumerate(billetes):
            y_label = 0.14 + 0.14 * i
            y_entry = 0.20 + 0.14 * i

            label = self.crear_label(self.frame_up, label_text, font=self.font_sans_16)
            label.place(relx=posx, rely=y_label)

            entry = self.crear_entry(frame=self.frame_up, ancho=ancho, alto=alto,
                                    color="#138d75", font=self.font_sans_20,
                                    validacion=False)
            entry.place(relx=0.15, rely=y_entry)
            entry.configure(text_color=color_text)

            setattr(self, attr_name, entry)

        bindings = [
            (self.txt_wisphub, self.txt_billetediezmil, self.txt_billete100),
            (self.txt_billete100, self.txt_wisphub, self.txt_billete200),
            (self.txt_billete200, self.txt_billete100, self.txt_billete500),
            (self.txt_billete500, self.txt_billete200, self.txt_billete1000),
            (self.txt_billete1000, self.txt_billete500, self.txt_billete2000),
            (self.txt_billete2000, self.txt_billete1000, self.txt_billetediezmil),
            (self.txt_billetediezmil, self.txt_billete2000, self.txt_wisphub)
        ]

        for entry, entry_up, entry_down in bindings:
            entry.bind("<Up>", lambda event, entry_next=entry_up: self.mover_cursor(entry_next))
            entry.bind("<Down>", lambda event, entry_next=entry_down: self.mover_cursor(entry_next))
            entry.bind("<Return>", lambda event, entry_next=entry_down: self.mover_cursor(entry_next))

        self.txt_billetediezmil.bind("<Return>", self.enterfinal)

    def mover_cursor(self, entry_next: ctk.CTkEntry):
        entry_next.focus_set()

    def crear_entry(self, frame, ancho: int, alto: int, color: str, font, validacion=True, place_holder="") -> ctk.CTkEntry:

        if validacion:

            prototipe_entry = ctk.CTkEntry(frame,
                                           width=ancho,
                                           height=alto,
                                           justify="center",
                                           bg_color="transparent",
                                           placeholder_text_color="#616A6B",
                                           font=font,
                                           border_color=color,
                                           fg_color="#232323",
                                           placeholder_text=place_holder,


                                           )
        else:
            prototipe_entry = ctk.CTkEntry(frame,
                                           width=ancho,
                                           height=alto,
                                           justify="center",
                                           placeholder_text_color="#616A6B",
                                           font=font,
                                           border_color=color,
                                           fg_color="#232323",
                                           validate="key",
                                           validatecommand=(self.master.register(
                                               self.validate_entry), "%S"),
                                           placeholder_text=place_holder
                                           )

        return prototipe_entry

    def crear_label(self, frame, text, font):
        prototipe_label = ctk.CTkLabel(
            frame,
            text=text,
            font=font,
            text_color="#8f8f8f")

        return prototipe_label

    def borrar_contenido_resultados(self):
        
        widgets = [
        self.txt_cantidad_virtuales,
        self.txt_monto_virtuales,
        self.cant_efectivo,
        self.total
        ]

        for widget in widgets:
            widget.configure(state="normal")
            widget.delete(first_index="0", last_index=ctk.END)
            widget.configure(state="disabled")

    
    def colocar_valores_txt(self, text_box, valor,cash):
        text_box.configure(state="normal")
        if cash:
            text_box.insert(index=ctk.END, string=f"${valor}")
        else:
            text_box.insert(index=ctk.END, string=valor)
        text_box.configure(state="disabled")


    def final_monto_virtuales(self) -> tuple:
        
        if not self.lista_virtuales:
            return 0, 0

        # Filtra y convierte las líneas a enteros
        numeros = [
            int(re.sub(r'[^0-9]', '', line))
            for line in self.lista_virtuales
            if re.sub(r'[^0-9]', '', line).isdigit()
        ]

        monto = sum(numeros)
        cant = len(numeros)

        return monto, cant


    def verificar_estado_final(self):

        if self.total.get() and self.txt_wisphub.get():
            wisphub = re.sub(r'[^0-9\[\]]', '', self.txt_wisphub.get().strip())
            total = self.monto_efectivo + self.monto_virtuales
            resultado = int(wisphub) - int(total)

                      
            self.et_resultado.place_forget()
            self.et_falta.place_forget()
            self.entry_falta.place_forget()
            self.entry_sobra.place_forget()
            self.et_sobra.place_forget()

            if resultado == 0:
                self.et_resultado.place(relx=0.3, rely=0.80)
                self.frame_down.configure(border_color="#27AE60")
                self.frame_right.configure(border_color="#27AE60")
                self.frame_up.configure(border_color="#27AE60")
            elif resultado < 0:
                self.et_sobra.place(relx=0.32, rely=0.73)
                self.entry_sobra.place(relx=0.3, rely=0.82)
                self.entry_sobra.configure(state="normal")
                self.entry_sobra.delete(first_index=0, last_index=ctk.END)
                self.entry_sobra.insert(index=ctk.END, string=str(abs(resultado)))
                self.entry_sobra.configure(state="disabled")
                self.frame_down.configure(border_color="#f1c40f")
                self.frame_right.configure(border_color="#f1c40f")
                self.frame_up.configure(border_color="#f1c40f")
            else:  # resultado > 0
                self.et_falta.place(relx=0.32, rely=0.73)
                self.entry_falta.place(relx=0.3, rely=0.82)
                self.entry_falta.configure(state="normal")
                self.entry_falta.delete(first_index=0, last_index=ctk.END)
                self.entry_falta.insert(index=ctk.END, string=str(abs(resultado)))
                self.entry_falta.configure(state="disabled")
                self.frame_down.configure(border_color="#e74c3c")
                self.frame_right.configure(border_color="#e74c3c")
                self.frame_up.configure(border_color="#e74c3c")

    def realizar_calculos(self):
        self.save_ok=True
        self.borrar_contenido_resultados()
        final_100 = int(self.txt_billete100.get()
                        ) if self.txt_billete100.get().isdigit() else 0
        final_200 = int(self.txt_billete200.get()
                        ) if self.txt_billete200.get().isdigit() else 0
        final_500 = int(self.txt_billete500.get()
                        ) if self.txt_billete500.get().isdigit() else 0
        final_1000 = int(self.txt_billete1000.get()
                         ) if self.txt_billete1000.get().isdigit() else 0
        final_2000 = int(self.txt_billete2000.get()
                         ) if self.txt_billete2000.get().isdigit() else 0
        final_diezmil = int(self.txt_billetediezmil.get()
                            ) if self.txt_billetediezmil.get().isdigit() else 0

        self.monto_efectivo = final_100*100+final_200*200 + \
            final_500*500+final_1000*1000+final_2000*2000 + final_diezmil*10000
        self.monto_virtuales, cant_virtuales = self.final_monto_virtuales()

        self.colocar_valores_txt(self.txt_cantidad_virtuales, cant_virtuales,False)
        self.colocar_valores_txt(
            self.txt_monto_virtuales, self.monto_virtuales,True)
        self.colocar_valores_txt(self.cant_efectivo, self.monto_efectivo,True)
        self.colocar_valores_txt(
            self.total, (self.monto_efectivo+self.monto_virtuales),True)
        self.verificar_estado_final()

    def colocar_widgets_framedown(self):
       
        color_border ="#0e6655"
        img3 = ctk.CTkImage(dark_image=Image.open("img/cashier.png"),
                            size=(30, 30))
        self.btn_resultado = ctk.CTkButton(self.frame_down,
                                           text="Finalizar Caja",
                                           width=170,
                                           font=self.font_sans_20,
                                           anchor="center",
                                           border_color="#154360",
                                           border_width=3,
                                           text_color="#282828",
                                           fg_color="#2980b9",
                                           hover_color="#1f618d",
                                           corner_radius=10,
                                           image=img3,
                                           command=self.realizar_calculos)

        self.btn_resultado.place(relx=0.3, rely=0.05)

        img_save = ctk.CTkImage(dark_image=Image.open("img/save.png"),
                            size=(30, 30))
        self.btn_save = ctk.CTkButton(
                            master=self.frame_down,
                            width=40,
                            height=40,
                            text="",
                            fg_color="#2b2b2b", 
                            hover_color="#2b2b2b",        
                            border_width=0,    
                            bg_color="transparent",  
                            image=img_save,
                            command=self.save_info  
                        )
        self.btn_save.place(relx=0.06, rely=0.05)


        img_recover = ctk.CTkImage(dark_image=Image.open("img/recover.png"), size=(30, 30))
        self.btn_recover =  ctk.CTkButton(
                            master=self.frame_down,
                            width=40,
                            height=40,
                            text="",
                            fg_color="#2b2b2b", 
                            hover_color="#2b2b2b",        
                            border_width=0,    
                            bg_color="transparent",  
                            image=img_recover,
                            command=self.recover  
                        )
        self.btn_recover.place(relx=0.82, rely=0.05)

        font_label = ("Lato Bold", 14)
        et_monto_virtuales = self.crear_label(
            frame=self.frame_down,
            text="Monto Virtuales",
            font=font_label)
        et_monto_virtuales.place(relx=0.06, rely=0.24)
        self.txt_monto_virtuales = self.crear_entry(
            frame=self.frame_down,
            ancho=150, alto=20,
            color=color_border,
            font=self.font_sans_16)
        self.txt_monto_virtuales.place(relx=0.05, rely=0.33)
        self.txt_monto_virtuales.configure(
            state="disabled", text_color="#dedede")

        et_cantidad_virtuales = self.crear_label(
            frame=self.frame_down,
            text="Cant Virtuales",
            font=font_label)
        et_cantidad_virtuales.place(relx=0.61, rely=0.24)
        self.txt_cantidad_virtuales = self.crear_entry(
            frame=self.frame_down,
            ancho=150, alto=26,
            color=color_border,
            font=font_label)
        self.txt_cantidad_virtuales.configure(
            state="disabled", text_color="#dedede")
        self.txt_cantidad_virtuales.place(relx=0.6, rely=0.33)

        et_cant_efectivo = self.crear_label(frame=self.frame_down,
                                            text="Monto Efectivo",
                                            font=font_label)
        et_cant_efectivo.place(relx=0.06, rely=0.51)
        self.cant_efectivo = self.crear_entry(frame=self.frame_down,
                                              ancho=150, alto=20,
                                              color=color_border,
                                              font=self.font_sans_16)
        self.cant_efectivo.place(relx=0.05, rely=0.60)
        self.cant_efectivo.configure(state="disabled", text_color="#dedede")

        et_total = self.crear_label(self.frame_down,
                                    "Monto Total",
                                    font_label)
        et_total.place(relx=0.61, rely=0.51)

        self.total = self.crear_entry(frame=self.frame_down,
                                      ancho=150, alto=20,
                                      color=color_border,
                                      font=self.font_sans_16)
        self.total.place(relx=0.6, rely=0.60)
        self.total.configure(state="disabled", text_color="#dedede")

        self.et_resultado = ctk.CTkEntry(self.frame_down, corner_radius=10, border_color="#27AE60", border_width=3,
                                         justify="center", text_color="#27AE60", width=170, height=40, font=self.font_sans_20)
        self.et_resultado.insert(index=ctk.END, string="Caja Correcta")
        self.et_sobra = ctk.CTkLabel(
            self.frame_down, text="Sobra", text_color="#f1c40f", font=("Berlin Sans FB", 20))
        self.entry_sobra = ctk.CTkEntry(self.frame_down, corner_radius=10, border_color="#f1c40f", border_width=3,
                                        justify="center", text_color="#f1c40f", width=170, height=40, font=self.font_sans_20)
        self.et_falta = ctk.CTkLabel(
            self.frame_down, text="Falta", text_color="#e74c3c", font=("Berlin Sans FB", 20))
        self.entry_falta = ctk.CTkEntry(self.frame_down, corner_radius=10, border_color="#e74c3c", border_width=3,
                                        justify="center", text_color="#e74c3c", width=170, height=40, font=self.font_sans_20)

    def enterfinal(self, event):
        self.btn_resultado.invoke()

    def colocal_widgets_frameright(self):

        self.entry_busqueda = ctk.CTkEntry(master=self.frame_right,
                                           width=760,
                                           height=45,
                                           justify="center",
                                           border_color="#3D91CB",
                                           border_width=3,
                                           text_color="#5DADE2",
                                           font=("Lato Bold",24),
                                           fg_color="#232323",
                                           placeholder_text="Búsqueda...",
                                           placeholder_text_color="#616A6B"
                                           )

        self.entry_busqueda.place(relx=0.06, rely=0.02)
        self.entry_busqueda.bind("<KeyRelease>", self.realizar_busqueda)

        self.txt_resultado_wisphub = ctk.CTkTextbox(master=self.frame_right,
                                                    border_color="#138d75",
                                                    border_width=3,
                                                    fg_color="#232323",
                                                    width=405, height=500,
                                                    font=self.font_sans_20,
                                                    )
        self.txt_resultado_wisphub.place(relx=0.02, rely=0.11)
        self.txt_resultado_wisphub.configure(
            state="disabled", text_color="#dedede")

        self.txt_resultado_virtuales = ctk.CTkTextbox(master=self.frame_right,
                                                      border_color="#138d75",
                                                      border_width=3,
                                                      fg_color="#232323",
                                                      width=405, height=500,
                                                      font=self.font_sans_20,
                                                      )
        self.txt_resultado_virtuales.place(relx=0.51, rely=0.11)
        self.txt_resultado_virtuales.configure(
            state="disabled", text_color="#dedede")

       

        img = ctk.CTkImage(dark_image=Image.open("img/upload.png"), size=(30, 30))

        self.btn_cargar_csv = ctk.CTkButton(master=self.frame_right,
                                            text="Cargar Wisphub",
                                            font=self.font_sans_20,
                                            width=200,
                                            height=45,
                                            border_color="#154360",
                                            border_width=3,
                                            text_color="#282828",
                                            fg_color="#2980b9",
                                            hover_color="#1f618d",
                                            corner_radius=10,
                                            image=img,
                                            command=self.cargar_csv)
        self.btn_cargar_csv.place(relx=0.12, rely=0.92)

        self.toplevel_window = None

        self.btn_virtuales = ctk.CTkButton(master=self.frame_right,
                                           text="Cargar Virtuales",
                                           font=self.font_sans_20,
                                           width=200,
                                           height=45,
                                           border_color="#154360",
                                           border_width=3,
                                           text_color="#282828",
                                           fg_color="#2980b9",
                                           hover_color="#1f618d",
                                           corner_radius=10,
                                           image=img,
                                           command=lambda: self.windows_virtuales())

        self.btn_virtuales.place(relx=0.64, rely=0.92)

        self.btn_diferencia = ctk.CTkButton(master=self.frame_right, text="◀ Diferencias ▶",
                                            font=self.font_sans_20,
                                            width=200,
                                            height=45,
                                            text_color="#282828",
                                            fg_color="#4664E1",
                                            hover_color="#334AA4",
                                            corner_radius=10,
                                            border_color="#1F2C61",
                                            border_width=3,
                                            command=self.encontrar_diferencia)

        self.btn_diferencia.place(relx=0.39, rely=0.86)

        self.en_wisphub = ctk.CTkEntry(self.frame_right,
                                       width=65,
                                       fg_color="#232323",
                                       height=35,
                                       justify="center",
                                       font=self.font_sans_20,
                                       corner_radius=10,
                                       border_color="#138d75",
                                       border_width=3,
                                       text_color="#B3B6B7",
                                       bg_color="transparent")

        self.en_wisphub.place(relx=0.22, rely=0.82)

        self.en_wisphub.configure(state="disabled")

        self.en_virtuales = ctk.CTkEntry(self.frame_right,
                                         width=65,
                                         fg_color="#232323",
                                         height=35,
                                         justify="center",
                                         font=self.font_sans_20,
                                         corner_radius=10,
                                         border_color="#138d75",
                                         border_width=3,
                                         text_color="#B3B6B7",
                                         bg_color="transparent")

        self.en_virtuales.place(relx=0.707, rely=0.82)

        self.en_virtuales.configure(state="disabled")

        self.lb_max_importe_virt = ctk.CTkLabel(
            self.frame_right,
            text="Importe Máximo $5000",
            font=("Lato Bold", 12),
            bg_color="transparent",
            text_color="#ff5733")

        self.lb_min_importe_virt = ctk.CTkLabel(
            self.frame_right,
            font=("Lato Bold", 12),
            bg_color="transparent",
            fg_color=None,
            text_color="#ff5733")

        self.lb_max_importe_wisp = ctk.CTkLabel(
            self.frame_right,
            text="Importe Máximo $5000",
            font=("Lato Bold", 12),
            bg_color="transparent",
            text_color="#ff5733")

        self.lb_min_importe_wisp = ctk.CTkLabel(
            self.frame_right,
            font=("Lato Bold", 12),
            bg_color="transparent",
            fg_color=None,
            text_color="#ff5733")
        

    def buscar_coincidencias(self, nombre_completo, input_usuario):
        nombre_completo = nombre_completo.lower()
        input_usuario = input_usuario.lower()
        palabras_input = input_usuario.split()
        return all(palabra in nombre_completo for palabra in palabras_input)

    def realizar_busqueda(self, *args):
        txt_busqueda = self.entry_busqueda.get().strip()
        request_virtuales = ""
        request_wisphub = ""
        cont_virtuales = 0
        cont_wisphub = 0

        self.txt_resultado_virtuales.configure(state="normal")
        self.txt_resultado_wisphub.configure(state="normal")

        self.txt_resultado_virtuales.delete(index1="0.0", index2=ctk.END)
        self.txt_resultado_wisphub.delete(index1="0.0", index2=ctk.END)

        if txt_busqueda:  # Si hay texto de búsqueda
            busqueda_title = txt_busqueda.title()

            # Buscar coincidencias en lista_virtuales
            for line in self.lista_virtuales:
                if self.buscar_coincidencias(line, busqueda_title):
                    request_virtuales += f"{line.strip()}\n"
                    cont_virtuales += 1

            # Buscar coincidencias en lista_wisphub
            for line in self.lista_wisphub:
                if self.buscar_coincidencias(line, busqueda_title):
                    request_wisphub += f"{line.strip()}\n"
                    cont_wisphub += 1

            # Actualizar contadores
            self.actualizar_contador(self.en_virtuales, cont_virtuales)
            self.actualizar_contador(self.en_wisphub, cont_wisphub)

            # Insertar resultados en los cuadros de texto
            self.insertar_resultados(self.txt_resultado_virtuales, request_virtuales, cont_virtuales)
            self.insertar_resultados(self.txt_resultado_wisphub, request_wisphub, cont_wisphub)

        else:  # Si no hay búsqueda, mostrar el total
            self.actualizar_contador(self.en_virtuales, len(self.lista_virtuales))
            self.actualizar_contador(self.en_wisphub, len(self.lista_wisphub))

        self.txt_resultado_virtuales.configure(state="disabled")
        self.txt_resultado_wisphub.configure(state="disabled")

    def actualizar_contador(self, widget, valor):
        widget.configure(state="normal")
        widget.delete(first_index="0", last_index=ctk.END)
        widget.insert(index=ctk.END, string=str(valor))
        widget.configure(state="disabled")

    def insertar_resultados(self, widget, texto, contador):
        if texto:
            widget.insert(ctk.END, texto)
        else:
            widget.tag_config("oneline", foreground="#EC7063")
            widget.insert(ctk.END, "\n\n\t          (ಥ﹏ಥ)\n    No se han encontrado coincidencias", "oneline")

    def windows_virtuales(self):

        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ctk.CTkToplevel(self.master)
            
            self.toplevel_window.geometry("700x700+300+0")
            self.toplevel_window.title("Carga de Virtuales")
            self.toplevel_window.resizable(width=False, height=False)
            # self.toplevel_window.iconbitmap("C:\\Users\\PC\\Documents\\repositorio\\FindeCaja\\img\\cash.ico")
            # self.toplevel_window.update()
            self.txt_box_virtules = ctk.CTkTextbox(self.toplevel_window,
                                                   width=680,
                                                   height=600,
                                                   font=("Lato Bold", 17),
                                                   fg_color="#202020",
                                                   corner_radius=10,
                                                   border_color="#1f618d",
                                                   border_width=3)
            self.txt_box_virtules.place(x=10, y=10)

            self.toplevel_window.attributes("-topmost", True)

            if self.lista_virtuales:
                lista = ""
                self.txt_box_virtules.delete(index1="0.0", index2=ctk.END)
                for line in self.lista_virtuales:
                    lista += f"{line}\n"
                self.txt_box_virtules.insert(ctk.END, lista)

         
            img = ctk.CTkImage(dark_image=Image.open("img/up.png"), size=(30, 30))
            btn_carga_virtuales = ctk.CTkButton(self.toplevel_window,
                                                height=50,
                                                width=200,
                                                text="Cargar Virtuales",
                                                anchor="center",
                                                border_color="#154360",
                                                border_width=3,
                                                text_color="#282828",
                                                fg_color="#2980b9",
                                                hover_color="#1f618d",
                                                corner_radius=10,
                                                image=img,
                                                font=self.font_sans_20,
                                                command=self.carga_virtuales)
            btn_carga_virtuales.place(relx=0.3, y=630)

        else:

            self.toplevel_window.focus_set()

    def carga_virtuales(self,recovery=None):
        max_importe: int = 0
        min_importe: int = 10000000
        if not recovery:
            lista = self.txt_box_virtules.get("1.0", "end")
        else:
            lista = recovery
        self.lista_virtuales.clear()
        lista_txt = []
        lista_txt = lista.split("\n")
        lista_txt = [x for x in lista_txt if x.strip()]
        regex_patron = r':\s*([^:]+)\s*:\s*([^:\[]+)'
        
        
        
        for line in lista_txt:
            request_match = re.search(regex_patron, line)
            
            if request_match:
                line = request_match.group(2).strip()
                          
           
            is_digit = re.sub(r'[^0-9\[\]]', '', line).strip()
            if is_digit.isdigit():
                    valor = int(is_digit)
                    if valor > max_importe:
                        max_importe = valor
                    if valor < min_importe:
                        min_importe = valor
                    self.lista_virtuales.append(str.title(line))

            

          

        self.en_virtuales.configure(state="normal")
        self.en_virtuales.delete(first_index="0", last_index=ctk.END)
        self.en_virtuales.insert(
            index=ctk.END, string=str(len(self.lista_virtuales)))
        self.en_virtuales.configure(state="disabled")

        if min_importe != 10000000 and max_importe != 0:
           
            self.lb_max_importe_virt.configure(
                text=f"Importe Máximo ${max_importe}")
            self.lb_min_importe_virt.configure(
                text=f"Importe Mínimo ${min_importe}")
            self.lb_max_importe_virt.place(relx=0.8, rely=0.845)
            self.lb_min_importe_virt.place(relx=0.8, rely=0.88)
        else:
            self.lb_max_importe_virt.place_forget()
            self.lb_min_importe_virt.place_forget()
        if not recovery:
            self.toplevel_window.destroy()

    def cargar_csv(self):
        load_dotenv()  # Cargar variables de entorno
        self.lista_wisphub.clear()  # Limpiar la lista
        max_importe = 0
        min_importe = 100000
        url = os.getenv("URL_FACTURAS")
        fecha_actual = datetime.now()

        fecha_formateada = fecha_actual.strftime('%Y-%m-%d')

        headers = {
            'Authorization': os.getenv("API")
        }

        params = {
            'fecha_pago__range_0': fecha_formateada,
            'fecha_pago__range_1': fecha_formateada,
            'estado': 2,
            'limit': 300,
            'offset': 0
        }
        
        results = []

        while True:
            response = requests.get(url, headers=headers, params=params)

            if response.status_code == 200:
                data = response.json()
                page_results = data.get('results', [])

                results.extend(page_results)

                # Si hay menos de 300 resultados, no se requiere más paginación
                if len(page_results) < 300:
                    break

                # Incrementar el offset
                params['offset'] += 300

            else:
                print(f"Error al obtener los datos: {response.status_code}")
                results = []  # Vaciar la lista si hay error
                break

        # Procesar los resultados
        for result in results:
            if result['forma_pago']['nombre'] == 'Trasnferencia Bancaria':
                cliente_nombre = result['cliente']['nombre'].replace('FW ', '').replace('CARP ', '').strip().title()
                total_cobrado = result['total_cobrado']
                txt_auxiliar = f"{cliente_nombre} {total_cobrado:.0f}"
                
                valor = int(total_cobrado)
                if valor > max_importe:
                    max_importe = valor
                if valor < min_importe:
                    min_importe = valor
                
                self.lista_wisphub.append(txt_auxiliar)

        # Actualizar la interfaz gráfica con los valores obtenidos
        if min_importe != 100000 and max_importe > 0:
            self.lb_max_importe_wisp.configure(text=f"Importe Máximo ${max_importe}")
            self.lb_min_importe_wisp.configure(text=f"Importe Mínimo ${min_importe}")
            self.lb_min_importe_wisp.place(relx=0.035, rely=0.88)
            self.lb_max_importe_wisp.place(relx=0.035, rely=0.845)

            # Actualizar el campo de cantidad de resultados
            self.en_wisphub.configure(state="normal")
            self.en_wisphub.delete(first_index="0", last_index=ctk.END)
            self.en_wisphub.insert(index=ctk.END, string=str(len(self.lista_wisphub)))
            self.en_wisphub.configure(state="disabled")
               
            

    def mostrar_contenido_diferencias(self, contenido_virtuales, contenido_wisphub):
        
        request_virtuales = "\n".join(contenido_virtuales)
        request_wisphub = "\n".join(contenido_wisphub)

        self.txt_resultado_virtuales.configure(state="normal")
        self.txt_resultado_virtuales.delete(index1="0.0", index2=ctk.END)
        self.txt_resultado_virtuales.insert(ctk.END, request_virtuales)
        self.txt_resultado_virtuales.configure(state="disabled")

        self.txt_resultado_wisphub.configure(state="normal")
        self.txt_resultado_wisphub.delete(index1="0.0", index2=ctk.END)
        self.txt_resultado_wisphub.insert(ctk.END, request_wisphub)
        self.txt_resultado_wisphub.configure(state="disabled")

    def encontrar_diferencia(self):

        
        bool_wisphub = (self.txt_resultado_wisphub.get(index1="0.0", index2=ctk.END).strip() == "" or 
                    self.txt_resultado_wisphub.get(index1="0.0", index2=ctk.END).__contains__("(ಥ﹏ಥ)"))
        bool_virtuales = (self.txt_resultado_virtuales.get(index1="0.0", index2=ctk.END).strip() == "" or 
                        self.txt_resultado_virtuales.get(index1="0.0", index2=ctk.END).__contains__("(ಥ﹏ಥ)"))

        if not bool_wisphub and not bool_virtuales:
            contenido_virtuales = self.txt_resultado_virtuales.get(index1="0.0", index2=ctk.END).strip().splitlines()
            contenido_wisphub = self.txt_resultado_wisphub.get(index1="0.0", index2=ctk.END).strip().splitlines()

            if len(contenido_virtuales) > 1 or len(contenido_wisphub) > 1:
                if contenido_virtuales and contenido_wisphub:
                    contenido_virtuales.sort()
                    contenido_wisphub.sort()

                    op = [95, 90, 85, 80, 75, 70, 65, 60, 55, 50, 45, 40, 35, 30]
                    index = 0

                    while index < len(op) and op[index] >= 45:
                        matches_virtuales = set()
                        matches_wisphub = set()

                        for wisphub in contenido_wisphub:
                            for virtual in contenido_virtuales:
                                aux_w = re.sub(r'[0-9]+', '', wisphub).strip()
                                aux_v = re.sub(r'[0-9]+', '', virtual).strip()

                                if fuzz.ratio(aux_w, aux_v) > op[index]:
                                    matches_virtuales.add(virtual)
                                    matches_wisphub.add(wisphub)

                        # Remover elementos después de finalizar la iteración
                        contenido_virtuales = [v for v in contenido_virtuales if v not in matches_virtuales]
                        contenido_wisphub = [w for w in contenido_wisphub if w not in matches_wisphub]

                        index += 1
                 
                if len(contenido_virtuales) == 0 and len(contenido_wisphub) == 0:
                    CTkMessagebox(master=self.master, title="Resultado", message="Ambas Listas Son Idénticas.",
                                  icon="check", justify="center", font=self.font_sans_20, icon_size=(40, 40))
                else:
                    self.mostrar_contenido_diferencias(
                        contenido_virtuales, contenido_wisphub)
            else:
                CTkMessagebox(master=self.master, title="ATENCIÓN!!", message="Nada para Comparar!!!",
                              icon="warning", justify="center", font=self.font_sans_20, icon_size=(40, 40))
        else:
            CTkMessagebox(master=self.master, title="ATENCIÓN!!", message="Nada para Comparar!!!",
                          icon="warning", justify="center", font=self.font_sans_20, icon_size=(40, 40))

    def save_info(self):
        if self.save_ok:
            monto_wisp=self.txt_wisphub.get()
            total = re.sub(r'\$', '',self.total.get())
            
            billetes = [{'denominacion':100,'cantidad':self.txt_billete100.get() if self.txt_billete100.get() else 0 },
                        {'denominacion':200,'cantidad':self.txt_billete200.get() if self.txt_billete200.get() else 0 },
                        {'denominacion':500,'cantidad':self.txt_billete500.get() if self.txt_billete500.get() else 0 },
                        {'denominacion':1000,'cantidad':self.txt_billete1000.get() if self.txt_billete1000.get() else 0 },
                        {'denominacion':2000,'cantidad':self.txt_billete2000.get() if self.txt_billete2000.get() else 0 },
                        {'denominacion':10000,'cantidad':self.txt_billetediezmil.get() if self.txt_billetediezmil.get() else 0 },]
            transferencias =[]

            for line in self.lista_virtuales:
                transfer = {'nombre':re.sub(r'\d', '', line).strip(),'importe': re.sub(r'[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ]', '', line).strip()}
                transferencias.append(transfer)
            cajero= get_cajero(self.user)
        
            save_sesion(cajero_id=int(cajero.id),total_wisp=float(monto_wisp),total_sesion=float(total),transferencias=transferencias,billetes=billetes,observaciones="No Falta nada")



    def recover(self):
       
       
        self.windows_recover()
       
        
    def windows_recover(self):
        self.windows_table=ctk.CTkToplevel()
        self.sesiones=None
        self.select_row=0
        
        # Configuración de la ventana
        self.windows_table.title("Sesiones de Cierre de Caja")
        self.windows_table.geometry("1320x700+0+0")
        self.windows_table.attributes("-topmost", True)
        ctk.set_appearance_mode("dark")



        self.estilos = ttk.Style()
        self.estilos.theme_use("alt")

        # Fondo de la tabla y líneas
        self.estilos.configure("Treeview",
                             background="#2b2b2b",  # Fondo oscuro
                             foreground="white",    # Texto blanco
                             rowheight=25,          # Altura de cada fila
                             fieldbackground="#2b2b2b",  # Fondo de las celdas
                             )


        

        # Estilo de los encabezados
        self.estilos.configure("Treeview.Heading",
                             background="#138d75",  # Fondo verde oscuro
                             foreground="white",    # Texto blanco
                             font=("Lato", 15, "bold"),  # Fuente de los encabezados
                            )
        
                             
        # Color cuando se selecciona una fila
        self.estilos.map("Treeview",
                       background=[("selected", "#3D91CB")],  # Fondo al seleccionar
                       foreground=[("selected", "white")])    # Texto al seleccionar



        # Crear frame para la tabla
        self.tabla = ttk.Treeview(self.windows_table, columns=("Cajero", "Fecha de Sesión", "Monto Final Wisphub", "Monto Final Caja", "Estado", "Observaciones"), show='headings')
        
        # Configurar las columnas
        for col in self.tabla["columns"]:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, anchor="center")

        # Agregar scrollbars
        self.scroll_y = ttk.Scrollbar(self.tabla, orient="vertical", command=self.tabla.yview)
        self.scroll_y.pack(side='right', fill='y')
        self.tabla.configure(yscrollcommand=self.scroll_y.set)

        self.scroll_x = ttk.Scrollbar(self.tabla, orient="horizontal", command=self.tabla.xview)
        self.scroll_x.pack(side='bottom', fill='x')
        self.tabla.configure(xscrollcommand=self.scroll_x.set)

        self.tabla.pack(expand=True, fill="both")

        # Cargar datos en la tabla
        self.traer_datos()
        # Crear frame para los botones
        self.frame_botones = ctk.CTkFrame(self.windows_table,height=150)
        self.frame_botones.pack(pady=30)


        separator = ttk.Separator(self.windows_table, orient='horizontal')
        separator.pack(fill='x')
        # Botón Traer
        self.boton_traer = ctk.CTkButton(self.frame_botones,
                                            text="Traer",
                                            command=self.reconstruir,
                                            bg_color="#58a151",
                                            border_color="#356031",
                                            height=50
                                            )
        self.boton_traer.pack(side="left", padx=30,pady=20)

        # Botón Cancelar
        self.boton_cancelar = ctk.CTkButton(self.frame_botones,
                                             text="Cancelar",
                                             command=self.cancelar,
                                             height=50)
        self.boton_cancelar.pack(side="left", padx=30,pady=20)

      

    def traer_datos(self):
        locale.setlocale(locale.LC_TIME, 'spanish')
        # Esta función debe ser implementada para cargar datos en la tabla
        self.sesiones = get_last_sesions()  # Obtén datos de sesiones (función ficticia)
        for index,sesion in enumerate(self.sesiones):
            fecha = sesion.fecha_cierre.strftime('%A %d-%m %H:%M')
            fecha=str(fecha).capitalize()
            diferencia = sesion.total_wisphub - sesion.total_importe
            mensajes = {
                0: "Caja correcta",
                -1: "Sobra",
                1: "Falta"
                    }
            estado = mensajes[(diferencia > 0) - (diferencia < 0)]
            self.tabla.insert("", tk.END, values=(sesion.cajero.nombre,f"{fecha}",sesion.total_wisphub,sesion.total_importe,estado,sesion.observaciones))
            for item in self.tabla.get_children():
                self.tabla.item(item, tags=("Custom.Row",))  # Aplica un tag a la fila

        # Cambiar la fuente de las filas
        self.tabla.tag_configure("Custom.Row", font=("Lato Bold", 13)) 

       
    def cancelar(self):
        """Función que se ejecuta al presionar el botón 'Cancelar'."""
        self.windows_table.destroy()  # Cierra la ventana
    
    
    def reconstruir(self):
            seleccion = self.tabla.selection()
            if seleccion:
                # Obtener el primer elemento seleccionado
                item_id = seleccion[0]
                # Obtener el índice de la fila seleccionada
                indice = self.tabla.index(item_id)
                
                sesion = self.sesiones[indice]
                
                billetes = [
                (self.txt_billete100),
                (self.txt_billete200),
                (self.txt_billete500),
                (self.txt_billete1000),
                (self.txt_billete2000),
                (self.txt_billetediezmil)
                                                        ]
                for index,billete in enumerate(sesion.billetes):
                    self.carga_entry(billetes[index],billete.cantidad)
                
                self.carga_entry(self.txt_wisphub,int(sesion.total_wisphub))
                
                if sesion.transferencias:
                    new_list = ""
                    for line in sesion.transferencias:
                        new_list+=f"{line.nombre_cliente} {int(line.importe_transferencia)}\n"
                    
                    self.carga_virtuales(new_list)
                else:
                     self.carga_virtuales("\n")
                
                
                self.windows_table.destroy()
    
    def carga_entry(self,entry,new_value):
        entry.delete(first_index="0", last_index=ctk.END)
        entry.insert(0,new_value)
        
        
        
if __name__ == '__main__':
    app=Calculadora()