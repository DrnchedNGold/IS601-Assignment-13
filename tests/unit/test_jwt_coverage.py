import pytest
from datetime import datetime, timezone
from app.auth import jwt
from app.schemas.token import TokenType
from uuid import uuid4

def test_create_token_error(monkeypatch):
    def fake_encode(*args, **kwargs):
        raise Exception("encode error")
    monkeypatch.setattr(jwt.jwt, "encode", fake_encode)
    with pytest.raises(Exception):
        jwt.create_token(str(uuid4()), TokenType.ACCESS)

def test_create_token_refresh(monkeypatch):
    # Test refresh token creation
    token = jwt.create_token(str(uuid4()), TokenType.REFRESH)
    assert isinstance(token, str)

def test_verify_password_and_hash():
    password = "TestPass123!"
    hashed = jwt.get_password_hash(password)
    assert jwt.verify_password(password, hashed)
    assert not jwt.verify_password("WrongPass", hashed)

import asyncio
from unittest.mock import AsyncMock, MagicMock

import os

import os

if "JPY_PARENT_PID" in os.environ or "VSCODE_PID" in os.environ:
    pytestmark = pytest.mark.skip("Skipping all async tests in VSCode/Jupyter environment")
