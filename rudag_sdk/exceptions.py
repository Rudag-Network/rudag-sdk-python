"""
Excepciones personalizadas para el SDK de Rudag Network
"""

class RudagError(Exception):
    """Excepción base para todos los errores del SDK de Rudag"""
    pass

class ConnectionError(RudagError):
    """Error de conexión con el nodo RUDAG"""
    pass

class TransactionError(RudagError):
    """Error al procesar una transacción"""
    pass

class WalletError(RudagError):
    """Error relacionado con operaciones de wallet"""
    pass

class NetworkError(RudagError):
    """Error relacionado con operaciones de red"""
    pass

class MiningError(RudagError):
    """Error relacionado con operaciones de minería"""
    pass

class ValidationError(RudagError):
    """Error de validación de datos"""
    pass

class BlockchainError(RudagError):
    """Error relacionado con la blockchain"""
    pass
