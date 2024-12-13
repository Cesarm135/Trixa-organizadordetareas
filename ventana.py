import tkinter as tk
from tkinter import PhotoImage
from pathlib import Path
import time
ventana = tk.Tk()

ventana.title("To-DoList PAI")
ventana.geometry("540x540")
ventana.minsize(width=540, height=540)
icono_ruta = Path(__file__).parent / "Media" / "icono.png"
icono = PhotoImage(file=str(icono_ruta))
ventana.iconphoto(False, icono)
ventana.configure(bg="white")

Numero = 1

etiqueta = tk.Label(ventana, text=Numero)
etiqueta.configure(fg="black", bg="white", font=("Arial", 34, "bold"))
etiqueta.after(1000)
etiqueta.pack()



def botonPress():
    print("Hola")
    global Numero
    Numero += 2

    etiqueta.configure(text=Numero)

boton = tk.Button(text="Hola", bg="green", fg="white", font=("Arial", 24))
boton.configure(command=botonPress)


boton.pack()


ventana.mainloop()