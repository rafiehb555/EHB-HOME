import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import httpx

from app.main import app


client = TestClient(app)


class TestServiceIntegration:
    @patch("httpx.AsyncClient.get")
    def test_pss_service_health(self, mock_get):
        """Test PSS service health check"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "healthy"}
        mock_get.return_value = mock_response

        response = client.get("/api/v1/services/pss/health")
        assert response.status_code == 200

    @patch("httpx.AsyncClient.get")
    def test_emo_service_health(self, mock_get):
        """Test EMO service health check"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "healthy"}
        mock_get.return_value = mock_response

        response = client.get("/api/v1/services/emo/health")
        assert response.status_code == 200

    @patch("httpx.AsyncClient.get")
    def test_edr_service_health(self, mock_get):
        """Test EDR service health check"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "healthy"}
        mock_get.return_value = mock_response

        response = client.get("/api/v1/services/edr/health")
        assert response.status_code == 200

    def test_get_all_services_health(self):
        """Test getting health of all services"""
        response = client.get("/api/v1/services/health")
        assert response.status_code == 200

        data = response.json()
        assert "total_services" in data
        assert "healthy_services" in data
        assert "unhealthy_services" in data
        assert "services" in data

    def test_get_available_services(self):
        """Test getting available services list"""
        response = client.get("/api/v1/services/available-services")
        assert response.status_code == 200

        data = response.json()
        assert "services" in data
        assert len(data["services"]) > 0

        # Check if expected services are present
        service_names = [service["name"] for service in data["services"]]
        expected_services = [
            "pss",
            "emo",
            "edr",
            "jps",
            "gosellr",
            "wallet",
            "ai-agent",
            "ai-robot",
        ]

        for expected_service in expected_services:
            assert expected_service in service_names

    def test_get_service_health_invalid_service(self):
        """Test getting health of invalid service"""
        response = client.get("/api/v1/services/invalid-service/health")
        assert response.status_code == 404

    @patch("httpx.AsyncClient.get")
    def test_get_service_profile(self, mock_get):
        """Test getting service profile"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "user_id": 1,
            "verification_status": "verified",
            "security_score": 95,
        }
        mock_get.return_value = mock_response

        # Mock authentication
        with patch("api.v1.services.get_current_user") as mock_auth:
            mock_user = MagicMock()
            mock_user.id = 1
            mock_auth.return_value = mock_user

            response = client.get("/api/v1/services/pss/profile/1")
            assert response.status_code == 200

    @patch("httpx.AsyncClient.post")
    def test_verify_with_service(self, mock_post):
        """Test verification with service"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "verification_id": "TEST_001",
            "status": "verified",
            "score": 95,
        }
        mock_post.return_value = mock_response

        # Mock authentication
        with patch("api.v1.services.get_current_user") as mock_auth:
            mock_user = MagicMock()
            mock_user.id = 1
            mock_auth.return_value = mock_user

            verification_data = {
                "document_type": "id_card",
                "document_data": "test_data",
                "verification_method": "document_upload",
            }

            response = client.post(
                "/api/v1/services/pss/verify", json=verification_data
            )
            assert response.status_code == 200

    def test_verify_with_invalid_service(self):
        """Test verification with invalid service"""
        # Mock authentication
        with patch("api.v1.services.get_current_user") as mock_auth:
            mock_user = MagicMock()
            mock_user.id = 1
            mock_auth.return_value = mock_user

            verification_data = {"test": "data"}

            response = client.post(
                "/api/v1/services/invalid-service/verify", json=verification_data
            )
            assert response.status_code == 404

    @patch("httpx.AsyncClient.get")
    def test_get_user_verification_status(self, mock_get):
        """Test getting user verification status"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "verification_status": "verified",
            "score": 95,
        }
        mock_get.return_value = mock_response

        # Mock authentication
        with patch("api.v1.services.get_current_user") as mock_auth:
            mock_user = MagicMock()
            mock_user.id = 1
            mock_auth.return_value = mock_user

            response = client.get("/api/v1/services/user/1/verification-status")
            assert response.status_code == 200

            data = response.json()
            assert "user_id" in data
            assert "verification_status" in data
            assert "overall_progress" in data


class TestServiceEndpoints:
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200

        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "docs" in data

    def test_health_endpoint(self):
        """Test health endpoint"""
        response = client.get("/health")
        assert response.status_code == 200

        data = response.json()
        assert "status" in data
        assert "database" in data
        assert "services" in data

    def test_dashboard_endpoint(self):
        """Test dashboard endpoint"""
        response = client.get("/api/dashboard")
        assert response.status_code == 200

        data = response.json()
        assert "users" in data
        assert "services" in data
        assert "transactions" in data
        assert "system" in data

    def test_services_status_endpoint(self):
        """Test services status endpoint"""
        response = client.get("/api/services/status")
        assert response.status_code == 200

        data = response.json()
        assert "services" in data
        assert "total_services" in data
        assert "healthy_services" in data
        assert "system_health" in data

    def test_sql_level_endpoint(self):
        """Test SQL level endpoint"""
        response = client.get("/api/sql/1")
        assert response.status_code == 200

        data = response.json()
        assert "user_id" in data
        assert "sql_level" in data
        assert "sql_points" in data
        assert "sql_rank" in data
        assert "verification_progress" in data


if __name__ == "__main__":
    pytest.main([__file__])
