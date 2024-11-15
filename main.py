import json

print("1: Añadir Tarea, 2: Eliminar Tarea, 3: Ver Tareas")
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
    print("Tareas:")
    
    try:
        with open("tareas.json", "r") as f:
            tareas = json.load(f)
            for tarea in tareas:
                print(f"{tarea['numero']}: {tarea['name']}")
    except FileNotFoundError:
        print("No hay tareas registradas.")
    except json.JSONDecodeError:
        print("El archivo de tareas está vacío o tiene un formato inválido.")

    userdelete = input("Elige el numero de una tarea:")
    
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
