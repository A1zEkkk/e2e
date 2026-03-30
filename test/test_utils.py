import pytest
from core.utils import hash_password, verify_password

@pytest.mark.parametrize("password", [
    "123",
    "hello",
    "long_password_123",
    "слово",
])
def test_passwords(password):
    hashed = hash_password(password)

    assert verify_password(password, hashed)
    assert not verify_password(password + "x", hashed)