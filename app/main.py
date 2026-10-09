from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router as advertisement_router

app = FastAPI(
    title="Classified Ads Service",
    description="A simple classified ads API with in-memory storage.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(advertisement_router, prefix="/advertisement")


@app.get("/")
def root():
    return {"message": "Classified Ads Service is running"}
