import tkinter as tk
from tkinter import PhotoImage, ttk
from pathlib import Path
import time
import customtkinter
from PIL import Image
import json
import os
from tkcalendar import Calendar
from datetime import datetime, date, timedelta
import locale
import re
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64

app = customtkinter.CTk()

# Ajustes de la app
customtkinter.set_appearance_mode("System")
app.title("Trixa: Organizador de tareas")
customtkinter.set_default_color_theme("blue")
app.configure(fg_color='gray88')
app.geometry("920x520")
app.minsize(width=920, height=520)
icono_ruta = Path(__file__).parent / "Media" / "icono.ico"
tareas_ruta = Path(__file__).parent / "Data" / "tareas.json"
info_ruta = Path(__file__).parent / "Data" / "info.json"
app.after(201, lambda: app.iconbitmap(icono_ruta))
customtkinter.set_default_color_theme("green")

# Variables de configuración para la tarea
config_tiempo = ""
config_prioridad = ""
fechaSeleccionadaTarea = ""

label1 = customtkinter.CTkLabel(app, text="Trixa: Organizador de tareas", fg_color="transparent", 
                                text_color="black", anchor="nw", font=("Catamaran", 25))
label1.pack(padx=12, pady=12, fill="x", side="top")

frameprincipal = customtkinter.CTkFrame(app)
frameprincipal.pack(fill="both", expand=True, padx=10, pady=0, anchor="nw")

# --- Frame de añadir tarea ---
frameanadirtarea = customtkinter.CTkFrame(frameprincipal, fg_color="transparent")
frameanadirtarea.pack(fill="x", padx=3, pady=3, anchor="nw")


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
                if fecha_str.strip() == "":
                    return datetime(1900, 1, 1)
                try:
                    return datetime.strptime(fecha_str, "%d/%m/%Y")
                except ValueError:
                    return datetime.strptime(fecha_str, "%d/%m/%y")
            except (KeyError, ValueError):
                return datetime(1900, 1, 1)
        if ordenar_combo.get() == "Ordenar por Tiempo/Prioridad":
            not_completed = [t for t in tareas if t["completada"] != "Completada"]
            completed = [t for t in tareas if t["completada"] == "Completada"]
            def sort_key(task):
                prioridad_niveles = {"Muy urgente": 0, "Urgente": 1, "No urgente": 2, "": 3}
                prioridad = prioridad_niveles.get(task.get("prioridad", ""), 3)
                tiempo_val = sum(int(x[:-1]) * (60 if "h" in x else 1) for x in re.findall(r'\d+[hm]', task.get("tiempo", "")))
                return (prioridad, -tiempo_val)
            not_completed.sort(key=sort_key)
            completed.sort(key=lambda t: obtener_fecha(t))
            tareas = not_completed + completed
        else:
            tareas.sort(key=lambda t: (t["completada"] == "Completada", obtener_fecha(t)))
    else:
        tareas = []

def recargarInterfaz(*args):
    for widget in listaTareas.winfo_children():
        widget.destroy()
    cargarTareas()
    for tarea in tareas:
        mostrarTarea(tarea["tarea"], tarea["completada"], tarea["fecha"], tarea.get("tiempo", ""), tarea.get("prioridad", ""))

# Subframe para colocar todos los controles en una sola fila
frameAñadir = customtkinter.CTkFrame(frameanadirtarea, fg_color="transparent")
frameAñadir.pack(fill="x", pady=5)

# Imagen "Añadir"
addImage_ruta = Path(__file__).parent / "Media" / "icono.ico"
addImage = customtkinter.CTkImage(light_image=Image.open(addImage_ruta),
                                  dark_image=Image.open(addImage_ruta),
                                  size=(25, 25))
addImageLabel = customtkinter.CTkLabel(frameAñadir, image=addImage, text="")
addImageLabel.pack(side="left", padx=2)

# Entrada de texto para la tarea
textotarea = customtkinter.CTkEntry(frameAñadir, placeholder_text="Escriba su tarea", 
                                    font=("Catamaran", 12), height=25, fg_color="transparent")
textotarea.pack(side="left", padx=2)

# Botón de calendario
image_rutaCalendario = Path(__file__).parent / "Media" / "calendario.png"
imagenCalendario = customtkinter.CTkImage(light_image=Image.open(image_rutaCalendario),
                                          dark_image=Image.open(image_rutaCalendario),
                                          size=(20, 20))
