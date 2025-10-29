"""
Ejemplo de cómo enviar transacciones con Rudag SDK
"""
from rudag_sdk import RudagSDK, RudagConfig, RudagTransaction

def main():
    config = RudagConfig(
        node_url="http://localhost:5000",
        network="mainnet",
        auto_connect=False
    )
    
    sdk = RudagSDK(config)
    
    print("=== Rudag Transaction Manager ===\n")
    
    print("1. Creando wallet del remitente...")
    sender_wallet = sdk.create_wallet(wallet_name="Remitente")
    print(f"✅ Wallet remitente: {sender_wallet.address}\n")
    
    print("2. Creando wallet del destinatario...")
    recipient_wallet = sdk.create_wallet(wallet_name="Destinatario")
    print(f"✅ Wallet destinatario: {recipient_wallet.address}\n")
    
    print("3. Creando transacción...")
    transaction = RudagTransaction(
        sender=sender_wallet.address,
        recipient=recipient_wallet.address,
        amount=10.5,
        fee=0.001
    )
    print(f"💸 Transacción creada:")
    print(f"   De: {transaction.sender}")
    print(f"   Para: {transaction.recipient}")
    print(f"   Monto: {transaction.amount} RGD")
    print(f"   Comisión: {transaction.fee} RGD")
    print(f"   ID: {transaction.transaction_id}\n")
    
    print("4. Firmando transacción...")
    transaction.sign(sender_wallet.private_key)
    print(f"✅ Transacción firmada\n")
    
    print("5. Enviando transacción a la red...")
    try:
        result = sdk.send_transaction(transaction)
        print(f"✅ Transacción enviada exitosamente!")
        print(f"   ID de transacción: {result.get('transaction_id')}")
        print(f"   Estado: {result.get('status')}\n")
    except Exception as e:
        print(f"⚠️  Error al enviar transacción: {e}\n")
    
    print("6. Consultando transacción...")
    try:
        tx_info = sdk.get_transaction(transaction.transaction_id)
        print(f"📋 Información de la transacción:")
        print(f"   Estado: {tx_info.get('status')}")
        print(f"   Bloque: {tx_info.get('block_height')}")
        print(f"   Confirmaciones: {tx_info.get('confirmations')}\n")
    except Exception as e:
        print(f"⚠️  Error al consultar transacción: {e}\n")

if __name__ == "__main__":
    main()
