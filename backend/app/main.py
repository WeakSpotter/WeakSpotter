from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from .routes import scan
from .database import create_db_and_tables

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(scan.router, prefix="/api")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
async def root():
    # Redirect to the API documentation
    return RedirectResponse(url="/docs")
