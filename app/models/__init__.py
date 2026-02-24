# Import all models here so Alembic and Base.metadata.create_all() can find them
from app.models.user import User          # noqa: F401
from app.models.test_suite import TestSuite   # noqa: F401
from app.models.test_case import TestCase     # noqa: F401
from app.models.test_run import TestRun       # noqa: F401
from app.models.test_result import TestResult # noqa: F401