def calendario_boton():
    image_RutaCalendarioICO_ruta = Path(__file__).parent / "Media" / "calendario.ico"
    ventana_calendario = customtkinter.CTkToplevel(app)
    ventana_calendario.title("Seleccionar fecha:")
    ventana_calendario.geometry("260x310")
    ventana_calendario.maxsize(260, 310)
    ventana_calendario.grab_set()
    ventana_calendario.attributes("-topmost", True)
    ventana_calendario.after(200, lambda: ventana_calendario.iconbitmap(image_RutaCalendarioICO_ruta))
    today = date.today()
    labelFecha = customtkinter.CTkLabel(ventana_calendario, 
        text="Mes                                  Año", fg_color="transparent", 
        text_color="black", anchor="nw", font=("Catamaran", 20))
    labelFecha.pack(side="top", anchor="n")
    calendario = Calendar(ventana_calendario, selectmode="day", showweeknumbers=False, 
                          showothermonthdays=True, foreground="transparent", 
                          year=datetime.now().year, month=datetime.now().month, day=today.day, 
                          font=("Catamaran"), yearint=datetime.now().year, locale="es_ES", background="transparent")
    calendario.pack(anchor="n", fill="x", expand=True)
    def confirmarFecha():
        fechaSeleccionada = calendario.get_date()
        ventana_calendario.destroy()
        global fechaSeleccionadaTarea
        fechaSeleccionadaTarea = fechaSeleccionada
    seleccionar_fecha = customtkinter.CTkButton(ventana_calendario, text="Hecho", 
                                                 command=confirmarFecha, font=("Catamaran", 12), 
                                                 fg_color="lime green", width=123)
    seleccionar_fecha.pack(padx=2, anchor="se", side="left")
    def cancelarFecha():
        ventana_calendario.destroy()
    cancelar_fecha = customtkinter.CTkButton(ventana_calendario, text="Cancelar", 
                                             command=cancelarFecha, font=("Catamaran", 12), 
                                             fg_color="transparent", width=123, text_color="lime green", hover_color="pale green")
    cancelar_fecha.pack(padx=2, anchor="s", side="right")
button_calendario = customtkinter.CTkButton(frameAñadir, image=imagenCalendario, text="", 
                                            fg_color="transparent", hover_color="gray",
                                            command=calendario_boton, width=25)
button_calendario.pack(side="left", padx=2)

# Botón de configuración de tarea (para tiempo y prioridad)
image_rutaSettings = Path(__file__).parent / "Media" / "settings.png"
imagenSettings = customtkinter.CTkImage(light_image=Image.open(image_rutaSettings),
                                        dark_image=Image.open(image_rutaSettings),
                                        size=(20, 20))

sel_hora = ""
sel_min = ""
def abrir_configuracion():
    ventana_config = customtkinter.CTkToplevel(app)
    ventana_config.title("Configurar tarea")
    ventana_config.geometry("300x260")
    ventana_config.maxsize(300, 260)
    ventana_config.grab_set()
    ventana_config.after(200, lambda: ventana_config.iconbitmap(icono_ruta))
    frame_superior = customtkinter.CTkFrame(ventana_config, fg_color="transparent")
    frame_superior.pack(padx=10, pady=10, fill="both", expand=True)

    

    # Labels en negrita y de mayor tamaño
    label_tiempo = customtkinter.CTkLabel(frame_superior, text="Tiempo necesario:", font=("Catamaran", 16, "bold"))
    label_tiempo.pack(pady=5)
    combo_horas = ttk.Combobox(frame_superior, values=["-"] + [f"{i} h" for i in range(0,9)],
                               font=("Catamaran", 12), justify="center")
    combo_horas.pack(pady=2)
    combo_horas.current(0)
    combo_minutos = ttk.Combobox(frame_superior, values=["-","0m","5m","10m","15m","20m","30m","40m","50m"],
                                 font=("Catamaran", 12), justify="center")
    combo_minutos.pack(pady=2)
    combo_minutos.current(0)
    label_prioridad = customtkinter.CTkLabel(frame_superior, text="Prioridad:", font=("Catamaran", 16, "bold"))
    label_prioridad.pack(pady=5)
    combo_prioridad = ttk.Combobox(frame_superior, values=["-","No urgente", "Urgente", "Muy urgente"],
                                   font=("Catamaran", 12), justify="center")
    combo_prioridad.pack(pady=2)
    combo_prioridad.current(0)

    

    def guardar_config():
        global config_tiempo, config_prioridad, sel_min, sel_hora
        sel_hora = combo_horas.get()
        sel_min = combo_minutos.get()
        sel_prio = combo_prioridad.get()
        config_tiempo = "" if sel_hora == "-" or sel_min == "-" else f"{sel_hora} {sel_min}"
        config_prioridad = "" if sel_prio == "-" else sel_prio
        ventana_config.destroy()

    combo_horas.set(sel_hora if sel_hora else "-")
    combo_minutos.set(sel_min if sel_min else "-")
    combo_prioridad.set(config_prioridad if config_prioridad else "-")

    # Botones "Hecho" y "Cancelar" para guardar o descartar
    frame_botones = customtkinter.CTkFrame(frame_superior, fg_color="transparent")
    frame_botones.pack(pady=10, fill="x")
    boton_hecho = customtkinter.CTkButton(frame_botones, text="Hecho", command=guardar_config, 
                                          font=("Catamaran", 12), fg_color="lime green")
    boton_hecho.pack(side="left", padx=5)
    boton_cancelar = customtkinter.CTkButton(frame_botones, text="Cancelar", 
                                             command=lambda: ventana_config.destroy(), 
                                             font=("Catamaran", 12), fg_color="red")
    boton_cancelar.pack(side="left", padx=5)
