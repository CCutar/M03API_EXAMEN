from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Definir modelo Pydantic para validación
class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

# Endpoint para devolver un template HTML
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Endpoint para validación con Pydantic
@app.post("/items/")
async def create_item(item: Item):
    return item

# Endpoint para pasar un parámetro
@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
