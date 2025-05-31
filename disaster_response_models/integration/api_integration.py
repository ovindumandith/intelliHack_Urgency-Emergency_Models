from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from model_loader import DisasterModelLoader
import uvicorn

app = FastAPI(title="Disaster Response AI API")
model_loader = None

class TextRequest(BaseModel):
    text: str

@app.on_event("startup")
async def startup_event():
    global model_loader
    model_loader = DisasterModelLoader()
    model_loader.load_models()

@app.get("/")
async def root():
    return {"message": "Disaster Response AI API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    if model_loader is None:
        raise HTTPException(status_code=503, detail="Models not initialized")
    return {"status": "healthy"}

@app.post("/classify/emergency")
async def classify_emergency(request: TextRequest):
    if model_loader is None:
        raise HTTPException(status_code=503, detail="Models not initialized")
    result = model_loader.classify_emergency(request.text)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@app.post("/analyze/request")
async def analyze_request(request: TextRequest):
    if model_loader is None:
        raise HTTPException(status_code=503, detail="Models not initialized")
    return model_loader.analyze_request(request.text)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
