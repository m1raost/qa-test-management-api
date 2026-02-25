import enum
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Priority(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class Severity(str, enum.Enum):
    trivial = "trivial"
    minor = "minor"
    major = "major"
    critical = "critical"
    blocker = "blocker"


class CaseStatus(str, enum.Enum):
    draft = "draft"
    active = "active"
    deprecated = "deprecated"


class TestCase(Base):
    __tablename__ = "test_cases"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    steps: Mapped[str | None] = mapped_column(Text, nullable=True)
    expected_result: Mapped[str | None] = mapped_column(Text, nullable=True)
    priority: Mapped[Priority] = mapped_column(Enum(Priority), default=Priority.medium, nullable=False)
    severity: Mapped[Severity] = mapped_column(Enum(Severity), default=Severity.major, nullable=False)
    status: Mapped[CaseStatus] = mapped_column(Enum(CaseStatus), default=CaseStatus.draft, nullable=False)
    suite_id: Mapped[int] = mapped_column(ForeignKey("test_suites.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    suite: Mapped["TestSuite"] = relationship(back_populates="test_cases")  # type: ignore[name-defined]  # noqa: F821
    results: Mapped[list["TestResult"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        back_populates="test_case", cascade="all, delete-orphan"
    )
