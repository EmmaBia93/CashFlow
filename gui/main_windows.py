import tkinter as tk
import ttkbootstrap as ttk
from gui.create_entry import Widgets

class MainWindows():

    def __init__(self) -> None:

        self.root = tk.Tk()
        self.root.geometry("1920x1080+0+0")
        self.root.wm_state('zoomed')
        style = ttk.Style("darkly")
        self.creator_widget = Widgets()
        self.w_screen = self.root.winfo_screenwidth()
        self.h_screen = self.root.winfo_screenheight()
        self.root.grid_columnconfigure(0,weight=4)
        self.root.grid_rowconfigure(0,weight=7)
        self.root.grid_rowconfigure(1,weight=3)
        self.create_frames()
        self.create_widgets()


    def create_frames(self):
        
        
        self.f_bill = ttk.Frame(self.root,border=3,width=self.w_screen//2,bootstyle="danger",height=self.h_screen//2)
        self.f_bill.grid(column=0,row=0,sticky='nw')
        
        self.f_results = ttk.Frame(self.root,width=self.w_screen//2,bootstyle="warning")
        self.f_results.grid(column=0,row=1)

        self.f_transfer = ttk.Frame(self.root,width=self.w_screen//2,height=self.h_screen,bootstyle="info")
        self.f_transfer.grid(column=1,row=0,rowspan=2)

    def create_widgets(self):
        self.btn1 = self.creator_widget.create_entry_onlynumber('#16a085',20,self.f_bill)
        self.btn2 = self.creator_widget.create_entry_onlynumber('#16a085',20,self.f_bill)
        self.btn3 = self.creator_widget.create_entry_onlynumber('#16a085',20,self.f_bill)
        self.btn4 = self.creator_widget.create_entry_onlynumber('#16a085',20,self.f_bill)
        self.btn5 = self.creator_widget.create_entry_onlynumber('#16a085',20,self.f_bill)

        self.btn1.pack(fill='both',padx=15,pady=10)
        self.btn2.pack(fill='both',padx=15,pady=10)
        self.btn3.pack(fill='both',padx=15,pady=10)
        self.btn4.pack(fill='both',padx=15,pady=10)
        self.btn5.pack(fill='both',padx=15,pady=10)
        
       



    def run(self):
        self.root.mainloop()