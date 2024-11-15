# WeakSpotter Backend

## How 2 Run

First install the dependencies:

```bash
pip install -r requirements.txt
```

Then run the application:

```bash
fastapi dev backend/app/main.py
```

## How 2 Build

To build the docker image:

```bash
docker build -t weakspotter-back .
```

Or be a *respectable human being* and use the `docker-compose.yml` file [here](../docker-compose.yml).

## API Documentation

Once the application is running, you can access the automatic API documentation at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Environment Variables

- `SQLITE_PATH`: Path to SQLite database file (default: "database.db")

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLModel](https://sqlmodel.tiangolo.com/)
