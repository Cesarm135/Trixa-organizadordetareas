import json
print("1: Añadir Tarea, 2: Eliminar Tarea, 3: Ver Tareas")
userModeInput = input("Seleccionar el modo: ")
inputTareaAAnadir = ""
tareaAAnadir = ""
tareaAAnadirJSON = ""

if (userModeInput == "1"):
  inputTareaAAnadir = input("Ingresar la tarea: ")
  tareaAAnadir = {"name": inputTareaAAnadir,
                  "estado: ": "Pendiente"}
  tareaAAnadirJSON = json.dumps(tareaAAnadir)
  f = open("tareas.json", "a")
  f.write(" \n " + tareaAAnadirJSON)
  f = open("tareas.json", "r")
  print("Listo, se ha añadido la tarea: " + inputTareaAAnadir)
elif (userModeInput == "2"):
  listNumber = 0
  f = open("tareas.txt", "r")
  print
  
  

  
  