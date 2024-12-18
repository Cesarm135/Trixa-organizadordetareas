import tkinter as tk
from tkinter import PhotoImage
from pathlib import Path
import time
import customtkinter

ventana = customtkinter.CTk()

# Ajustes Ventana
#customtkinter.set_appearance_mode("System")
ventana.title("To-DoList PAI")
customtkinter.set_default_color_theme("blue")
ventana.configure(fg_color='gray88')
ventana.geometry("675x375")
ventana.minsize(width=675, height=375)
icono_ruta = Path(__file__).parent / "Media" / "icono.ico"
ventana.after(201, lambda :ventana.iconbitmap(icono_ruta))
customtkinter.set_appearance_mode("System")


entry = customtkinter.CTkEntry(ventana, placeholder_text="Tarea", width="100")
entry.pack()

ventana.mainloop()