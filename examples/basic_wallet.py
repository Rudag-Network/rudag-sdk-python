"""
Ejemplo básico de uso de wallet con Rudag SDK
"""
from rudag_sdk import RudagSDK, RudagConfig

def main():
    config = RudagConfig(
        node_url="http://localhost:5000",
        network="mainnet",
        auto_connect=False
    )
    
    sdk = RudagSDK(config)
    
    print("=== Rudag Wallet Manager ===\n")
    
    print("1. Creando nueva wallet...")
    wallet = sdk.create_wallet(wallet_name="Mi Primera Wallet")
    print(f"✅ Wallet creada exitosamente!")
    print(f"   📍 Dirección: {wallet.address}")
    print(f"   🔑 Clave pública: {wallet.public_key[:20]}...")
    print(f"   🔐 Clave privada: {wallet.private_key[:20]}...\n")
    
    print("2. Guardando información de la wallet...")
    print("⚠️  IMPORTANTE: Guarda tu clave privada de forma segura!")
    print(f"   Clave privada completa: {wallet.private_key}\n")
    
    print("3. Consultando balance...")
    try:
        balance = sdk.get_balance(wallet.address)
        print(f"💰 Balance: {balance} RGD\n")
    except Exception as e:
        print(f"⚠️  No se pudo consultar el balance: {e}\n")
    
    print("4. Creando wallet con contraseña...")
    secure_wallet = sdk.create_wallet(
        password="mi_password_seguro",
        wallet_name="Wallet Segura"
    )
    print(f"✅ Wallet segura creada!")
    print(f"   📍 Dirección: {secure_wallet.address}")
    print(f"   🔒 Clave privada cifrada: {secure_wallet.encrypted}\n")

if __name__ == "__main__":
    main()
