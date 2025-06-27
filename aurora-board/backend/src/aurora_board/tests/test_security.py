import pytest
from jose import jwt
from datetime import timedelta, datetime, timezone

from aurora_board import security # Assuming aurora_board is in PYTHONPATH or structure allows this import
# If not, adjust to: from .. import security or from aurora_board.security import ...

def test_hash_password():
    password = "testpassword"
    hashed_password = security.hash_password(password)
    assert hashed_password != password
    assert security.verify_password(password, hashed_password)

def test_verify_password():
    password = "testpassword"
    hashed_password = security.hash_password(password)
    assert security.verify_password(password, hashed_password)
    assert not security.verify_password("wrongpassword", hashed_password)

def test_create_access_token():
    data = {"sub": "testuser"}
    token = security.create_access_token(data)

    decoded_payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
    assert decoded_payload["sub"] == "testuser"
    assert "exp" in decoded_payload

    # Check expiration time roughly
    expected_exp = datetime.now(timezone.utc) + timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    actual_exp_timestamp = decoded_payload["exp"]
    actual_exp_datetime = datetime.fromtimestamp(actual_exp_timestamp, tz=timezone.utc)

    # Allow a small delta for time differences during test execution
    assert abs((actual_exp_datetime - expected_exp).total_seconds()) < 5

def test_create_access_token_custom_expiry():
    data = {"sub": "testuser_custom_exp"}
    custom_delta = timedelta(hours=1)
    token = security.create_access_token(data, expires_delta=custom_delta)

    decoded_payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
    assert decoded_payload["sub"] == "testuser_custom_exp"

    expected_exp = datetime.now(timezone.utc) + custom_delta
    actual_exp_timestamp = decoded_payload["exp"]
    actual_exp_datetime = datetime.fromtimestamp(actual_exp_timestamp, tz=timezone.utc)

    assert abs((actual_exp_datetime - expected_exp).total_seconds()) < 5

# Note: Testing get_current_user directly as a unit test is more complex
# as it involves FastAPI's dependency injection and database interaction.
# It's typically tested via integration tests on protected endpoints.
# If you need to unit test parts of its logic, you might refactor it
# to separate the token decoding from the database call, and test decoding logic here.
# For instance, a helper function like `decode_token(token: str) -> dict` could be unit tested.
# Then `get_current_user` would use this helper and its database part would be mocked or integration tested.

# For now, this covers the core security utilities.
# Tests for get_current_user will be part of endpoint tests.
