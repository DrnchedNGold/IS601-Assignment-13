import pytest
from app.models.user import User
import uuid

class DummyDB:
    def __init__(self, users=None):
        self._users = users or []
        self.added = []
    def query(self, cls):
        class Query:
            def __init__(self, users):
                self._users = users
            def filter(self, *args, **kwargs):
                return self
            def first(self):
                return self._users[0] if self._users else None
        return Query(self._users)
    def add(self, user):
        self.added.append(user)
    def flush(self):
        pass

def test_register_short_password():
    db = DummyDB()
    user_data = {
        "first_name": "A",
        "last_name": "B",
        "email": "a@b.com",
        "username": "ab",
        "password": "123"
    }
    with pytest.raises(ValueError, match="at least 6 characters"):
        User.register(db, user_data)

def test_register_long_password():
    db = DummyDB()
    user_data = {
        "first_name": "A",
        "last_name": "B",
        "email": "a@b.com",
        "username": "ab",
        "password": "x" * 73
    }
    with pytest.raises(ValueError, match="longer than 72"):
        User.register(db, user_data)

def test_register_duplicate_user():
    dummy_user = object()
    db = DummyDB(users=[dummy_user])
    user_data = {
        "first_name": "A",
        "last_name": "B",
        "email": "a@b.com",
        "username": "ab",
        "password": "123456"
    }
    with pytest.raises(ValueError, match="already exists"):
        User.register(db, user_data)

def test_verify_token_invalid():
    assert User.verify_token("invalid.token") is None

def test_verify_token_invalid_uuid(monkeypatch):
    # Patch jose.jwt.decode to return a payload with invalid UUID
    def fake_decode(token, key, algorithms):
        return {"sub": "not-a-uuid"}
    monkeypatch.setattr("jose.jwt.decode", fake_decode)
    monkeypatch.setattr("app.models.user.settings", type("S", (), {"JWT_SECRET_KEY": "key", "ALGORITHM": "HS256"})())
    assert User.verify_token("token") is None