button_settings = customtkinter.CTkButton(frameAñadir, image=imagenSettings, text="", 
                                          fg_color="transparent", hover_color="gray", 
                                          command=abrir_configuracion, width=25)
button_settings.pack(side="left", padx=2)

# Botón para añadir la tarea
buttonAddTask = customtkinter.CTkButton(frameAñadir, text="Añadir Tarea", command= lambda: addTask(),
                                        width=30, height=25, fg_color="lime green", font=("Catamaran", 12))
buttonAddTask.pack(side="left", padx=2)

# Desplegable de ordenación, colocado al extremo derecho de este mismo frame
ordenar_combo = customtkinter.CTkComboBox(frameAñadir, values=["Ordenar por Completada", "Ordenar por Tiempo/Prioridad"],
                                           width=150, font=("Catamaran", 12), command=recargarInterfaz)
ordenar_combo.set("Ordenar por Completada")
ordenar_combo.pack(side="right", padx=5)


# --- Área para listar tareas ---
listaTareas = customtkinter.CTkScrollableFrame(frameprincipal, fg_color="transparent")
listaTareas.pack(anchor="nw", fill="both", expand=True)

def actualizarTarea(texto, checkbox):
    if os.path.exists(tareas_ruta):
        with open(tareas_ruta, "r") as file:
            tareas = json.load(file)
    else:
        tareas = []
    for tarea in tareas:
        if tarea["tarea"] == texto:
            tarea["completada"] = "Completada" if checkbox.get() else "Pendiente"
            break
    with open(tareas_ruta, "w") as file:
        json.dump(tareas, file, indent=4)
    recargarInterfaz()



def mostrarTarea(texto, completada, fecha, tiempo, prioridad):
    tarea_frame = customtkinter.CTkFrame(listaTareas, fg_color="white", corner_radius=5)
    tarea_frame.pack(fill="x", pady=5, padx=10)
    checkbox = customtkinter.CTkCheckBox(tarea_frame, text="", command=lambda: actualizarTarea(texto, checkbox))
    checkbox.pack(side="left", padx=5)
    if completada == "Completada":
        checkbox.select()
        tarea_estilo = {"text_color": "gray", "font": ("Catamaran", 10, "overstrike")}
    else:
        checkbox.deselect()
        tarea_estilo = {"text_color": "black", "font": ("Catamaran", 10)}
    tarea_label = customtkinter.CTkLabel(tarea_frame, text=texto, font=tarea_estilo["font"], fg_color="transparent", text_color=tarea_estilo["text_color"])
    tarea_label.pack(side="left", padx=20)
    if completada != "Completada":
        if prioridad and tiempo:
            info_text = f"{prioridad} {tiempo}"
            if prioridad == "No urgente":
                bg_color = "#22a30f"
            elif prioridad == "Urgente":
                bg_color = "#edc200"
            elif prioridad == "Muy urgente":
                bg_color = "#ad0707"
            else:
                bg_color = "gray"
            info_frame = customtkinter.CTkFrame(tarea_frame, fg_color=bg_color, corner_radius=5, height=5)
            info_frame.pack(side="left", padx=5)
            info_label = customtkinter.CTkLabel(info_frame, text=info_text, text_color="white", font=("Catamaran", 8), fg_color=bg_color)
            info_label.pack(padx=4, pady=2)
        elif tiempo:
            info_text = tiempo
            bg_color = "gray"  # Color gris si no hay prioridad
            info_frame = customtkinter.CTkFrame(tarea_frame, fg_color=bg_color, corner_radius=5, height=5)
            info_frame.pack(side="left", padx=5)
            info_label = customtkinter.CTkLabel(info_frame, text=info_text, text_color="white", font=("Catamaran", 8), fg_color=bg_color)
            info_label.pack(padx=4, pady=2)
        fecha_label = customtkinter.CTkLabel(tarea_frame, text=fecha, text_color="gray", font=("Catamaran", 8))
        fecha_label.pack(side="right", padx=10)

