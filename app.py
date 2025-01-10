import tkinter as tk
from tkinter import PhotoImage
from pathlib import Path
import time
import customtkinter
from PIL import Image

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

#Imagen Añadir
addImage_ruta = Path(__file__).parent / "Media" / "add.png"
addImage = customtkinter.CTkImage(light_image=Image.open(addImage_ruta),
                                  dark_image=Image.open(addImage_ruta),
                                  size=(25, 25))

addImageLabel = customtkinter.CTkLabel(frameanadirtarea, image=addImage, text="")
addImageLabel.pack(side="left")

# Texto para añadir tarea
textotarea = customtkinter.CTkEntry(frameanadirtarea, placeholder_text="Escriba su tarea", font=("Catamaran", 12), height=25, fg_color="transparent")
textotarea.pack(side="left", padx= 3)

#Anadir tarea boton
def addTask():
    tareaAANadir = textotarea.get()
    print("Añadiendo tarea: " + textotarea.get())
    textotarea.delete(0, customtkinter.END)

buttonAddTask = customtkinter.CTkButton(frameanadirtarea, text="Añadir Tarea", command=addTask, width=30, height=25, fg_color="lime green", font=("Catamaran", 12))
buttonAddTask.pack(padx=4, anchor="n", side="left")

# Lista de tareas
listaTareas = customtkinter.CTkFrame(frameprincipal, fg_color="green")
listaTareas.pack(anchor="nw", fill="both")







app.mainloop()