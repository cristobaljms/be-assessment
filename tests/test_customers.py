from datetime import datetime

import pytest
from fastapi.testclient import TestClient


def create_customer(
    client: TestClient,
    *,
    name: str = "Juan Pérez",
    email: str = "juan@example.com",
) -> dict[str, object]:
    response = client.post("/customers", json={"name": name, "email": email})
    assert response.status_code == 201
    return response.json()


def test_health_check(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_customer_normalizes_input_and_defaults_to_pending(client: TestClient) -> None:
    response = client.post(
        "/customers",
        json={"name": "  Juan Pérez  ", "email": "  JUAN@EXAMPLE.COM  "},
    )

    assert response.status_code == 201
    customer = response.json()
    assert customer["id"] == 1
    assert customer["name"] == "Juan Pérez"
    assert customer["email"] == "juan@example.com"
    assert customer["status"] == "PENDING"
    assert datetime.fromisoformat(customer["created_at"]).tzinfo is not None


def test_rejects_duplicate_email_case_insensitively(client: TestClient) -> None:
    create_customer(client, email="Customer@Example.com")

    response = client.post(
        "/customers",
        json={"name": "Another customer", "email": "customer@example.com"},
    )

    assert response.status_code == 409
    assert response.json() == {"detail": "A customer with this email already exists."}


@pytest.mark.parametrize(
    "payload",
    [
        {"name": "Juan Pérez", "email": "not-an-email"},
        {"name": "   ", "email": "juan@example.com"},
        {"name": "Juan Pérez", "email": "juan@example.com", "unknown": True},
    ],
)
def test_rejects_invalid_customer_payloads(
    client: TestClient,
    payload: dict[str, object],
) -> None:
    response = client.post("/customers", json=payload)

    assert response.status_code == 422


def test_lists_customers_and_filters_by_status(client: TestClient) -> None:
    first = create_customer(client, name="Ana López", email="ana@example.com")
    second = create_customer(client, name="Luis Díaz", email="luis@example.com")
    client.patch(f"/customers/{first['id']}/status", json={"status": "ACTIVE"})
    client.patch(f"/customers/{second['id']}/status", json={"status": "BLOCKED"})

    all_response = client.get("/customers")
    active_response = client.get("/customers", params={"status": "ACTIVE"})
    pending_response = client.get("/customers", params={"status": "PENDING"})

    assert all_response.status_code == 200
    assert len(all_response.json()) == 2
    assert [customer["email"] for customer in active_response.json()] == ["ana@example.com"]
    assert pending_response.json() == []


def test_rejects_invalid_status_filter(client: TestClient) -> None:
    response = client.get("/customers", params={"status": "UNKNOWN"})

    assert response.status_code == 422


def test_gets_existing_customer_and_returns_404_for_missing_customer(client: TestClient) -> None:
    created = create_customer(client)

    existing_response = client.get(f"/customers/{created['id']}")
    missing_response = client.get("/customers/999")

    assert existing_response.status_code == 200
    assert existing_response.json() == created
    assert missing_response.status_code == 404
    assert missing_response.json() == {"detail": "Customer 999 was not found."}


def test_updates_customer_status(client: TestClient) -> None:
    created = create_customer(client)

    response = client.patch(
        f"/customers/{created['id']}/status",
        json={"status": "ACTIVE"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "ACTIVE"


def test_rejects_invalid_status_update(client: TestClient) -> None:
    created = create_customer(client)

    response = client.patch(
        f"/customers/{created['id']}/status",
        json={"status": "UNKNOWN"},
    )

    assert response.status_code == 422


def test_returns_404_when_updating_missing_customer(client: TestClient) -> None:
    response = client.patch("/customers/999/status", json={"status": "ACTIVE"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Customer 999 was not found."}
