"""
Ejemplo de creación y gestión de tokens personalizados con Rudag SDK

Este ejemplo demuestra cómo:
- Crear un token personalizado
- Emitir tokens
- Transferir tokens entre wallets
- Consultar balances de tokens
- Quemar tokens
- Gestionar metadatos del token
"""
from rudag_sdk import RudagSDK, RudagConfig, RudagTransaction
from typing import Dict, Optional, List
import hashlib
import time

class CustomToken:
    """Clase para gestionar un token personalizado en Rudag Network"""
    
    def __init__(self, name: str, symbol: str, decimals: int, 
                 total_supply: float, owner_address: str):
        """
        Inicializar un token personalizado
        
        Args:
            name: Nombre del token (ej: "Mi Token")
            symbol: Símbolo del token (ej: "MTK")
            decimals: Número de decimales
            total_supply: Suministro total
            owner_address: Dirección del propietario
        """
        self.name = name
        self.symbol = symbol
        self.decimals = decimals
        self.total_supply = total_supply
        self.owner_address = owner_address
        self.token_id = self._generate_token_id()
        self.creation_time = time.time()
        
        # Registro de balances por dirección
        self.balances = {owner_address: total_supply}
        
        # Historial de transacciones del token
        self.transaction_history = []
    
    def _generate_token_id(self) -> str:
        """Generar ID único para el token"""
        data = f"{self.name}{self.symbol}{self.owner_address}{time.time()}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def get_info(self) -> Dict:
        """Obtener información del token"""
        return {
            'token_id': self.token_id,
            'name': self.name,
            'symbol': self.symbol,
            'decimals': self.decimals,
            'total_supply': self.total_supply,
            'owner': self.owner_address,
            'created_at': self.creation_time
        }
    
    def get_balance(self, address: str) -> float:
        """Obtener balance de tokens para una dirección"""
        return self.balances.get(address, 0.0)
    
    def transfer(self, from_address: str, to_address: str, amount: float) -> bool:
        """
        Transferir tokens entre direcciones
        
        Args:
            from_address: Dirección del remitente
            to_address: Dirección del destinatario
            amount: Cantidad de tokens a transferir
            
        Returns:
            bool: True si la transferencia fue exitosa
        """
        # Validar balance suficiente
        if self.get_balance(from_address) < amount:
            print(f"❌ Balance insuficiente. Balance actual: {self.get_balance(from_address)} {self.symbol}")
            return False
        
        # Realizar transferencia
        self.balances[from_address] -= amount
        self.balances[to_address] = self.balances.get(to_address, 0) + amount
        
        # Registrar en historial
        self.transaction_history.append({
            'type': 'transfer',
            'from': from_address,
            'to': to_address,
            'amount': amount,
            'timestamp': time.time()
        })
        
        return True
    
    def mint(self, to_address: str, amount: float, minter_address: str) -> bool:
        """
        Emitir nuevos tokens (solo el propietario puede hacerlo)
        
        Args:
            to_address: Dirección que recibirá los tokens
            amount: Cantidad de tokens a emitir
            minter_address: Dirección que realiza la emisión
            
        Returns:
            bool: True si la emisión fue exitosa
        """
        # Verificar que solo el propietario puede emitir
        if minter_address != self.owner_address:
            print(f"❌ Solo el propietario puede emitir tokens")
            return False
        
        # Emitir tokens
        self.balances[to_address] = self.balances.get(to_address, 0) + amount
        self.total_supply += amount
        
        # Registrar en historial
        self.transaction_history.append({
            'type': 'mint',
            'to': to_address,
            'amount': amount,
            'timestamp': time.time()
        })
        
        print(f"✅ {amount} {self.symbol} emitidos a {to_address[:20]}...")
        return True
    
    def burn(self, from_address: str, amount: float) -> bool:
        """
        Quemar tokens (reducir suministro)
        
        Args:
            from_address: Dirección desde donde se quemarán tokens
            amount: Cantidad de tokens a quemar
            
        Returns:
            bool: True si la quema fue exitosa
        """
        # Validar balance suficiente
        if self.get_balance(from_address) < amount:
            print(f"❌ Balance insuficiente para quemar")
            return False
        
        # Quemar tokens
        self.balances[from_address] -= amount
        self.total_supply -= amount
        
        # Registrar en historial
        self.transaction_history.append({
            'type': 'burn',
            'from': from_address,
            'amount': amount,
            'timestamp': time.time()
        })
        
        print(f"🔥 {amount} {self.symbol} quemados desde {from_address[:20]}...")
        return True
    
    def get_holders(self) -> List[Dict]:
        """Obtener lista de holders del token"""
        return [
            {'address': address, 'balance': balance}
            for address, balance in self.balances.items()
            if balance > 0
        ]
    
    def print_info(self):
        """Imprimir información del token de forma legible"""
        info = self.get_info()
        print(f"\n🪙 Información del Token:")
        print(f"   Nombre: {info['name']}")
        print(f"   Símbolo: {info['symbol']}")
        print(f"   ID: {info['token_id'][:32]}...")
        print(f"   Decimales: {info['decimals']}")
        print(f"   Suministro Total: {info['total_supply']:,.2f} {self.symbol}")
        print(f"   Propietario: {info['owner'][:20]}...")
    
    def print_holders(self):
        """Imprimir información de holders"""
        holders = self.get_holders()
        print(f"\n👥 Holders del Token ({len(holders)} direcciones):")
        print("=" * 80)
        
        for i, holder in enumerate(holders, 1):
            percentage = (holder['balance'] / self.total_supply) * 100
            print(f"{i}. {holder['address'][:30]}... → {holder['balance']:>10.2f} {self.symbol} ({percentage:.2f}%)")

