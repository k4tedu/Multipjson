from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from multipjson.generate_json import generate_data

app = FastAPI()

@app.post("/api/generate")
async def generate_json(request: Request):
    try:
        data = await request.json()
        json_array = generate_data(data)
        return JSONResponse(content=json_array)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}
