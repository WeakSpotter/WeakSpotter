from abc import ABC, abstractmethod
from typing import Any, List

from app.jobs.tools import add_data
from app.models.scan import Scan


class Job(ABC):
    requirements: List[str]  # List of required data keys
    key: str  # Unique key for the job
    name: str  # Human readable name of the job
    _scan: Scan  # The scan object
    _raw_output: Any  # Raw output of the job
    result: Any  # Parsed output of the job

    def scan(self, scan: Scan) -> None:
        self._scan = scan

        # Check if all required data is present
        for requirement in self.requirements:
            if not scan.data_dict.get(requirement):
                raise ValueError(f"Missing required data: {requirement}")

        # Run the scan
        self.run()

        # Parse the results
        self.parse_results()

        # Save the results
        add_data(scan, self.key, self.result)

    @abstractmethod
    def run(self) -> None:
        pass

    @abstractmethod
    def parse_results(self) -> None:
        pass

    @abstractmethod
    def score(self) -> float:
        """TODO: Return a score for the job."""
        pass

    @abstractmethod
    def definitions(self) -> dict:
        """TODO: Return a list of definitions for the job."""
        pass

    def __str__(self):
        return f"<{self.name} ({self.key}) reqs:{self.requirements}>"
