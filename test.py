from tkinter import *
from tkinter.ttk import *

# creating tkinter window 
root = Tk()

# Adding widgets to the root window 
Label(root, text = 'btn').pack(side = TOP, pady = 10) 
 
# Creating a photoimage object to use image 
photo = PhotoImage(file = r"img/refresh.png") 
  
# here, image option is used to set image on button  
Button(root, text = 'button', image = photo).pack(side = TOP)  
 
mainloop()