class TokenManager:
    """Gestor de tokens para Rudag Network"""
    
    def __init__(self, node_url: str = "http://localhost:5000"):
        """Inicializar el gestor de tokens"""
        config = RudagConfig(
            node_url=node_url,
            network="mainnet",
            auto_connect=False
        )
        self.sdk = RudagSDK(config)
        self.tokens = {}
    
    def create_token(self, creator_wallet, name: str, symbol: str, 
                    decimals: int, initial_supply: float) -> CustomToken:
        """
        Crear un nuevo token personalizado
        
        Args:
            creator_wallet: Wallet del creador
            name: Nombre del token
            symbol: Símbolo del token
            decimals: Número de decimales
            initial_supply: Suministro inicial
            
        Returns:
            CustomToken: Token creado
        """
        token = CustomToken(
            name=name,
            symbol=symbol,
            decimals=decimals,
            total_supply=initial_supply,
            owner_address=creator_wallet.address
        )
        
        self.tokens[token.token_id] = token
        
        print(f"✅ Token '{name}' ({symbol}) creado exitosamente!")
        print(f"   ID del Token: {token.token_id[:32]}...")
        print(f"   Suministro Inicial: {initial_supply:,.2f} {symbol}")
        
        return token
    
    def get_token(self, token_id: str) -> Optional[CustomToken]:
        """Obtener un token por su ID"""
        return self.tokens.get(token_id)
    
    def list_tokens(self) -> List[CustomToken]:
        """Listar todos los tokens creados"""
        return list(self.tokens.values())

