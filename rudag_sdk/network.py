"""
Módulo de gestión de red y nodos para Rudag Network
"""
import requests
import asyncio
import websockets
import json
from typing import List, Dict, Any, Callable, Optional
from .exceptions import NetworkError

class NetworkManager:
    """Gestor de red y comunicaciones P2P"""
    
    def __init__(self, config):
        self.config = config
        self.base_url = config.node_url
        self.websocket_url = config.websocket_url or config.node_url.replace('http', 'ws')
        self.nodes = []
        self.event_callbacks = {}
        self.ws_connection = None
    
    def add_node(self, node_url: str) -> Dict[str, Any]:
        """Añadir un nuevo nodo a la red"""
        try:
            response = requests.post(
                f"{self.base_url}/nodes/add",
                json={'node_url': node_url},
                timeout=self.config.timeout
            )
            response.raise_for_status()
            self.nodes.append(node_url)
            return response.json()
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Error al añadir nodo: {e}") from e
    
    def remove_node(self, node_url: str) -> Dict[str, Any]:
        """Eliminar un nodo de la red"""
        try:
            response = requests.post(
                f"{self.base_url}/nodes/remove",
                json={'node_url': node_url},
                timeout=self.config.timeout
            )
            response.raise_for_status()
            if node_url in self.nodes:
                self.nodes.remove(node_url)
            return response.json()
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Error al eliminar nodo: {e}") from e
    
    def get_nodes(self) -> List[str]:
        """Obtener lista de nodos conectados"""
        try:
            response = requests.get(
                f"{self.base_url}/nodes",
                timeout=self.config.timeout
            )
            response.raise_for_status()
            data = response.json()
            self.nodes = data.get('nodes', [])
            return self.nodes
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Error al obtener nodos: {e}") from e
    
    def sync_blockchain(self) -> Dict[str, Any]:
        """Sincronizar la blockchain con otros nodos"""
        try:
            response = requests.post(
                f"{self.base_url}/blockchain/sync",
                timeout=self.config.timeout * 3
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Error al sincronizar blockchain: {e}") from e
    
    def broadcast_transaction(self, transaction: Dict[str, Any]) -> Dict[str, Any]:
        """Difundir una transacción a todos los nodos"""
        try:
            response = requests.post(
                f"{self.base_url}/transaction/broadcast",
                json=transaction,
                timeout=self.config.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Error al difundir transacción: {e}") from e
    
    def broadcast_block(self, block: Dict[str, Any]) -> Dict[str, Any]:
        """Difundir un bloque a todos los nodos"""
        try:
            response = requests.post(
                f"{self.base_url}/block/broadcast",
                json=block,
                timeout=self.config.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Error al difundir bloque: {e}") from e
    
    def subscribe_events(self, event_types: List[str], callback: Callable):
        """Suscribirse a eventos en tiempo real mediante WebSocket"""
        for event_type in event_types:
            self.event_callbacks[event_type] = callback
        
        asyncio.create_task(self._websocket_listener())
    
    async def _websocket_listener(self):
        """Escuchar eventos por WebSocket"""
        try:
            async with websockets.connect(self.websocket_url) as websocket:
                self.ws_connection = websocket
                
                subscribe_msg = json.dumps({
                    'action': 'subscribe',
                    'events': list(self.event_callbacks.keys())
                })
                await websocket.send(subscribe_msg)
                
                async for message in websocket:
                    data = json.loads(message)
                    event_type = data.get('type')
                    if event_type in self.event_callbacks:
                        callback = self.event_callbacks[event_type]
                        callback(data)
        except Exception as e:
            raise NetworkError(f"Error en conexión WebSocket: {e}") from e
    
    def disconnect_websocket(self):
        """Desconectar el WebSocket"""
        if self.ws_connection:
            asyncio.create_task(self.ws_connection.close())
            self.ws_connection = None
    
    def get_network_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas de la red"""
        try:
            response = requests.get(
                f"{self.base_url}/network/stats",
                timeout=self.config.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Error al obtener estadísticas: {e}") from e
