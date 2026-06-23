from decimal import Decimal

from fastapi.testclient import TestClient

from apps.api.app.main import app

client = TestClient(app)


def test_order_item_payload_accepts_camel_case() -> None:
    payload = {
        "customerName": "Cliente Teste",
        "customerPhone": "+55 48 99999-0000",
        "customerEmail": "cliente@example.com",
        "deliveryType": "pickup",
        "pickupPoint": "UFSC",
        "items": [
            {
                "itemType": "product",
                "productId": "00000000-0000-0000-0000-000000000001",
                "quantity": "1",
            },
        ],
    }

    # This test validates request-shape compatibility. It may return 400
    # because the product does not exist in the in-memory test DB.
    response = client.post("/api/orders", json=payload)
    assert response.status_code in {201, 400}


def test_stock_adjustment_shape_accepts_camel_case() -> None:
    payload = {"quantityDelta": "1", "reason": "test"}

    response = client.patch(
        "/api/admin/products/00000000-0000-0000-0000-000000000001/stock",
        json=payload,
    )
    assert response.status_code in {200, 400}


def test_admin_product_create_accepts_camel_case() -> None:
    payload = {
        "name": "QA Produto API",
        "description": "Teste",
        "category": "hortifruti",
        "unit": "unidade",
        "price": "5.50",
        "stockQuantity": "3",
        "imageUrl": "",
        "isActive": True,
    }

    response = client.post("/api/admin/products", json=payload)
    assert response.status_code in {201, 400}


def test_admin_product_update_accepts_camel_case() -> None:
    payload = {
        "category": "frutas",
        "stockQuantity": "8",
        "isActive": True,
    }

    response = client.patch(
        "/api/admin/products/00000000-0000-0000-0000-000000000001",
        json=payload,
    )
    assert response.status_code in {200, 400, 404}
