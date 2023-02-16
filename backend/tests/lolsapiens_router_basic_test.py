from backend.api.router.basic import basic_router
from fastapi.testclient import TestClient


class TestRootEndpoint:
    def test_root_returns_status_ok(self):
        client = TestClient(basic_router)
        response = client.get("/")
        content = response.json()
        assert response.status_code == 200
        assert "Status" in content
        assert content["Status"] == "OK 🗿"

    def test_root_returns_json_content_type(self):
        client = TestClient(basic_router)
        response = client.get("/")
        assert response.headers["Content-Type"] == "application/json"


class TestHealthCheckEndpoint:
    def test_health_check_returns_status_ok(self):
        client = TestClient(basic_router)
        response = client.get("/health-check")
        content = response.json()
        assert response.status_code == 200
        assert "Status" in content
        assert content["Status"] == "Running faster than iwi's brain"

    def test_health_check_returns_json_content_type(self):
        client = TestClient(basic_router)
        response = client.get("/health-check")
        assert response.headers["Content-Type"] == "application/json"
