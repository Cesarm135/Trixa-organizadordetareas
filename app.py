import tkinter as tk
from tkinter import PhotoImage
from pathlib import Path
import time
import customtkinter

app = customtkinter.CTk()

# Ajustes app
customtkinter.set_appearance_mode("System")
app.title("To-DoList PAI")
customtkinter.set_default_color_theme("blue")
app.configure(fg_color='gray88')
app.geometry("920x520")
app.minsize(width=920, height=520)
icono_ruta = Path(__file__).parent / "Media" / "icono.ico"
app.after(201, lambda :app.iconbitmap(icono_ruta))
customtkinter.set_default_color_theme("green")

#Tareas que hacer texto:
label1 = customtkinter.CTkLabel(app, text="Tareas que hacer:", fg_color="transparent", text_color="black", anchor="nw", width=900, height=100, font=("Catamaran", 30))
label1.pack(padx=6, pady=6, fill="both", expand=True)

#Anadir tarea.
def addTask():
    print("Añadir Tarea")

button1 = customtkinter.CTkButton(app, text="CTkButton", command=addTask, anchor="nw", width=50, height=20)
button1.pack(padx=12, pady=6, fill="both")

app.mainloop()