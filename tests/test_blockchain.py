"""Tests para el módulo de blockchain"""
import pytest
from rudag_sdk.blockchain import RudagTransaction, BlockchainClient
from rudag_sdk import RudagConfig

class TestRudagTransaction:
    """Tests para RudagTransaction"""
    
    def test_create_transaction(self):
        """Test crear transacción"""
        tx = RudagTransaction(
            sender="RGD:sender",
            recipient="RGD:recipient",
            amount=10.0,
            fee=0.001
        )
        
        assert tx.sender == "RGD:sender"
        assert tx.recipient == "RGD:recipient"
        assert tx.amount == 10.0
        assert tx.fee == 0.001
        assert tx.transaction_id is not None
        assert tx.timestamp is not None
    
    def test_transaction_to_dict(self):
        """Test convertir transacción a diccionario"""
        tx = RudagTransaction(
            sender="RGD:sender",
            recipient="RGD:recipient",
            amount=10.0
        )
        
        tx_dict = tx.to_dict()
        assert 'sender' in tx_dict
        assert 'recipient' in tx_dict
        assert 'amount' in tx_dict
        assert 'timestamp' in tx_dict

class TestBlockchainClient:
    """Tests para BlockchainClient"""
    
    def test_client_creation(self, config):
        """Test crear cliente de blockchain"""
        client = BlockchainClient(config)
        assert client.base_url == config.node_url
        assert client.config == config
