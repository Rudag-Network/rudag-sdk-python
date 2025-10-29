import logging
from typing import Optional, Dict, Any
from dataclasses import dataclass
import requests

from .wallet import WalletManager
from .blockchain import BlockchainClient
from .network import NetworkManager
from .mining import MiningClient
from .exceptions import RudagError, ConnectionError

logger = logging.getLogger(__name__)

@dataclass
class RudagConfig:
    """Configuración para el SDK de Rudag Network"""
    node_url: str
    network: str = "mainnet"
    timeout: int = 30
    retry_attempts: int = 3
    api_key: Optional[str] = None
    websocket_url: Optional[str] = None
    auto_connect: bool = True
    debug: bool = False

class RudagSDK:
    """
    Cliente principal para interactuar con Rudag Network
    
    Esta clase proporciona una interfaz unificada para todas las operaciones
    de la blockchain RUDAG.
    """
    
    def __init__(self, config: RudagConfig):
        self.config = config
        self.wallet_manager = WalletManager()
        self.blockchain_client = BlockchainClient(config)
        self.network_manager = NetworkManager(config)
        self.mining_client = MiningClient(config)
        
        self._setup_logging()
        
        if config.auto_connect:
            self._test_connection()
    
    def _setup_logging(self):
        """Configurar el sistema de logging"""
        level = logging.DEBUG if self.config.debug else logging.INFO
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def _test_connection(self):
        """Probar la conexión con el nodo RUDAG"""
        try:
            response = requests.get(
                f"{self.config.node_url}/",
                timeout=self.config.timeout
            )
            if response.status_code != 200:
                raise ConnectionError(
                    f"No se pudo conectar al nodo. Código: {response.status_code}"
                )
            logger.info("✅ Conexión establecida con el nodo RUDAG")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Error de conexión: {e}") from e
    
    def get_network_info(self) -> Dict[str, Any]:
        """Obtener información de la red RUDAG"""
        return self.blockchain_client.get_network_info()
    
    def create_wallet(self, password: Optional[str] = None, 
                     wallet_name: Optional[str] = None):
        """Crear una nueva wallet RUDAG"""
        return self.wallet_manager.create_wallet(password, wallet_name)
    
    def import_wallet(self, private_key: str, password: Optional[str] = None):
        """Importar una wallet existente"""
        return self.wallet_manager.import_wallet(private_key, password)
    
    def get_balance(self, address: str) -> float:
        """Obtener el balance de una dirección"""
        return self.blockchain_client.get_balance(address)
    
    def send_transaction(self, transaction, private_key: Optional[str] = None):
        """Enviar una transacción a la red"""
        return self.blockchain_client.send_transaction(transaction, private_key)
    
    def get_transaction(self, transaction_id: str):
        """Obtener información de una transacción"""
        return self.blockchain_client.get_transaction(transaction_id)
    
    def get_blockchain(self):
        """Obtener la cadena completa"""
        return self.blockchain_client.get_blockchain()
    
    def get_block(self, block_height: Optional[int] = None, 
                 block_hash: Optional[str] = None):
        """Obtener un bloque específico"""
        return self.blockchain_client.get_block(block_height, block_hash)
    
    def mine_block(self, mining_wallet: Optional[str] = None):
        """Minar un nuevo bloque"""
        return self.mining_client.mine_block(mining_wallet)
    
    def set_mining_wallet(self, wallet_address: str):
        """Configurar wallet de minería"""
        return self.mining_client.set_mining_wallet(wallet_address)
    
    def add_node(self, node_url: str):
        """Añadir un nuevo nodo a la red"""
        return self.network_manager.add_node(node_url)
    
    def sync_blockchain(self):
        """Sincronizar la blockchain"""
        return self.network_manager.sync_blockchain()
    
    def subscribe_events(self, event_types, callback):
        """Suscribirse a eventos en tiempo real"""
        return self.network_manager.subscribe_events(event_types, callback)
