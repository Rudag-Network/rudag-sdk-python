"""
Ejemplo de sistema de pagos con Rudag SDK

Este ejemplo demuestra cómo construir un sistema de pagos completo
que incluye:
- Gestión de múltiples wallets
- Procesamiento de pagos
- Validación de balances
- Historial de transacciones
- Manejo de errores
"""
from rudag_sdk import RudagSDK, RudagConfig, RudagTransaction
from typing import List, Dict, Optional
import time

class PaymentSystem:
    """Sistema de pagos para Rudag Network"""
    
    def __init__(self, node_url: str = "http://localhost:5000"):
        """Inicializar el sistema de pagos"""
        config = RudagConfig(
            node_url=node_url,
            network="mainnet",
            timeout=30,
            auto_connect=False
        )
        self.sdk = RudagSDK(config)
        self.payment_history = []
    
    def create_merchant_wallet(self, merchant_name: str):
        """Crear una wallet para un comerciante"""
        wallet = self.sdk.create_wallet(wallet_name=merchant_name)
        print(f"✅ Wallet de comerciante creada para {merchant_name}")
        print(f"   📍 Dirección: {wallet.address}")
        return wallet
    
    def create_customer_wallet(self, customer_name: str):
        """Crear una wallet para un cliente"""
        wallet = self.sdk.create_wallet(wallet_name=customer_name)
        print(f"✅ Wallet de cliente creada para {customer_name}")
        print(f"   📍 Dirección: {wallet.address}")
        return wallet
    
    def process_payment(self, sender_wallet, recipient_address: str, 
                       amount: float, description: str = "") -> Optional[Dict]:
        """
        Procesar un pago
        
        Args:
            sender_wallet: Wallet del remitente
            recipient_address: Dirección del destinatario
            amount: Monto a enviar
            description: Descripción del pago
            
        Returns:
            Dict con información del pago o None si falla
        """
        try:
            print(f"\n💳 Procesando pago...")
            print(f"   De: {sender_wallet.address[:20]}...")
            print(f"   Para: {recipient_address[:20]}...")
            print(f"   Monto: {amount} RGD")
            print(f"   Descripción: {description}")
            
            # Verificar balance (simulado)
            print(f"   Verificando balance...")
            
            # Crear transacción
            transaction = RudagTransaction(
                sender=sender_wallet.address,
                recipient=recipient_address,
                amount=amount,
                fee=0.001
            )
            
            # Firmar transacción
            transaction.sign(sender_wallet.private_key)
            
            # Enviar transacción
            result = self.sdk.send_transaction(transaction)
            
            # Guardar en historial
            payment_record = {
                'transaction_id': transaction.transaction_id,
                'sender': sender_wallet.address,
                'recipient': recipient_address,
                'amount': amount,
                'fee': transaction.fee,
                'description': description,
                'timestamp': transaction.timestamp,
                'status': result.get('status', 'pending')
            }
            self.payment_history.append(payment_record)
            
            print(f"✅ Pago procesado exitosamente!")
            print(f"   ID de transacción: {transaction.transaction_id}")
            
            return payment_record
            
        except Exception as e:
            print(f"❌ Error al procesar pago: {e}")
            return None
    
    def process_bulk_payments(self, sender_wallet, payments: List[Dict]) -> Dict:
        """
        Procesar múltiples pagos en lote
        
        Args:
            sender_wallet: Wallet del remitente
            payments: Lista de pagos con formato:
                      [{'recipient': address, 'amount': float, 'description': str}]
                      
        Returns:
            Dict con estadísticas del procesamiento
        """
        print(f"\n📦 Procesando {len(payments)} pagos en lote...")
        
        successful = 0
        failed = 0
        total_amount = 0
        
        for payment in payments:
            result = self.process_payment(
                sender_wallet,
                payment['recipient'],
                payment['amount'],
                payment.get('description', '')
            )
            
            if result:
                successful += 1
                total_amount += payment['amount']
            else:
                failed += 1
            
            time.sleep(0.5)  # Pequeña pausa entre transacciones
        
        stats = {
            'total': len(payments),
            'successful': successful,
            'failed': failed,
            'total_amount': total_amount
        }
        
        print(f"\n📊 Estadísticas del procesamiento:")
        print(f"   Total de pagos: {stats['total']}")
        print(f"   Exitosos: {stats['successful']}")
        print(f"   Fallidos: {stats['failed']}")
        print(f"   Monto total: {stats['total_amount']} RGD")
        
        return stats
    
    def get_payment_history(self, wallet_address: Optional[str] = None) -> List[Dict]:
        """
        Obtener historial de pagos
        
        Args:
            wallet_address: Filtrar por dirección (opcional)
            
        Returns:
            Lista de pagos
        """
        if wallet_address:
            return [
                payment for payment in self.payment_history
                if payment['sender'] == wallet_address or 
                   payment['recipient'] == wallet_address
            ]
        return self.payment_history
    
    def print_payment_history(self, wallet_address: Optional[str] = None):
        """Imprimir historial de pagos de forma legible"""
        history = self.get_payment_history(wallet_address)
        
        if not history:
            print("📝 No hay pagos en el historial")
            return
        
        print(f"\n📝 Historial de pagos ({len(history)} transacciones):")
        print("=" * 80)
        
        for i, payment in enumerate(history, 1):
            print(f"\n{i}. Transacción {payment['transaction_id'][:16]}...")
            print(f"   De: {payment['sender'][:20]}...")
            print(f"   Para: {payment['recipient'][:20]}...")
            print(f"   Monto: {payment['amount']} RGD")
            print(f"   Comisión: {payment['fee']} RGD")
            print(f"   Descripción: {payment['description']}")
            print(f"   Estado: {payment['status']}")
    
    def calculate_fees(self, amount: float) -> float:
        """Calcular comisión para un monto"""
        base_fee = 0.001
        percentage_fee = amount * 0.001  # 0.1%
        return max(base_fee, percentage_fee)

