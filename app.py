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
import re
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from datetime import timedelta
import base64

app = customtkinter.CTk()

# Ajustes app
customtkinter.set_appearance_mode("System")
app.title("Trixa: Organizador de tareas")
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
label1 = customtkinter.CTkLabel(app, text="Trixa: Organizador de tareas", fg_color="transparent", text_color="black", anchor="nw", font=("Catamaran", 25))
label1.pack(padx=12, pady=12, fill="x", side="top")

#Frame tarea principal
frameprincipal = customtkinter.CTkFrame(app)
frameprincipal.pack(fill="both", expand=True, padx=10, pady=0, anchor="nw")

#Añadir Tareas
tareaAANadir = ""
frameanadirtarea = customtkinter.CTkFrame(frameprincipal, fg_color="transparent")
frameanadirtarea.pack(padx=3, pady=3, anchor="nw")

#Imagen Añadir
addImage_ruta = Path(__file__).parent / "Media" / "icono.ico"
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

    # Recargar la interfaz para reflejar los cambios
    recargarInterfaz()

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
        "completada": "Pendiente",
        "correo_enviado": False  
    }

    try:
        with open(tareas_ruta, "r") as file:
            tareas = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        tareas = []

    tareas.insert(0, nueva_tarea)

    with open(tareas_ruta, "w") as file:
        json.dump(tareas, file, indent=4)

    recargarInterfaz()
    textotarea.delete(0, customtkinter.END)
    del fechaSeleccionadaTarea

# Recagar interfaz
def recargarInterfaz():
    # Limpiar todos los widgets dentro de listaTareas
    for widget in listaTareas.winfo_children():
        widget.destroy()  # Usar destroy() en lugar de pack_forget()

    # Cargar las tareas nuevamente
    cargarTareas()
    for tarea in tareas:
        mostrarTarea(tarea["tarea"], tarea["completada"], tarea["fecha"])


# Botón para añadir tarea
buttonAddTask = customtkinter.CTkButton(
    frameanadirtarea, text="Añadir Tarea", command=addTask,
    width=30, height=25, fg_color="lime green", font=("Catamaran", 12)
)
buttonAddTask.pack(padx=2, anchor="n", side="left")


#Guardar correo:
def guardar_correo():
    correo = entryCorreo.get()
    if correo:  
        with open(info_ruta, "w") as file:
            json.dump({"correo": correo}, file, indent=4)
    estado_switch = state_recordarcorreo.get()  
    if correo or estado_switch:  
        with open(info_ruta, "w") as file:
            json.dump({"correo": correo, "recordar_correo": estado_switch}, file, indent=4)

def cargar_correo():
    if info_ruta.exists():
        with open(info_ruta, "r") as file:
            try:
                data = json.load(file)
                return data.get("correo", ""), data.get("recordar_correo", "on")  
            except json.JSONDecodeError:
                return "", "on"  
    return "", "on"  


#Config Frame
def abrirConfig():
    global state_recordarcorreo
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
    #Switch recordar correo

    
    state_recordarcorreo = customtkinter.StringVar(value=cargar_correo()[1])

    switch_recordarcorreo = customtkinter.CTkSwitch(frameAjustesIzq, text="- Recordar tareas por correo electronico", variable=state_recordarcorreo, onvalue="on", offvalue="off")
    switch_recordarcorreo.pack(anchor="nw", padx=4, pady=4)

    
    # Frame ajustes derecha
    frameAjustesDer = customtkinter.CTkFrame(ventana_config, fg_color="gray84")
    frameAjustesDer.pack(expand=True, side="right", anchor="nw", padx=4, fill="x")
    #Correo electronico
    labelcorreo = customtkinter.CTkLabel(frameAjustesDer, text="Correo electronico:", fg_color="transparent", text_color="black", anchor="nw", font=("Catamaran", 15, "bold"))
    labelcorreo.pack(padx=4, pady=2, anchor="n")

    #Entry correo
    global entryCorreo
    entryCorreo = customtkinter.CTkEntry(frameAjustesDer, placeholder_text="ejemplo@ejemplo.com", width=200, font=("Catamaran", 12))
    entryCorreo.pack(pady=0)

    
    correo, estado_switch = cargar_correo()
    entryCorreo.insert(0, correo)
    state_recordarcorreo.set(estado_switch)

    entryCorreo.bind("<KeyRelease>", lambda event: guardar_correo())
    switch_recordarcorreo.configure(command=guardar_correo)

#Enviar correos 
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def obtener_credenciales():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def enviar_correo(destinatario, asunto, mensaje):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if not re.match(regex, destinatario):
        print("Dirección de correo inválida.")
        return

    try:
        creds = obtener_credenciales()
        service = build('gmail', 'v1', credentials=creds)

        mensaje = MIMEText(mensaje)
        mensaje['to'] = destinatario
        mensaje['subject'] = asunto
        raw_message = base64.urlsafe_b64encode(mensaje.as_bytes()).decode()

        message = service.users().messages().send(userId='me', body={'raw': raw_message}).execute()
        print(f"Correo enviado a {destinatario} con mensaje: {asunto}")
    except Exception as error:
        print(f"Error al enviar el correo: {error}")

# Enviar 24h antes
def verificar_tareas_para_correo():
    if cargar_correo()[1] == "off":
        print("El envío de correos está desactivado.")
        return

    def formatear_fecha(fecha):
        dia, mes, anio = fecha.split('/')
        return f"{int(dia):02d}/{int(mes):02d}/{anio}"

    today = datetime.now()
    for tarea in tareas:
        if "fecha" in tarea and not tarea.get("correo_enviado", False):
            try:
                fecha_formateada = formatear_fecha(tarea["fecha"])
                fecha_tarea = datetime.strptime(fecha_formateada, "%d/%m/%y")

                if fecha_tarea - today <= timedelta(days=1) and fecha_tarea - today > timedelta(days=0):
                    correo = cargar_correo()[0]
                    if correo:
                        asunto = f"Recordatorio: Tarea pendiente '{tarea['tarea']}'"
                        mensaje = f"Hola, solo queríamos recordarte que tienes una tarea pendiente: {tarea['tarea']} que debe realizarse el {tarea['fecha']}."
                        enviar_correo(correo, asunto, mensaje)
                        tarea["correo_enviado"] = True  # Marcar el correo como enviado
            except ValueError:
                print(f"Fecha inválida para la tarea {tarea['tarea']}.")

    # Guardar los cambios en el archivo JSON
    with open(tareas_ruta, "w") as file:
        json.dump(tareas, file, indent=4)

def verificar_tareas_periodicamente():
    cargarTareas()  
    verificar_tareas_para_correo() 
    recargarInterfaz()  
    app.after(60000, verificar_tareas_periodicamente)  
    print("Verificado")
verificar_tareas_periodicamente()




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