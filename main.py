from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import APIKeyHeader
from fastapi.templating import Jinja2Templates
from jinja2 import Template
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="templates")

######Pregunta 1: Creació API (2 punts)#####
#Escriu una API utilitzant FastAPI, amb endpoint (/info) que retorni informació amb les
#teves dades.

informacion = [
    {"Nombre": "Cristian Alexandru", "Apellido": "Cutar", "Dirección": "Camarles",}
]

@app.get("/info")
async def info():
    return {"informacion": informacion}


######Pregunta 2: Pydantic (5 punts)######
#A la mateixa api que hem creat a l’exercici anterior afegirem dos endpoints nous, un per a
#crear llibres amb els atributs (title, author i published_year) i un altre per poder-los
#recuperar a partir d’una id per exemple /books/{book_id}
#S’ha d’utilitzar pydantic per a validar el model de dades al crear el llibre. Podeu utilitzar un
#array per guardar els llibres i l’id pot ser directament l'índex de l’array per poder-lo
#recuperar.
#Amb l’endpoint per recuperar el llibre s’ha de mostrar els tres atributs prèviament
#comentats.

class Book(BaseModel):
    id: int
    title: str
    author: str
    publish_year: int

books = []

@app.post("/create_book/")
async def create_book(book: Book):
    books.append(book)
    return {"message": "El libro se ha creado", "book": book.dict()}

@app.get("/books/{book_id}")
async def get_book(book_id: int):
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Libro no encontrado")


######Pregunta 3: Plantilles Jinja (3 punts)#####
#Amb el json que trobareu a la mateixa tasca del moodle, mostreu una pàgina html
#utilitzant les plantilles Jinja.

@app.get("/display_game")
async def display_game(request: Request):
    return templates.TemplateResponse("juego.html"  )
