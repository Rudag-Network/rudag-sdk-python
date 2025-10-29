"""Tests para el módulo de wallet"""
import pytest
from rudag_sdk.wallet import WalletManager, RudagWallet
from rudag_sdk.exceptions import WalletError

class TestWalletManager:
    """Tests para WalletManager"""
    
    def test_create_wallet(self):
        """Test crear wallet"""
        manager = WalletManager()
        wallet = manager.create_wallet()
        
        assert wallet.address.startswith('RGD:')
        assert wallet.public_key is not None
        assert wallet.private_key is not None
        assert not wallet.encrypted
    
    def test_create_wallet_with_password(self):
        """Test crear wallet con contraseña"""
        manager = WalletManager()
        wallet = manager.create_wallet(password="test123")
        
        assert wallet.address.startswith('RGD:')
        assert wallet.encrypted
    
    def test_create_wallet_with_name(self):
        """Test crear wallet con nombre"""
        manager = WalletManager()
        wallet = manager.create_wallet(wallet_name="Mi Wallet")
        
        assert wallet.name == "Mi Wallet"
    
    def test_get_wallet(self):
        """Test obtener wallet"""
        manager = WalletManager()
        wallet = manager.create_wallet()
        
        retrieved = manager.get_wallet(wallet.address)
        assert retrieved.address == wallet.address
    
    def test_list_wallets(self):
        """Test listar wallets"""
        manager = WalletManager()
        wallet1 = manager.create_wallet()
        wallet2 = manager.create_wallet()
        
        wallets = manager.list_wallets()
        assert len(wallets) == 2

class TestRudagWallet:
    """Tests para RudagWallet"""
    
    def test_wallet_to_dict(self):
        """Test convertir wallet a diccionario"""
        wallet = RudagWallet(
            address="RGD:test",
            public_key="test_key",
            private_key="test_private"
        )
        
        wallet_dict = wallet.to_dict()
        assert wallet_dict['address'] == "RGD:test"
        assert wallet_dict['public_key'] == "test_key"
