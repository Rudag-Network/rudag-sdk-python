"""
Ejemplo de monitor en tiempo real usando WebSocket
"""
from rudag_sdk import RudagSDK, RudagConfig
import asyncio

class RudagMonitor:
    """Monitor de eventos en tiempo real de la red Rudag"""
    
    def __init__(self, node_url: str, websocket_url: str = None):
        self.config = RudagConfig(
            node_url=node_url,
            websocket_url=websocket_url,
            auto_connect=False
        )
        self.sdk = RudagSDK(self.config)
        self.transaction_count = 0
        self.block_count = 0
    
    def on_new_transaction(self, data):
        """Callback para nuevas transacciones"""
        self.transaction_count += 1
        print(f"\n💸 Nueva transacción detectada:")
        print(f"   ID: {data.get('transaction_id')}")
        print(f"   De: {data.get('sender')}")
        print(f"   Para: {data.get('recipient')}")
        print(f"   Monto: {data.get('amount')} RGD")
        print(f"   Total transacciones: {self.transaction_count}")
    
    def on_new_block(self, data):
        """Callback para nuevos bloques"""
        self.block_count += 1
        print(f"\n⛓️  Nuevo bloque minado:")
        print(f"   Altura: {data.get('height')}")
        print(f"   Hash: {data.get('hash')[:16]}...")
        print(f"   Transacciones: {data.get('transaction_count')}")
        print(f"   Minero: {data.get('miner')}")
        print(f"   Total bloques: {self.block_count}")
    
    def on_node_connected(self, data):
        """Callback para conexión de nodos"""
        print(f"\n🔗 Nuevo nodo conectado:")
        print(f"   URL: {data.get('node_url')}")
        print(f"   Versión: {data.get('version')}")
    
    def start_monitoring(self):
        """Iniciar monitoreo de eventos"""
        print("=== Monitor en Tiempo Real - Rudag Network ===\n")
        print("🔍 Iniciando monitoreo de eventos...")
        print("   - Transacciones nuevas")
        print("   - Bloques minados")
        print("   - Nodos conectados")
        print("\nPresiona Ctrl+C para detener\n")
        
        event_handlers = {
            'new_transaction': self.on_new_transaction,
            'new_block': self.on_new_block,
            'node_connected': self.on_node_connected
        }
        
        try:
            self.sdk.subscribe_events(
                event_types=list(event_handlers.keys()),
                callback=lambda data: event_handlers.get(
                    data.get('type'), 
                    lambda x: None
                )(data)
            )
        except Exception as e:
            print(f"❌ Error al conectar: {e}")
    
    def get_stats(self):
        """Obtener estadísticas del monitor"""
        return {
            'transactions_monitored': self.transaction_count,
            'blocks_monitored': self.block_count
        }

def main():
    monitor = RudagMonitor(
        node_url="http://localhost:5000",
        websocket_url="ws://localhost:5000/ws"
    )
    
    try:
        monitor.start_monitoring()
        
        while True:
            asyncio.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Deteniendo monitor...")
        stats = monitor.get_stats()
        print(f"\n📊 Estadísticas de monitoreo:")
        print(f"   Transacciones monitoreadas: {stats['transactions_monitored']}")
        print(f"   Bloques monitoreados: {stats['blocks_monitored']}")
        print("\n✅ Monitor detenido")

if __name__ == "__main__":
    main()
