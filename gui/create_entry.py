from ttkbootstrap import Entry,Label,Frame
from ttkbootstrap.validation import add_numeric_validation

class Widgets():

    def create_entry_onlynumber(self,color:str,size_font:int,root:Frame) -> Entry:
        entry = Entry(root,
                      background=color,
                      font=("JetBrains Mono",size_font),
                      foreground='#d6dbdf',
                      justify='center')
        add_numeric_validation(entry,when='key')
        
        return entry