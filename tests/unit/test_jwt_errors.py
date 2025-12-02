import pytest
from app.auth import jwt as jwt_module
from app.schemas.token import TokenType
from uuid import uuid4
from jose import jwt as jose_jwt
from fastapi import HTTPException
import secrets

def test_create_token_exception(monkeypatch):
    # Simulate jwt.encode raising an exception
    monkeypatch.setattr("app.auth.jwt.jwt.encode", lambda *a, **kw: (_ for _ in ()).throw(Exception("fail")))
    with pytest.raises(HTTPException) as exc:
        jwt_module.create_token(str(uuid4()), TokenType.ACCESS)
    assert exc.value.status_code == 500
    assert "Could not create token" in str(exc.value.detail)
