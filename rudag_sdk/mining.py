"""
Módulo de minería para Rudag Network
"""
import requests
import hashlib
import time
from typing import Optional, Dict, Any
from .exceptions import MiningError

class MiningClient:
    """Cliente para operaciones de minería"""
    
    def __init__(self, config):
        self.config = config
        self.base_url = config.node_url
        self.mining_wallet = None
        self.is_mining = False
    
    def set_mining_wallet(self, wallet_address: str) -> Dict[str, str]:
        """Configurar la wallet que recibirá las recompensas de minería"""
        self.mining_wallet = wallet_address
        return {
            'status': 'success',
            'message': f'Wallet de minería configurada: {wallet_address}'
        }
    
    def get_mining_wallet(self) -> Optional[str]:
        """Obtener la wallet de minería configurada"""
        return self.mining_wallet
    
    def mine_block(self, mining_wallet: Optional[str] = None) -> Dict[str, Any]:
        """
        Minar un nuevo bloque
        
        Args:
            mining_wallet: Dirección de la wallet para recibir recompensas (opcional)
            
        Returns:
            Dict con información del bloque minado
        """
        wallet = mining_wallet or self.mining_wallet
        if not wallet:
            raise MiningError("Debe configurar una wallet de minería primero")
        
        try:
            response = requests.post(
                f"{self.base_url}/mine",
                json={'mining_wallet': wallet},
                timeout=self.config.timeout * 10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise MiningError(f"Error al minar bloque: {e}") from e
    
    def start_mining(self, mining_wallet: Optional[str] = None) -> Dict[str, str]:
        """Iniciar minería continua"""
        wallet = mining_wallet or self.mining_wallet
        if not wallet:
            raise MiningError("Debe configurar una wallet de minería primero")
        
        try:
            response = requests.post(
                f"{self.base_url}/mining/start",
                json={'mining_wallet': wallet},
                timeout=self.config.timeout
            )
            response.raise_for_status()
            self.is_mining = True
            return response.json()
        except requests.exceptions.RequestException as e:
            raise MiningError(f"Error al iniciar minería: {e}") from e
    
    def stop_mining(self) -> Dict[str, str]:
        """Detener minería continua"""
        try:
            response = requests.post(
                f"{self.base_url}/mining/stop",
                timeout=self.config.timeout
            )
            response.raise_for_status()
            self.is_mining = False
            return response.json()
        except requests.exceptions.RequestException as e:
            raise MiningError(f"Error al detener minería: {e}") from e
    
    def get_mining_status(self) -> Dict[str, Any]:
        """Obtener estado actual de la minería"""
        try:
            response = requests.get(
                f"{self.base_url}/mining/status",
                timeout=self.config.timeout
            )
            response.raise_for_status()
            data = response.json()
            self.is_mining = data.get('is_mining', False)
            return data
        except requests.exceptions.RequestException as e:
            raise MiningError(f"Error al obtener estado de minería: {e}") from e
    
    def get_mining_difficulty(self) -> int:
        """Obtener la dificultad actual de minería"""
        try:
            response = requests.get(
                f"{self.base_url}/mining/difficulty",
                timeout=self.config.timeout
            )
            response.raise_for_status()
            data = response.json()
            return int(data.get('difficulty', 0))
        except requests.exceptions.RequestException as e:
            raise MiningError(f"Error al obtener dificultad: {e}") from e
    
    def get_mining_reward(self) -> float:
        """Obtener la recompensa actual por bloque minado"""
        try:
            response = requests.get(
                f"{self.base_url}/mining/reward",
                timeout=self.config.timeout
            )
            response.raise_for_status()
            data = response.json()
            return float(data.get('reward', 0))
        except requests.exceptions.RequestException as e:
            raise MiningError(f"Error al obtener recompensa: {e}") from e
    
    def calculate_hash(self, block_data: Dict[str, Any]) -> str:
        """Calcular hash de un bloque"""
        block_string = str(block_data).encode()
        return hashlib.sha256(block_string).hexdigest()
    
    def validate_proof_of_work(self, block_hash: str, difficulty: int) -> bool:
        """Validar que un hash cumple con la dificultad requerida"""
        return block_hash.startswith('0' * difficulty)
