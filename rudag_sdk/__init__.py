"""
Rudag Network SDK

SDK oficial de Python para interactuar con la blockchain de Rudag Network.
"""

__version__ = "1.0.0"
__author__ = "Rudag Network"
__email__ = "cmoraes199322@gmail.com"

from .core import RudagSDK, RudagConfig
from .wallet import RudagWallet, WalletManager
from .blockchain import RudagTransaction, BlockchainClient
from .network import NetworkManager
from .mining import MiningClient
from .exceptions import (
    RudagError,
    ConnectionError,
    TransactionError,
    WalletError,
    NetworkError,
)

__all__ = [
    "RudagSDK",
    "RudagConfig",
    "RudagWallet",
    "RudagTransaction",
    "WalletManager",
    "BlockchainClient", 
    "NetworkManager",
    "MiningClient",
    "RudagError",
    "ConnectionError",
    "TransactionError",
    "WalletError",
    "NetworkError",
    "__version__",
    "__author__",
    "__email__",
]