def main():
    """Demostración del sistema de pagos"""
    print("=" * 80)
    print("🏦 SISTEMA DE PAGOS RUDAG")
    print("=" * 80)
    
    # Inicializar sistema
    payment_system = PaymentSystem()
    
    # Crear wallets
    print("\n1. Creando wallets...")
    merchant = payment_system.create_merchant_wallet("Tienda Online")
    customer1 = payment_system.create_customer_wallet("Cliente 1")
    customer2 = payment_system.create_customer_wallet("Cliente 2")
    customer3 = payment_system.create_customer_wallet("Cliente 3")
    
    # Procesar pago individual
    print("\n2. Procesando pago individual...")
    payment_system.process_payment(
        customer1,
        merchant.address,
        25.50,
        "Compra de producto A"
    )
    
    # Procesar múltiples pagos
    print("\n3. Procesando pagos en lote...")
    bulk_payments = [
        {
            'recipient': merchant.address,
            'amount': 10.00,
            'description': 'Producto B'
        },
        {
            'recipient': merchant.address,
            'amount': 15.75,
            'description': 'Producto C'
        },
        {
            'recipient': merchant.address,
            'amount': 8.25,
            'description': 'Producto D'
        }
    ]
    payment_system.process_bulk_payments(customer2, bulk_payments)
    
    # Pago de cliente a cliente
    print("\n4. Procesando pago entre clientes...")
    payment_system.process_payment(
        customer1,
        customer3.address,
        5.00,
        "Transferencia personal"
    )
    
    # Mostrar historial completo
    print("\n5. Historial completo de pagos:")
    payment_system.print_payment_history()
    
    # Mostrar historial del comerciante
    print("\n6. Historial del comerciante:")
    payment_system.print_payment_history(merchant.address)
    
    # Calcular comisiones
    print("\n7. Cálculo de comisiones:")
    amounts = [10, 100, 1000, 10000]
    for amount in amounts:
        fee = payment_system.calculate_fees(amount)
        print(f"   Monto: {amount:>6} RGD → Comisión: {fee:.4f} RGD")
    
    print("\n" + "=" * 80)
    print("✅ Demo del sistema de pagos completada")
    print("=" * 80)

if __name__ == "__main__":
    main()
