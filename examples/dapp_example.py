"""
Ejemplo de DApp básica usando Rudag SDK
Simula una aplicación descentralizada simple
"""
from rudag_sdk import RudagSDK, RudagConfig, RudagTransaction
import time

class SimplePaymentDApp:
    """DApp de ejemplo para pagos simples"""
    
    def __init__(self, node_url: str):
        self.config = RudagConfig(
            node_url=node_url,
            network="mainnet",
            auto_connect=False
        )
        self.sdk = RudagSDK(self.config)
        self.wallets = {}
    
    def create_user(self, username: str) -> dict:
        """Crear un nuevo usuario con su wallet"""
        wallet = self.sdk.create_wallet(wallet_name=username)
        self.wallets[username] = wallet
        return {
            'username': username,
            'address': wallet.address,
            'balance': 0
        }
    
    def get_user_balance(self, username: str) -> float:
        """Obtener balance de un usuario"""
        if username not in self.wallets:
            raise ValueError(f"Usuario {username} no encontrado")
        
        wallet = self.wallets[username]
        try:
            return self.sdk.get_balance(wallet.address)
        except Exception:
            return 0.0
    
    def send_payment(self, sender: str, recipient: str, amount: float) -> dict:
        """Enviar pago entre usuarios"""
        if sender not in self.wallets:
            raise ValueError(f"Remitente {sender} no encontrado")
        if recipient not in self.wallets:
            raise ValueError(f"Destinatario {recipient} no encontrado")
        
        sender_wallet = self.wallets[sender]
        recipient_wallet = self.wallets[recipient]
        
        transaction = RudagTransaction(
            sender=sender_wallet.address,
            recipient=recipient_wallet.address,
            amount=amount,
            fee=0.001
        )
        
        transaction.sign(sender_wallet.private_key)
        
        try:
            result = self.sdk.send_transaction(transaction)
            return {
                'success': True,
                'transaction_id': result.get('transaction_id'),
                'message': f'Pago de {amount} RGD enviado de {sender} a {recipient}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

def main():
    print("=== DApp de Pagos Simple - Rudag Network ===\n")
    
    dapp = SimplePaymentDApp("http://localhost:5000")
    
    print("1. Creando usuarios...")
    alice = dapp.create_user("Alice")
    bob = dapp.create_user("Bob")
    charlie = dapp.create_user("Charlie")
    
    print(f"✅ Usuario creado: {alice['username']} - {alice['address']}")
    print(f"✅ Usuario creado: {bob['username']} - {bob['address']}")
    print(f"✅ Usuario creado: {charlie['username']} - {charlie['address']}\n")
    
    print("2. Consultando balances iniciales...")
    for username in ['Alice', 'Bob', 'Charlie']:
        balance = dapp.get_user_balance(username)
        print(f"💰 {username}: {balance} RGD")
    print()
    
    print("3. Simulando pagos entre usuarios...")
    print("   Alice -> Bob: 5 RGD")
    result1 = dapp.send_payment("Alice", "Bob", 5.0)
    if result1['success']:
        print(f"   ✅ {result1['message']}")
    else:
        print(f"   ❌ Error: {result1['error']}")
    
    time.sleep(1)
    
    print("   Bob -> Charlie: 2.5 RGD")
    result2 = dapp.send_payment("Bob", "Charlie", 2.5)
    if result2['success']:
        print(f"   ✅ {result2['message']}")
    else:
        print(f"   ❌ Error: {result2['error']}")
    print()
    
    print("4. Consultando información de red...")
    try:
        network_info = dapp.sdk.get_network_info()
        print(f"🌐 Red: {network_info.get('name')}")
        print(f"📦 Altura de bloque: {network_info.get('block_height')}")
        print(f"👥 Nodos conectados: {network_info.get('node_count')}")
    except Exception as e:
        print(f"⚠️  No se pudo obtener información de red: {e}")

if __name__ == "__main__":
    main()
