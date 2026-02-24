import enum
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ResultStatus(str, enum.Enum):
    passed = "passed"
    failed = "failed"
    skipped = "skipped"
    blocked = "blocked"
    error = "error"


class TestResult(Base):
    __tablename__ = "test_results"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    status: Mapped[ResultStatus] = mapped_column(Enum(ResultStatus), nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)        # failure notes, observations
    duration_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)  # execution time in ms
    executed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # FK → test_runs
    run_id: Mapped[int] = mapped_column(ForeignKey("test_runs.id"), nullable=False)
    run: Mapped["TestRun"] = relationship(back_populates="results")  # type: ignore[name-defined]  # noqa: F821

    # FK → test_cases
    test_case_id: Mapped[int] = mapped_column(ForeignKey("test_cases.id"), nullable=False)
    test_case: Mapped["TestCase"] = relationship(back_populates="results")  # type: ignore[name-defined]  # noqa: F821
