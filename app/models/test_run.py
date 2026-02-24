import enum
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class RunStatus(str, enum.Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    aborted = "aborted"


class TestRun(Base):
    __tablename__ = "test_runs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[RunStatus] = mapped_column(Enum(RunStatus), default=RunStatus.pending, nullable=False)

    # Optional FK — a run may cover a full suite or be ad-hoc
    suite_id: Mapped[int | None] = mapped_column(ForeignKey("test_suites.id"), nullable=True)
    suite: Mapped["TestSuite | None"] = relationship(back_populates="test_runs")  # type: ignore[name-defined]  # noqa: F821

    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # One run → many individual test results
    results: Mapped[list["TestResult"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        back_populates="run", cascade="all, delete-orphan"
    )
