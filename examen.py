# Importa las clases y funciones necesarias de los módulos FastAPI, Pydantic, y Jinja2.
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import APIKeyHeader
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

# Define una clave API para proteger ciertas rutas.
API_KEY = "my_api_key"
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

# Crea una instancia de la aplicación FastAPI.
# Configura el manejador de plantillas Jinja2 y establece el directorio de plantillas en "templates".
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Define dos modelos Pydantic (Item y ParCheck) que se utilizan para validar la entrada de datos en las rutas.
class Item(BaseModel):
    name: str
    description: str = None

class ParCheck(BaseModel):
    number: int

# Crea dos variables globales (last_item y last_number) para almacenar el último Item creado y el último número verificado.
last_item: Item = None
last_number: int = None

# Define una ruta POST "/create_item/" que recibe datos de tipo Item y almacena el último Item creado.
@app.post("/create_item/")
async def create_item(item: Item):
    global last_item
    last_item = item
    return {"message": "Item creado correctamente"}

# Define una ruta POST "/check_par/" que recibe datos de tipo ParCheck,
# verifica si el número es par o impar, y almacena el último número verificado.
@app.post("/check_par/", response_model=dict)
async def check_par(par_check: ParCheck):
    global last_number
    last_number = par_check.number
    return {"message": "Número es par" if par_check.number % 2 == 0 else "Número es impar"}

# Define una ruta GET "/show_data/" que muestra los datos almacenados (last_item y last_number) utilizando una plantilla HTML.
@app.get("/show_data/", response_class=HTMLResponse)
async def show_data(request: Request):
    return templates.TemplateResponse("show_data.html", {"request": request, "last_item": last_item, "last_number": last_number})

# Define una ruta GET "/protected/" que requiere una clave API para acceder.
@app.get("/protected/")
async def protected(api_key: str = Depends(api_key_header)):
    return {"message": "Esta es la ruta protegida"}



#####Ejercicio1#####

#Crea un modelo Pydantic llamado User con campos username (str) y email (str).
#Crea una ruta /create_user que reciba datos de tipo User mediante un método POST.
#Implementa la validación usando Pydantic para asegurarte de que username y email sean proporcionados y cumplan con las #restricciones adecuadas.

class User (BaseModel) :
    username: str
    email: str
    
@app.post("/create_user/")
async def create_user(user: User):
    return {"message": "El usuario se ha creado correctamente", "user": user.dict()}


#####Ejercicio2#####

#Crea una lista llamada tasks que contenga diccionarios representando tareas, cada uno con campos como id (int), description #(str), y completed (bool).
#Crea una ruta /get_tasks que devuelva la lista completa de tareas.
#Crea una ruta /get_task/{task_id} que devuelva la información de una tarea específica según el ID proporcionado.

tasks = [
    {"id": 1, "description": "Hacer la compra", "completed": False},
    {"id": 2, "description": "Estudiar para el examen", "completed": True},
]

@app.get("/get_tasks")
async def get_tasks():
    return {"tasks": tasks}

    

@app.get("/get_task/{task_id}")
async def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Tarea no encontrada")




####Ejercicio3####

#Crea un archivo HTML llamado display_user.html.
#En este archivo, utiliza Jinja para mostrar la información de un usuario (nombre de usuario y correo electrónico) #pasada desde la ruta.
#Crea una ruta /display_user que renderice este template con datos de usuario ficticios.

@app.get("/display_user")
async def display_user(request: Request):
    user_data = {"username": "JohnDoe", "email": "john.doe@example.com"}
    return templates.TemplateResponse("display_user.html", {"request": request, "user": user_data})
 