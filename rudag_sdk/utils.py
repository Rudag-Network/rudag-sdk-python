"""
Utilidades generales para el SDK de Rudag Network
"""
import hashlib
import json
import time
from typing import Any, Dict
from datetime import datetime

def generate_hash(data: str) -> str:
    """Generar hash SHA256 de un string"""
    return hashlib.sha256(data.encode()).hexdigest()

def generate_transaction_id(sender: str, recipient: str, amount: float, timestamp: float) -> str:
    """Generar ID único para una transacción"""
    data = f"{sender}{recipient}{amount}{timestamp}"
    return generate_hash(data)

def validate_address(address: str) -> bool:
    """Validar formato de dirección RUDAG"""
    if not address.startswith('RGD:'):
        return False
    address_part = address[4:]
    if len(address_part) < 26:
        return False
    return True

def format_balance(balance: float, decimals: int = 8) -> str:
    """Formatear balance con decimales"""
    return f"{balance:.{decimals}f}"

def timestamp_to_datetime(timestamp: float) -> str:
    """Convertir timestamp a formato datetime legible"""
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def current_timestamp() -> float:
    """Obtener timestamp actual"""
    return time.time()

def dict_to_json(data: Dict[str, Any]) -> str:
    """Convertir diccionario a JSON string"""
    return json.dumps(data, indent=2)

def json_to_dict(json_str: str) -> Dict[str, Any]:
    """Convertir JSON string a diccionario"""
    return json.loads(json_str)

def calculate_fee(amount: float, fee_percentage: float = 0.001) -> float:
    """Calcular comisión de transacción"""
    return amount * fee_percentage

def validate_transaction_amount(amount: float) -> bool:
    """Validar que el monto de transacción sea válido"""
    return amount > 0

def format_rgd(amount: float) -> str:
    """Formatear cantidad en RGD"""
    return f"{amount:.8f} RGD"

def abbreviate_hash(hash_str: str, length: int = 8) -> str:
    """Abreviar un hash largo para mostrar"""
    if len(hash_str) <= length * 2:
        return hash_str
    return f"{hash_str[:length]}...{hash_str[-length:]}"

def validate_private_key(private_key: str) -> bool:
    """Validar formato de clave privada"""
    try:
        bytes.fromhex(private_key)
        return len(private_key) == 64
    except ValueError:
        return False

def validate_public_key(public_key: str) -> bool:
    """Validar formato de clave pública"""
    try:
        bytes.fromhex(public_key)
        return len(public_key) == 128
    except ValueError:
        return False

class RudagEncoder(json.JSONEncoder):
    """Encoder JSON personalizado para objetos de Rudag"""
    def default(self, obj):
        if hasattr(obj, 'to_dict'):
            return obj.to_dict()
        if isinstance(obj, bytes):
            return obj.hex()
        return super().default(obj)
