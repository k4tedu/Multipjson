from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from multipjson.generate_json import build_json_array
import os, json

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def form_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/", response_class=HTMLResponse)
async def handle_form(
    request: Request,
    total: int = Form(...),
    fields: str = Form(...),
    values: str = Form(...),
    prefix: str = Form(""),
    suffix: str = Form(""),
    id_type: str = Form("normal"),
    email_domain: str = Form("demo.org"),
    phone_digits: int = Form(12)
):
    try:
        json_data = build_json_array(
            total=total,
            fields=fields,
            values=values,
            prefix=prefix,
            suffix=suffix,
            id_type=id_type,
            email_domain=email_domain,
            phone_digits=phone_digits
        )
        os.makedirs("static", exist_ok=True)
        with open("static/web_output.json", "w") as f:
            json.dump(json_data, f, indent=2)

        return templates.TemplateResponse("result.html", {"request": request, "data": json_data})
    except Exception as e:
        return HTMLResponse(f"<h3>Error: {str(e)}</h3>")

@app.get("/static/web_output.json", response_class=FileResponse)
async def get_raw_json():
    return "static/web_output.json"
