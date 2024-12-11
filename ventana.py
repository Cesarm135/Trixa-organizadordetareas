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



frame1 = tk.Frame(ventana)
frame1.configure(width=300, height=200, bg="red", bd= "5") 
frame2 = tk.Frame(frame1)
frame2.configure(width=50, height=50, bg="yellow", bd= "5") 
boton = tk.button(frame2, text="hola")
frame2.pack()
frame1.pack()






ventana.mainloop()