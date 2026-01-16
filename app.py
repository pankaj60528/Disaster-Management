import sys, subprocess, os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from backend.ml_model import load_model
from backend.routes import report, sos

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_model()
    # Note: Ye subprocess background me chalega, par production me 
    # agar frontend iske port (e.g. 5002) par request karega to wo fail ho sakta hai.
    # Filhal deploy fix karne ke liye hum isse aise hi rakhenge.
    subprocess.Popen([sys.executable, "backend/ML/disaster_response_api.py"])
    yield
    print("🛑 Application shutting down")

app = FastAPI(
    title="Disaster Tweet Classifier API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(report.router)
app.include_router(sos.router)

if __name__ == "__main__":
    import uvicorn
    # Render automatically PORT provide karta hai, agar nahi mila to 8000 use karega
    port = int(os.environ.get("PORT", 8000))
    
    # 0.0.0.0 is VERY IMPORTANT for Render
    print(f"🚀 Starting server on 0.0.0.0:{port}")
    uvicorn.run(app, host="0.0.0.0", port=port)