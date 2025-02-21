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
import locale
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
info_ruta = Path(__file__).parent / "Data" / "info.json"
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
    ventana_calendario.geometry("260x310")
    ventana_calendario.maxsize(260, 310)
    ventana_calendario.grab_set()
    ventana_calendario.attributes("-topmost", True)
    ventana_calendario.after(200, lambda: ventana_calendario.iconbitmap(image_RutaCalendarioICO_ruta))
    #Calendario
    today = date.today()
    labelFecha = customtkinter.CTkLabel(ventana_calendario, text="Mes                                  Año", fg_color="transparent", text_color="black", anchor="nw", font=("Catamaran", 20))
    labelFecha.pack(side="top", anchor="n")
    calendario = Calendar(ventana_calendario, selectmode="day", showweeknumbers=False, showothermonthdays=True, foreground="transparent", year=datetime.now().year, month=datetime.now().month, day=today.day, font=("Catamaran"), yearint=datetime.now().year, locale="es_ES", background="transparent")
    calendario.pack(anchor="n", fill="x", expand=True)

    #Boton de seleccionar fecha
    def confirmarFecha():
        fechaSeleccionada = calendario.get_date()
        ventana_calendario.destroy()
        global fechaSeleccionadaTarea
        fechaSeleccionadaTarea = fechaSeleccionada
        
    seleccionar_fecha = customtkinter.CTkButton(ventana_calendario, text="Hecho", command=confirmarFecha, font=("Catamaran", 12), fg_color="lime green", width=123)
    seleccionar_fecha.pack(padx=2, anchor="se", side="left")

     #Boton cancelar
    def cancelarFecha():
        ventana_calendario.destroy()
    cancelar_fecha = customtkinter.CTkButton(ventana_calendario, text="Cancelar", command=cancelarFecha, font=("Catamaran", 12), fg_color="transparent", width=123, text_color="lime green", hover_color="pale green")
    cancelar_fecha.pack(padx=2, anchor="s", side="right")

# Crear botón con imagen
button_image = customtkinter.CTkButton(master=frameanadirtarea, image=imagenCalendario, text="", 
                                       fg_color="transparent", hover_color="gray",
                                       command=calendario_boton, width=25)
button_image.pack(anchor="nw", padx=2, side="left")


# Lista de tareas
listaTareas = customtkinter.CTkScrollableFrame(frameprincipal, fg_color="transparent")
listaTareas.pack(anchor="nw", fill="both", expand=True)

def cargarTareas():
    global tareas
    if os.path.exists(tareas_ruta):  
        with open(tareas_ruta, "r") as file:
            try:
                tareas = json.load(file)
            except json.JSONDecodeError:
                tareas = []

        def obtener_fecha(tarea):
            try:
                fecha_str = tarea["fecha"]
                if len(fecha_str.split("/")[-1]) == 2:  # Si el año tiene solo 2 dígitos
                    return datetime.strptime(fecha_str, "%d/%m/%y")
                return datetime.strptime(fecha_str, "%d/%m/%Y")
            except (KeyError, ValueError):
                return datetime.max  # Si hay un error, la manda al final


        tareas.sort(key=lambda tarea: (tarea["completada"] == "Completada", obtener_fecha(tarea)))
        for tarea in tareas:
            mostrarTarea(tarea["tarea"], tarea["completada"], tarea["fecha"])

def mostrarTarea(texto, completada, fecha):
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
    fecha_label = customtkinter.CTkLabel(
    tarea_frame, text=fecha, text_color="gray", font=("Catamaran", 10)
)
    fecha_label.pack(side="right", padx=10)
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
    global fechaSeleccionadaTarea
    tareaAANadir = textotarea.get().strip()
    if not tareaAANadir:
        print("La tarea no puede estar vacía.")
        return

    if "fechaSeleccionadaTarea" not in globals():
        fechaSeleccionadaTarea = "" 

    fecha = fechaSeleccionadaTarea  
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
    del fechaSeleccionadaTarea

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
    #ventana_config.attributes("-topmost", True)
    ventana_config.after(201, lambda: ventana_config.iconbitmap(configImage_ruta))
    labelconfig = customtkinter.CTkLabel(ventana_config, text="Configuracion:", fg_color="transparent", text_color="black", anchor="nw", font=("Catamaran", 20))
    labelconfig.pack(padx=4, pady=4, fill="x")
    # Frame ajustes izquierda
    frameAjustesIzq = customtkinter.CTkFrame(ventana_config, fg_color="transparent", width=400, height=350)
    frameAjustesIzq.pack(expand=True, side="left", anchor="nw", padx=4, pady=4, fill="x")
    state_recordarcorreo = customtkinter.StringVar(value="on")
    switch_recordarcorreo = customtkinter.CTkSwitch(frameAjustesIzq, text="- Recordar tareas por correo electronico", variable=state_recordarcorreo, onvalue="on", offvalue="off")
    switch_recordarcorreo.pack(anchor="nw", padx=4, pady=4)

    
    # Frame ajustes derecha
    frameAjustesDer = customtkinter.CTkFrame(ventana_config, fg_color="gray84")
    frameAjustesDer.pack(expand=True, side="right", anchor="nw", padx=4, fill="x")
    #Correo electronico
    labelcorreo = customtkinter.CTkLabel(frameAjustesDer, text="Correo electronico:", fg_color="transparent", text_color="black", anchor="nw", font=("Catamaran", 15, "bold"))
    labelcorreo.pack(padx=4, pady=2, anchor="n")

    #Entry correo
    #Guardar correo:
    def guardar_correo():
        correo = entryCorreo.get()
        if correo:  
            with open(info_ruta, "w") as file:
                json.dump({"correo": correo}, file, indent=4)

    def cargar_correo():
        if info_ruta.exists():
            with open(info_ruta, "r") as file:
                try:
                    data = json.load(file)
                    return data.get("correo", "")
                except json.JSONDecodeError:
                    return ""
        return ""

    entryCorreo = customtkinter.CTkEntry(frameAjustesDer, placeholder_text="ejemplo@ejemplo.com", width=200, font=("Catamaran", 12))
    entryCorreo.pack(pady=0)

    entryCorreo.insert(0, cargar_correo())
    entryCorreo.bind("<KeyRelease>", lambda event: guardar_correo())

#Frame botones abajo
frameBotones = customtkinter.CTkFrame(app, fg_color="transparent")
frameBotones.pack(anchor="se", side="bottom")
#Eliminar boton
def eliminarTareasCompletadas():
        global tareas 
        tareas = [tarea for tarea in tareas if tarea["completada"] != "Completada"]
        with open(tareas_ruta, "w") as file:
            json.dump(tareas, file, indent=4) 
        recargarInterfaz()  

eliminarBoton = customtkinter.CTkButton(frameBotones, text="Borrar tareas completadas", command=eliminarTareasCompletadas,
width=50, height=40, fg_color="red", font=("Catamaran", 15), text_color="white", hover_color="red4")
eliminarBoton.pack(anchor="se", padx=5, pady=5, side="left")

    

# Botón config
buttonConfig = customtkinter.CTkButton(
    frameBotones, text="Configuracion", command=abrirConfig,
    width=50, height=40, fg_color="gray", font=("Catamaran", 15)
)
buttonConfig.pack(padx=5, pady=5, anchor="s", side="right")



# Cargar tareas al iniciar
cargarTareas()

# Ejecutar la aplicación
app.mainloop()