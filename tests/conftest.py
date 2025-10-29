"""Configuración y fixtures para tests"""
import pytest
from rudag_sdk import RudagSDK, RudagConfig

@pytest.fixture
def config():
    """Configuración de prueba"""
    return RudagConfig(
        node_url="http://localhost:5000",
        network="testnet",
        timeout=10,
        auto_connect=False
    )

@pytest.fixture
def sdk(config):
    """Instancia del SDK para pruebas"""
    return RudagSDK(config)

@pytest.fixture
def sample_wallet():
    """Datos de wallet de ejemplo"""
    return {
        'address': 'RGD:1A77LFiAzzVnDdpMRjKqwB3ZjiVnuNqQjk',
        'public_key': 'sample_public_key_hex',
        'private_key': 'sample_private_key_hex'
    }

@pytest.fixture
def sample_transaction():
    """Transacción de ejemplo"""
    return {
        'sender': 'RGD:1A77LFiAzzVnDdpMRjKqwB3ZjiVnuNqQjk',
        'recipient': 'RGD:2B88MBgVxzVnDdpMRjKqwB3ZjiVnuNqQjl',
        'amount': 10.5,
        'fee': 0.001
    }
