import json
import tkinter as tk
from tkinter import *

while True:
    print("1: Añadir Tarea, 2: Eliminar Tarea, 3: Ver Tareas, 4. Salir")
    userModeInput = input("Seleccionar el modo: ")
    
    if userModeInput == "1":
        inputTareaAAnadir = input("Ingresar la tarea: ")
    
        try:
            with open("config.json", "r") as f:
                config = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            config = {"numero": 0} 
    
        numero_actual = config.get("numero", 0)  
    
    
        numero_actual += 1
        config["numero"] = numero_actual
    
        
        with open("config.json", "w") as f:
            json.dump(config, f, indent=4)
    
        tareaAAnadir = {
            "name": inputTareaAAnadir,
            "estado": "Pendiente",
            "numero": numero_actual
        }
    
        try:
            with open("tareas.json", "r") as f:
                tareas = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            tareas = []  
    
        tareas.append(tareaAAnadir)
    
        with open("tareas.json", "w") as f:
            json.dump(tareas, f, indent=4)
    
        print("Listo, se ha añadido la tarea:", inputTareaAAnadir)
    
    elif userModeInput == "2":
        try:
            with open("tareas.json", "r") as f:
                tareas = json.load(f)
    
            if not tareas:
                print("No hay tareas para eliminar.")
            else:
                for tarea in tareas:
                    print(f"{tarea['numero']}: {tarea['name']}")
    
                numero_a_eliminar = int(input("Número de la tarea a eliminar: "))
    
        
                tarea_encontrada = None
                for tarea in tareas:
                    if tarea["numero"] == numero_a_eliminar:
                        tarea_encontrada = tarea
                        break
    
                if tarea_encontrada:
                    tareas.remove(tarea_encontrada)  
                    with open("tareas.json", "w") as f:
                        json.dump(tareas, f, indent=4)   
                    print(f"Tarea '{tarea_encontrada['name']}' eliminada con éxito.")
                else:
                    print("No se encontró una tarea con ese número.")
        except FileNotFoundError:
            print("El archivo de tareas no existe. No hay tareas para eliminar.")
        except ValueError:
            print("Por favor, ingrese un número válido.")
        except json.JSONDecodeError:
            print("El archivo de tareas está vacío o corrupto.")
                
                
    elif userModeInput == "3":
        try:
            with open("tareas.json", "r") as f:
                tareas = json.load(f)
                for tarea in tareas:
                    print(f"{tarea['numero']}: {tarea['name']} - {tarea['estado']}")
        except FileNotFoundError:
            print("No hay tareas registradas.")
        else:
            print("Opción no válida.")
    elif userModeInput == "4":
        print("Se ha salido.") 
        exit()