def main():
    """Demostración de tokens personalizados"""
    print("=" * 80)
    print("🪙 SISTEMA DE TOKENS PERSONALIZADOS - RUDAG")
    print("=" * 80)
    
    # Inicializar gestor de tokens
    token_manager = TokenManager()
    
    # Crear wallets
    print("\n1. Creando wallets...")
    sdk = RudagSDK(RudagConfig(node_url="http://localhost:5000", auto_connect=False))
    
    owner_wallet = sdk.create_wallet(wallet_name="Token Owner")
    user1_wallet = sdk.create_wallet(wallet_name="Usuario 1")
    user2_wallet = sdk.create_wallet(wallet_name="Usuario 2")
    user3_wallet = sdk.create_wallet(wallet_name="Usuario 3")
    
    print(f"✅ Wallet del propietario: {owner_wallet.address[:30]}...")
    print(f"✅ Wallet Usuario 1: {user1_wallet.address[:30]}...")
    print(f"✅ Wallet Usuario 2: {user2_wallet.address[:30]}...")
    print(f"✅ Wallet Usuario 3: {user3_wallet.address[:30]}...")
    
    # Crear tokens personalizados
    print("\n2. Creando tokens personalizados...")
    
    # Token 1: Token de utilidad
    utility_token = token_manager.create_token(
        creator_wallet=owner_wallet,
        name="Utility Token",
        symbol="UTK",
        decimals=18,
        initial_supply=1000000
    )
    
    # Token 2: Token de gobernanza
    governance_token = token_manager.create_token(
        creator_wallet=owner_wallet,
        name="Governance Token",
        symbol="GOV",
        decimals=18,
        initial_supply=100000
    )
    
    # Token 3: Token de recompensas
    reward_token = token_manager.create_token(
        creator_wallet=owner_wallet,
        name="Reward Token",
        symbol="RWD",
        decimals=8,
        initial_supply=5000000
    )
    
    # Mostrar información de tokens
    print("\n3. Información de tokens creados:")
    for token in token_manager.list_tokens():
        token.print_info()
    
    # Transferir tokens
    print("\n4. Distribuyendo tokens a usuarios...")
    
    # Distribuir Utility Token
    utility_token.transfer(owner_wallet.address, user1_wallet.address, 10000)
    print(f"✅ 10,000 UTK → Usuario 1")
    
    utility_token.transfer(owner_wallet.address, user2_wallet.address, 15000)
    print(f"✅ 15,000 UTK → Usuario 2")
    
    utility_token.transfer(owner_wallet.address, user3_wallet.address, 5000)
    print(f"✅ 5,000 UTK → Usuario 3")
    
    # Distribuir Governance Token
    governance_token.transfer(owner_wallet.address, user1_wallet.address, 1000)
    print(f"✅ 1,000 GOV → Usuario 1")
    
    governance_token.transfer(owner_wallet.address, user2_wallet.address, 2000)
    print(f"✅ 2,000 GOV → Usuario 2")
    
    # Emitir más tokens
    print("\n5. Emitiendo tokens adicionales...")
    reward_token.mint(user3_wallet.address, 50000, owner_wallet.address)
    
    # Transferencias entre usuarios
    print("\n6. Transferencias entre usuarios...")
    utility_token.transfer(user1_wallet.address, user2_wallet.address, 2000)
    print(f"✅ Usuario 1 → Usuario 2: 2,000 UTK")
    
    governance_token.transfer(user2_wallet.address, user1_wallet.address, 500)
    print(f"✅ Usuario 2 → Usuario 1: 500 GOV")
    
    # Quemar tokens
    print("\n7. Quemando tokens...")
    utility_token.burn(owner_wallet.address, 100000)
    
    # Mostrar holders
    print("\n8. Holders de cada token:")
    
    print("\n📊 Utility Token (UTK):")
    utility_token.print_holders()
    
    print("\n📊 Governance Token (GOV):")
    governance_token.print_holders()
    
    print("\n📊 Reward Token (RWD):")
    reward_token.print_holders()
    
    # Consultar balances
    print("\n9. Balances finales de Usuario 1:")
    print(f"   UTK: {utility_token.get_balance(user1_wallet.address):,.2f}")
    print(f"   GOV: {governance_token.get_balance(user1_wallet.address):,.2f}")
    print(f"   RWD: {reward_token.get_balance(user1_wallet.address):,.2f}")
    
    # Estadísticas finales
    print("\n10. Estadísticas de tokens:")
    for token in token_manager.list_tokens():
        holders = token.get_holders()
        print(f"\n   {token.name} ({token.symbol}):")
        print(f"   - Suministro Total: {token.total_supply:,.2f}")
        print(f"   - Holders: {len(holders)}")
        print(f"   - Transacciones: {len(token.transaction_history)}")
    
    print("\n" + "=" * 80)
    print("✅ Demo de tokens personalizados completada")
    print("=" * 80)

if __name__ == "__main__":
    main()
