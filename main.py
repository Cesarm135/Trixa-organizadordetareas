import tkinter as tk
from tkinter import PhotoImage
from pathlib import Path


ventana = tk.Tk()

ventana.title("To-DoList PAI")
ventana.geometry("540x540")
ventana.minsize(width=540, height=540)
icono_ruta = Path(__file__).parent / "Media" / "icono.png"
icono = PhotoImage(file=str(icono_ruta))
ventana.iconphoto(False, icono)
ventana.configure(bg="white")
ventana.mainloop()
