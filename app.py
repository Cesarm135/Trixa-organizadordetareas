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

#Frame tarea principal
frameprincipal = customtkinter.CTkFrame(app)
frameprincipal.pack(fill="both", expand=True, padx=20, pady=20, anchor="nw")


#Tareas que hacer texto:
label1 = customtkinter.CTkLabel(frameprincipal, text="Tareas que hacer:", fg_color="transparent", text_color="black", anchor="nw", width=10, height=10, font=("Catamaran", 30))
label1.pack(padx=6, pady=6, fill="both")

#Añadir Tareas
tareaAANadir = ""
frameanadirtarea = customtkinter.CTkFrame(frameprincipal, fg_color="transparent")
frameanadirtarea.pack(padx=3, pady=3, anchor="nw")

# Texto para añadir tarea
textotarea = customtkinter.CTkEntry(frameanadirtarea, placeholder_text="Escriba su tarea")
textotarea.pack(anchor="nw", side="left")

#Anadir tarea boton
def addTask():
    tareaAANadir = textotarea.get()
    print("Añadiendo tarea: " + textotarea.get())
    textotarea.delete(0, customtkinter.END)

button1 = customtkinter.CTkButton(frameanadirtarea, text="Añadir Tarea", command=addTask, width=20, height=20, fg_color="lime green")
button1.pack(padx=12, pady=6, anchor="nw", side="right")

# Lista de tareas
listaTareas = customtkinter.CTkFrame(frameprincipal, fg_color="green", height="90")
listaTareas.pack(anchor="nw", fill="x")
app.mainloop()