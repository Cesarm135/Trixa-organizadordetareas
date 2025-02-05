import tkinter as tk
from tkinter import PhotoImage
from pathlib import Path
import time
import customtkinter
from PIL import Image
import json
import os
from tkcalendar import Calendar
from datetime import datetime
from datetime import date
app = customtkinter.CTk()

# Ajustes app
customtkinter.set_appearance_mode("System")
app.title("To-DoList PAI")
customtkinter.set_default_color_theme("blue")
app.configure(fg_color='gray88')
app.geometry("920x520")
app.minsize(width=920, height=520)
icono_ruta = Path(__file__).parent / "Media" / "icono.ico"
tareas_ruta = Path(__file__).parent / "Data" / "tareas.json"
app.after(201, lambda :app.iconbitmap(icono_ruta))
customtkinter.set_default_color_theme("green")

#Tareas que hacer texto:
label1 = customtkinter.CTkLabel(app, text="Lista de tareas:", fg_color="transparent", text_color="black", anchor="nw", font=("Catamaran", 30))
label1.pack(padx=12, pady=12, fill="x", side="top")

#Frame tarea principal
frameprincipal = customtkinter.CTkFrame(app)
frameprincipal.pack(fill="both", expand=True, padx=10, pady=0, anchor="nw")

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

# Calendario boton
image_rutaCalendario = Path(__file__).parent / "Media" / "calendario.png"
imagenCalendario = customtkinter.CTkImage(light_image=Image.open(image_rutaCalendario),
                                  dark_image=Image.open(image_rutaCalendario),
                                  size=(20, 20))

# Función del botón
def calendario_boton():
    image_RutaCalendarioICO_ruta = Path(__file__).parent / "Media" / "calendario.ico"
    ventana_calendario = customtkinter.CTkToplevel(app)
    ventana_calendario.title("Seleccionar fecha:")
    ventana_calendario.geometry("250x215")
    # ventana_calendario.grab_set()
    ventana_calendario.attributes("-topmost", True)
    ventana_calendario.after(200, lambda: ventana_calendario.iconbitmap(image_RutaCalendarioICO_ruta))
    #Calendario
    today = date.today()
    calendario = Calendar(ventana_calendario, selectmode="day", year=datetime.now().year, month=datetime.now().month, day=today.day, font=("Catamaran"), locale="es_ES", background="transparent")
    calendario.pack(side="top", anchor="n")
    #Boton de seleccionar fecha
    def confirmarFecha():
        fechaSeleccionada = calendario.get_date()
        print(fechaSeleccionada)
        ventana_calendario.destroy()
    seleccionar_fecha = customtkinter.CTkButton(ventana_calendario, text="Hecho", command=confirmarFecha, font=("Catamaran", 12), fg_color="lime green", width=123)
    seleccionar_fecha.pack(padx=2, side="right", anchor="se")
     #Boton cancelar
    def cancelarFecha():
        ventana_calendario.destroy()
    cancelar_fecha = customtkinter.CTkButton(ventana_calendario, text="Cancelar", command=cancelarFecha, font=("Catamaran", 12), fg_color="transparent", width=123, text_color="lime green", hover_color="pale green")
    cancelar_fecha.pack(padx=2, anchor="s", side="left")

# Crear botón con imagen
button_image = customtkinter.CTkButton(master=frameanadirtarea, image=imagenCalendario, text="", 
                                       fg_color="transparent", hover_color="gray",
                                       command=calendario_boton, width=25)
button_image.pack(anchor="nw", padx=2, side="left")


# Lista de tareas
listaTareas = customtkinter.CTkScrollableFrame(frameprincipal, fg_color="transparent")
listaTareas.pack(anchor="nw", fill="both", expand=True)

def cargarTareas():
    if os.path.exists(tareas_ruta):  
        with open(tareas_ruta, "r") as file:
            try:
                tareas = json.load(file)
            except json.JSONDecodeError:
                tareas = []

        tareas.sort(key=lambda tarea: tarea["completada"] == "Completada")
        for tarea in tareas:
            mostrarTarea(tarea["tarea"], tarea["completada"])

