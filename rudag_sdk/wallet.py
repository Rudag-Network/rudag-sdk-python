"""
Módulo de gestión de wallets para Rudag Network
"""
import hashlib
import ecdsa
import base58
from typing import Optional, Dict
from dataclasses import dataclass
from .exceptions import WalletError

@dataclass
class RudagWallet:
    """Representa una wallet de Rudag Network"""
    address: str
    public_key: str
    private_key: Optional[str] = None
    name: Optional[str] = None
    encrypted: bool = False
    
    def to_dict(self) -> Dict:
        """Convertir wallet a diccionario"""
        return {
            'address': self.address,
            'public_key': self.public_key,
            'name': self.name,
            'encrypted': self.encrypted
        }

class WalletManager:
    """Gestor de wallets para Rudag Network"""
    
    def __init__(self):
        self.wallets = {}
    
    def create_wallet(self, password: Optional[str] = None, 
                     wallet_name: Optional[str] = None) -> RudagWallet:
        """
        Crear una nueva wallet RUDAG
        
        Args:
            password: Contraseña para cifrar la clave privada (opcional)
            wallet_name: Nombre identificativo de la wallet (opcional)
            
        Returns:
            RudagWallet: Objeto wallet con las claves generadas
        """
        try:
            sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
            private_key = sk.to_string().hex()
            public_key = sk.get_verifying_key().to_string().hex()
            
            address = self._generate_address(public_key)
            
            encrypted = password is not None
            if encrypted:
                private_key = self._encrypt_private_key(private_key, password)
            
            wallet = RudagWallet(
                address=address,
                public_key=public_key,
                private_key=private_key,
                name=wallet_name,
                encrypted=encrypted
            )
            
            self.wallets[address] = wallet
            return wallet
            
        except Exception as e:
            raise WalletError(f"Error al crear wallet: {e}") from e
    
    def import_wallet(self, private_key: str, 
                     password: Optional[str] = None) -> RudagWallet:
        """
        Importar una wallet existente usando su clave privada
        
        Args:
            private_key: Clave privada de la wallet
            password: Contraseña para cifrar la clave privada (opcional)
            
        Returns:
            RudagWallet: Objeto wallet importado
        """
        try:
            sk = ecdsa.SigningKey.from_string(
                bytes.fromhex(private_key), 
                curve=ecdsa.SECP256k1
            )
            public_key = sk.get_verifying_key().to_string().hex()
            address = self._generate_address(public_key)
            
            encrypted = password is not None
            if encrypted:
                private_key = self._encrypt_private_key(private_key, password)
            
            wallet = RudagWallet(
                address=address,
                public_key=public_key,
                private_key=private_key,
                encrypted=encrypted
            )
            
            self.wallets[address] = wallet
            return wallet
            
        except Exception as e:
            raise WalletError(f"Error al importar wallet: {e}") from e
    
    def get_wallet(self, address: str) -> Optional[RudagWallet]:
        """Obtener una wallet por su dirección"""
        return self.wallets.get(address)
    
    def list_wallets(self):
        """Listar todas las wallets gestionadas"""
        return list(self.wallets.values())
    
    def _generate_address(self, public_key: str) -> str:
        """
        Generar dirección RUDAG desde clave pública
        
        Args:
            public_key: Clave pública en formato hexadecimal
            
        Returns:
            str: Dirección RUDAG con prefijo RGD:
        """
        sha256_hash = hashlib.sha256(public_key.encode()).digest()
        ripemd160_hash = hashlib.new('ripemd160', sha256_hash).digest()
        address_bytes = b'\x00' + ripemd160_hash
        checksum = hashlib.sha256(hashlib.sha256(address_bytes).digest()).digest()[:4]
        address = base58.b58encode(address_bytes + checksum).decode()
        return f"RGD:{address}"
    
    def _encrypt_private_key(self, private_key: str, password: str) -> str:
        """Cifrar clave privada con contraseña (implementación básica)"""
        from cryptography.fernet import Fernet
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
        import base64
        
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'rudag_salt',
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        f = Fernet(key)
        return f.encrypt(private_key.encode()).decode()
    
    def _decrypt_private_key(self, encrypted_key: str, password: str) -> str:
        """Descifrar clave privada con contraseña"""
        from cryptography.fernet import Fernet
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
        import base64
        
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'rudag_salt',
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        f = Fernet(key)
        return f.decrypt(encrypted_key.encode()).decode()
