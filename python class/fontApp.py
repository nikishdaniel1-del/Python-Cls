from customtkinter import *
from tkinter import font

main = CTk()
label = CTkLabel(main,text='Nikish Daniel',font=("Arial", 24))
label.pack()
print(font.families())
CTkOptionMenu(main,values=font.families(),command=lambda x:label.configure(font=(x,24))).pack()
main.mainloop()