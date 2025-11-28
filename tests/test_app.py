import pytest
from app import app
from scripts.collect_signals import aggregate_events


class TestApp:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = app.test_client()
        self.client.testing = True
    
    def test_health(self):
        # Arrange
        response = self.client.get('/health')
        
        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert 'status' in data
        assert data['status'] == 'OK'
    
    def test_empty_input(self):
        # Arrange
        expected_stats = {
            "total_events": 0,
            "by_source": {},
            "by_protocol": {}
        }
        
        # Act
        stats = aggregate_events([])
        
        # Assert
        assert stats == expected_stats
        
        
        
        