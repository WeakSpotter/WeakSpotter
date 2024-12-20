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

## How 2 Add a Job

```python
from app.jobs.abstract_job import Job

class CustomJob(Job):
    requirements: List[str] = ["domain"]  # Required data for the job
    key: str = "custom"  # Unique key for the job
    name: str = "Custom Job"  # Human readable name of the job

    def run(self) -> None:
        """Runs the scan, sets the `_raw_output` attribute"""
        self._raw_output: str = run_container(
            "image_name",
            f"command {self._scan.data['domain']}"
        )

    def parse_results(self) -> None:
        """Parses the raw output and sets the `result` attribute"""
        self.result = [x for x in self._raw_output.split("\n") if x]    # Example of parsing the output, do your thing here

    def score(self) -> float:
        """Calculates the score based on the job data"""
        job_data = self._scan.data[self.key]

        # Calculate the score based on the job data

        return score
```

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLModel](https://sqlmodel.tiangolo.com/)
