"""
CropShield Backend API Entrypoint
"""

from fastapi import FastAPI

app = FastAPI(
    title="CropShield API",
    description="Backend API for CropShield ML and Monitoring Services",
    version="0.1.0"
)

@app.get("/")
def read_root():
    return {"status": "online", "message": "CropShield API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
