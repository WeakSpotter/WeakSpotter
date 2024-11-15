# WeakSpotter Backend

## Prerequisites

```bash
pip install -r requirements.txt
```

## Running the Application

### Development Mode
```bash
fastapi dev backend/app/main.py
```

## API Documentation

Once the application is running, you can access the automatic API documentation at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Environment Variables

- `SQLITE_PATH`: Path to SQLite database file (default: "database.db")

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLModel](https://sqlmodel.tiangolo.com/)