def addTask():
    global fechaSeleccionadaTarea, config_tiempo, config_prioridad
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
        "correo_enviado": False,
        "tiempo": config_tiempo,
        "prioridad": config_prioridad
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
    if "fechaSeleccionadaTarea" in globals():
        del fechaSeleccionadaTarea

    config_tiempo = ""
    config_prioridad = ""
    fechaSeleccionadaTarea = ""
    sel_hora = ""
    sel_min = ""



# Configuración de correo
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

def abrirConfig():
    global state_recordarcorreo
    configImage_ruta = Path(__file__).parent / "Media" / "config.ico"
    ventana_config = customtkinter.CTkToplevel(app)
    ventana_config.title("Configuración")
    ventana_config.geometry("700x400")
    ventana_config.grab_set()
    ventana_config.after(201, lambda: ventana_config.iconbitmap(configImage_ruta))
    labelconfig = customtkinter.CTkLabel(ventana_config, text="Configuración:", fg_color="transparent", 
                                         text_color="black", anchor="nw", font=("Catamaran", 20))
    labelconfig.pack(padx=10, pady=10, fill="x")
    frameAjustesIzq = customtkinter.CTkFrame(ventana_config, fg_color="transparent", width=400, height=350)
    frameAjustesIzq.pack(expand=True, side="left", anchor="nw", padx=10, pady=10, fill="both")
    state_recordarcorreo = customtkinter.StringVar(value=cargar_correo()[1])
    switch_recordarcorreo = customtkinter.CTkSwitch(frameAjustesIzq, text="- Recordar tareas por correo electrónico",
                                                    variable=state_recordarcorreo, onvalue="on", offvalue="off",
                                                    font=("Catamaran", 14))
    switch_recordarcorreo.pack(anchor="nw", padx=10, pady=10)
    frameAjustesDer = customtkinter.CTkFrame(ventana_config, fg_color="gray84")
    frameAjustesDer.pack(expand=True, side="right", anchor="nw", padx=10, fill="x")
    labelcorreo = customtkinter.CTkLabel(frameAjustesDer, text="Correo electrónico:", fg_color="transparent",
                                         text_color="black", anchor="nw", font=("Catamaran", 15, "bold"))
    labelcorreo.pack(padx=10, pady=10, anchor="n")
    global entryCorreo
    entryCorreo = customtkinter.CTkEntry(frameAjustesDer, placeholder_text="ejemplo@ejemplo.com", width=200, font=("Catamaran", 12))
    entryCorreo.pack(pady=5)
    correo, estado_switch = cargar_correo()
    entryCorreo.insert(0, correo)
    state_recordarcorreo.set(estado_switch)
    entryCorreo.bind("<KeyRelease>", lambda event: guardar_correo())
    switch_recordarcorreo.configure(command=guardar_correo)

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
                        mensaje = f"Hola, te recordamos que tienes una tarea pendiente: {tarea['tarea']} para el {tarea['fecha']}.\nPrioridad: {tarea.get('prioridad', '')}\nTiempo estimado: {tarea.get('tiempo', '')}"
                        enviar_correo(correo, asunto, mensaje)
                        tarea["correo_enviado"] = True
            except ValueError:
                print(f"Fecha inválida para la tarea {tarea['tarea']}.")
    with open(tareas_ruta, "w") as file:
        json.dump(tareas, file, indent=4)

def verificar_tareas_periodicamente():
    cargarTareas()
    verificar_tareas_para_correo()
    recargarInterfaz()
    app.after(60000, verificar_tareas_periodicamente)
    print("Verificado")
verificar_tareas_periodicamente()

frameBotones = customtkinter.CTkFrame(app, fg_color="transparent")
frameBotones.pack(anchor="se", side="bottom")
def eliminarTareasCompletadas():
    global tareas
    tareas = [t for t in tareas if t["completada"] != "Completada"]
    with open(tareas_ruta, "w") as file:
        json.dump(tareas, file, indent=4)
    recargarInterfaz()
eliminarBoton = customtkinter.CTkButton(frameBotones, text="Borrar tareas completadas", command=eliminarTareasCompletadas,
                                         width=50, height=40, fg_color="red", font=("Catamaran", 15), text_color="white", hover_color="red4")
eliminarBoton.pack(side="left", padx=5, pady=5)
buttonConfig = customtkinter.CTkButton(frameBotones, text="Configuracion", command=abrirConfig,
                                         width=50, height=40, fg_color="gray", font=("Catamaran", 15))
buttonConfig.pack(side="right", padx=5, pady=5)

cargarTareas()
app.mainloop()
