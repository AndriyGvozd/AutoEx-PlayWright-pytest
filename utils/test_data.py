import os
import time
import uuid


def unique_user_data() -> dict:
    # A millisecond timestamp alone can collide when tests run in parallel
    # (pytest-xdist workers can generate one in the same millisecond), so mix
    # in the worker id and a short random suffix to guarantee uniqueness
    # across concurrent processes, not just across time.
    timestamp = int(time.time() * 1000)
    worker_id = os.environ.get("PYTEST_XDIST_WORKER", "master")
    unique_suffix = f"{worker_id}{uuid.uuid4().hex[:6]}"
    return {
        "name": f"Test User {timestamp}{unique_suffix}",
        "email": f"testuser{timestamp}{unique_suffix}@example.com",
        "title": "Mr",
        "password": "Passw0rd!123",
        "day": "10",
        "month": "5",
        "year": "1995",
        "first_name": "Test",
        "last_name": "User",
        "company": "TestCo",
        "address1": "123 Test Street",
        "address2": "Apt 4",
        "country": "United States",
        "state": "California",
        "city": "Los Angeles",
        "zipcode": "90001",
        "mobile_number": "1234567890",
    }