def mostrarTarea(texto, completada):
    # Contenedor para la tarea
    tarea_frame = customtkinter.CTkFrame(listaTareas, fg_color="white", corner_radius=5)
    tarea_frame.pack(fill="x", pady=5, padx=10)

    # Checkbox
    checkbox = customtkinter.CTkCheckBox(
        tarea_frame, text="", command=lambda: actualizarTarea(texto, checkbox)
    )
    checkbox.pack(side="left", padx=5)
    if completada == "Completada":
        checkbox.select()
        tarea_estilo = {"text_color": "gray", "font": ("Catamaran", 12, "overstrike")}
    else:
        checkbox.deselect()
        tarea_estilo = {"text_color": "black", "font": ("Catamaran", 12)}

# Tarea
    tarea_label = customtkinter.CTkLabel(
        tarea_frame, text=texto, **tarea_estilo
    )
    tarea_label.pack(side="left", padx=10)
# Función para actualizar el estado de una tarea
def actualizarTarea(texto, checkbox):
    # Leer archivo JSON
    if os.path.exists(tareas_ruta):
        with open(tareas_ruta, "r") as file:
            tareas = json.load(file)
    else:
        tareas = []

    # Actualizar el estado de la tarea correspondiente
    for tarea in tareas:
        if tarea["tarea"] == texto:
            tarea["completada"] = "Completada" if checkbox.get() else "Pendiente"
            break

    # Guardar los cambios en el archivo
    with open(tareas_ruta, "w") as file:
        json.dump(tareas, file, indent=4)

    recargarInterfaz()

# Función para añadir nueva tarea
def addTask():
    tareaAANadir = textotarea.get().strip()
    if not tareaAANadir:
        print("La tarea no puede estar vacía.")
        return

    fecha = "Sin definir"
    nueva_tarea = {
        "tarea": tareaAANadir,
        "fecha": fecha,
        "completada": "Pendiente"
    }

    # Leer archivo JSON
    try:
        with open(tareas_ruta, "r") as file:
            tareas = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        tareas = []

    # Añadir nueva tarea
    tareas.insert(0, nueva_tarea)

    # Guardar en el archivo
    with open(tareas_ruta, "w") as file:
        json.dump(tareas, file, indent=4)

    # Mostrar en la interfaz
    recargarInterfaz()

    # Limpiar entrada
    textotarea.delete(0, customtkinter.END)

# Recagar interfaz
def recargarInterfaz():
    # Eliminar todos los widgets dentro de listaTareas
    for widget in listaTareas.winfo_children():
       widget.pack_forget()

    cargarTareas()

# Botón para añadir tarea
buttonAddTask = customtkinter.CTkButton(
    frameanadirtarea, text="Añadir Tarea", command=addTask,
    width=30, height=25, fg_color="lime green", font=("Catamaran", 12)
)
buttonAddTask.pack(padx=2, anchor="n", side="left")

#Config Frame
def abrirConfig():
    configImage_ruta = Path(__file__).parent / "Media" / "config.ico"
    ventana_config = customtkinter.CTkToplevel(app)
    ventana_config.title("Configuracion")
    ventana_config.geometry("700x400")
    ventana_config.grab_set()
    ventana_config.attributes("-topmost", True)
    ventana_config.after(201, lambda: ventana_config.iconbitmap(configImage_ruta))
    labelconfig = customtkinter.CTkLabel(ventana_config, text="Configuracion:", fg_color="transparent", text_color="black", anchor="nw", font=("Catamaran", 20))
    labelconfig.pack(padx=4, pady=4, fill="x")
    # Frame ajustes izquierda
    frameAjustesIzq = customtkinter.CTkFrame(ventana_config, fg_color="transparent", width=400)
    frameAjustesIzq.pack(expand=True, side="left", anchor="nw", padx=4, fill="x")
    state_recordarcorreo = customtkinter.StringVar(value="on")
    switch_recordarcorreo = customtkinter.CTkSwitch(frameAjustesIzq, text="- Recordar tareas por correo electronico", variable=state_recordarcorreo, onvalue="on", offvalue="off")
    switch_recordarcorreo.pack(anchor="nw")


    # Frame ajustes derecha
    frameAjustesDer = customtkinter.CTkFrame(ventana_config, fg_color="transparent")
    frameAjustesDer.pack(expand=True, side="right", anchor="nw", padx=4, fill="x")

# Botón config
buttonConfig = customtkinter.CTkButton(
    app, text="Configuracion", command=abrirConfig,
    width=50, height=40, fg_color="gray", font=("Catamaran", 15)
)
buttonConfig.pack(padx=5, pady=6, anchor="se", side="bottom")



# Cargar tareas al iniciar
cargarTareas()

# Ejecutar la aplicación
app.mainloop()