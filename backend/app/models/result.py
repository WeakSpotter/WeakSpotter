from enum import IntEnum
from typing import TYPE_CHECKING, Optional

from app.ai import create_custom_vulnerability
from sqlmodel import Field, Relationship, Session, SQLModel

if TYPE_CHECKING:
    from .scan import Scan


class Severity(IntEnum):
    debug = 0
    info = 1
    warning = 2
    error = 3
    critical = 4


class Category(IntEnum):
    unknown = 0


class Result(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    severity: Severity = Severity.info
    score: int = 0
    category: Category = Category.unknown
    short_description: str = ""
    description: str = ""
    recommendation: str = ""

    # Add these lines to create the relationship with Scan
    scan_id: Optional[int] = Field(default=None, foreign_key="scan.id")
    scan: Optional["Scan"] = Relationship(back_populates="results")

    def gen(self, session: Session):
        """
        Modifies the result object and persists changes to the database.

        Args:
            session (Session): SQLModel session for database operations

        Returns:
            Self: Returns the modified result object

        Example:
            result = Result(title="Test")
            result.gen(session).severity = Severity.critical
        """
        print(f"Generating result for {self.title}")
        if not self.id:
            session.add(self)

        if self.description and self.recommendation:
            return

        vulg = create_custom_vulnerability(f"{self.title} - {self.short_description}")

        if not vulg:
            return

        try:
            self.description = vulg["Vulgarization"]
            self.recommendation = vulg["Solution"]
        except KeyError:
            print("Vulgarization or Solution not found in the custom vulnerability.")
            return
        except Exception as e:
            print(f"Error getting custom vulnerability: {e}")
            return

        session.commit()
        session.refresh(self)
        return self
