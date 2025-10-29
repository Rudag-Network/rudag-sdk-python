"""
Módulo de interacción con la blockchain de Rudag Network
"""
import requests
import hashlib
import time
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, asdict
from .exceptions import TransactionError, BlockchainError

@dataclass
class RudagTransaction:
    """Representa una transacción en la red RUDAG"""
    sender: str
    recipient: str
    amount: float
    fee: float = 0.001
    timestamp: Optional[float] = None
    signature: Optional[str] = None
    transaction_id: Optional[str] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()
        if self.transaction_id is None:
            self.transaction_id = self._generate_id()
    
    def _generate_id(self) -> str:
        """Generar ID único para la transacción"""
        data = f"{self.sender}{self.recipient}{self.amount}{self.timestamp}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def to_dict(self) -> Dict:
        """Convertir transacción a diccionario"""
        return asdict(self)
    
    def sign(self, private_key: str):
        """Firmar la transacción con la clave privada"""
        import ecdsa
        sk = ecdsa.SigningKey.from_string(
            bytes.fromhex(private_key), 
            curve=ecdsa.SECP256k1
        )
        message = f"{self.sender}{self.recipient}{self.amount}{self.timestamp}"
        self.signature = sk.sign(message.encode()).hex()

class BlockchainClient:
    """Cliente para interactuar con la blockchain de Rudag Network"""
    
    def __init__(self, config):
        self.config = config
        self.base_url = config.node_url
        self.session = requests.Session()
        if config.api_key:
            self.session.headers.update({'Authorization': f'Bearer {config.api_key}'})
    
    def get_network_info(self) -> Dict[str, Any]:
        """Obtener información de la red RUDAG"""
        try:
            response = self.session.get(
                f"{self.base_url}/network/info",
                timeout=self.config.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise BlockchainError(f"Error al obtener información de la red: {e}") from e
    
    def get_balance(self, address: str) -> float:
        """Obtener el balance de una dirección"""
        try:
            response = self.session.get(
                f"{self.base_url}/wallet/balance/{address}",
                timeout=self.config.timeout
            )
            response.raise_for_status()
            data = response.json()
            return float(data.get('balance', 0))
        except requests.exceptions.RequestException as e:
            raise BlockchainError(f"Error al obtener balance: {e}") from e
    
    def send_transaction(self, transaction: RudagTransaction, 
                        private_key: Optional[str] = None) -> Dict[str, Any]:
        """Enviar una transacción a la red"""
        try:
            if private_key:
                transaction.sign(private_key)
            
            response = self.session.post(
                f"{self.base_url}/transaction/send",
                json=transaction.to_dict(),
                timeout=self.config.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise TransactionError(f"Error al enviar transacción: {e}") from e
    
    def get_transaction(self, transaction_id: str) -> Dict[str, Any]:
        """Obtener información de una transacción"""
        try:
            response = self.session.get(
                f"{self.base_url}/transaction/{transaction_id}",
                timeout=self.config.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise TransactionError(f"Error al obtener transacción: {e}") from e
    
    def get_blockchain(self) -> List[Dict[str, Any]]:
        """Obtener la cadena completa"""
        try:
            response = self.session.get(
                f"{self.base_url}/blockchain",
                timeout=self.config.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise BlockchainError(f"Error al obtener blockchain: {e}") from e
    
    def get_block(self, block_height: Optional[int] = None, 
                 block_hash: Optional[str] = None) -> Dict[str, Any]:
        """Obtener un bloque específico"""
        try:
            if block_height is not None:
                url = f"{self.base_url}/block/height/{block_height}"
            elif block_hash is not None:
                url = f"{self.base_url}/block/hash/{block_hash}"
            else:
                raise BlockchainError("Debe especificar block_height o block_hash")
            
            response = self.session.get(url, timeout=self.config.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise BlockchainError(f"Error al obtener bloque: {e}") from e
    
    def get_pending_transactions(self) -> List[Dict[str, Any]]:
        """Obtener transacciones pendientes"""
        try:
            response = self.session.get(
                f"{self.base_url}/transactions/pending",
                timeout=self.config.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise TransactionError(f"Error al obtener transacciones pendientes: {e}") from e
