from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from generate_json import generate_data
from uuid import uuid4
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "../templates")
STATIC_DIR = os.path.join(BASE_DIR, "../static")

templates = Jinja2Templates(directory=TEMPLATES_DIR)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# In-memory cache for generated JSON (temporary for each session)
raw_json_store = {}

@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate", response_class=HTMLResponse)
async def generate_json(
    request: Request,
    fields: str = Form(...),
    id_option: str = Form("uuid"),
    phone_option: str = Form("random"),
    email_domain: str = Form("demo.org")
):
    try:
        fields_list = [field.strip() for field in fields.split(",") if field.strip()]
        json_data = generate_data(fields_list, id_option, phone_option, email_domain)

        # Generate unique key for this JSON result
        json_key = str(uuid4())
        raw_json_store[json_key] = json_data

        return templates.TemplateResponse("result.html", {
            "request": request,
            "json_data": json_data,
            "json_key": json_key
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/view_raw/{json_key}", response_class=JSONResponse)
async def view_raw_json(json_key: str):
    data = raw_json_store.get(json_key)
    if not data:
        return JSONResponse(status_code=404, content={"error": "JSON not found"})
    return JSONResponse(content=data)
