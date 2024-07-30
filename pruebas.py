import ttkbootstrap as ttk
from ttkbootstrap.validation import add_text_validation,add_regex_validation,add_option_validation,add_numeric_validation

app = ttk.Window()

entry = ttk.Entry()
entry.pack(padx=10, pady=10)

# check if contents is text
add_text_validation(entry)

# prevent any entry except text
add_numeric_validation(entry, when='key')

# # check for a specific list of options
# add_option_validation(entry, ['red', 'blue', 'green'])

# # validate against a specific regex expression
# add_regex_validation(entry, r'\d{4}-\d{2}-\d{2}') 

app.mainloop()