from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from .database import create_db_and_tables
from .routes import scan, user, version

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(version.router, prefix="/api")
app.include_router(scan.router, prefix="/api")
app.include_router(user.router, prefix="/api")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
async def root():
    # Redirect to the API documentation
    return RedirectResponse(url="/docs")
