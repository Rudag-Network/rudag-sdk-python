"""Tests para el módulo de red"""
import pytest
from rudag_sdk.network import NetworkManager
from rudag_sdk import RudagConfig

class TestNetworkManager:
    """Tests para NetworkManager"""
    
    def test_manager_creation(self, config):
        """Test crear gestor de red"""
        manager = NetworkManager(config)
        assert manager.base_url == config.node_url
        assert manager.nodes == []
    
    def test_websocket_url_generation(self, config):
        """Test generar URL de WebSocket"""
        manager = NetworkManager(config)
        expected = config.node_url.replace('http', 'ws')
        assert manager.websocket_url == expected
