import pytest
from unittest.mock import AsyncMock, patch
from app.auth import redis as redis_mod

import os

if "JPY_PARENT_PID" in os.environ or "VSCODE_PID" in os.environ:
    pytestmark = pytest.mark.skip("Skipping all async tests in VSCode/Jupyter environment")
