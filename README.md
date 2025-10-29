# Rudag Network SDK

[![PyPI version](https://img.shields.io/pypi/v/rudag-sdk.svg)](https://pypi.org/project/rudag-sdk/)
[![Python Versions](https://img.shields.io/pypi/pyversions/rudag-sdk.svg)](https://pypi.org/project/rudag-sdk/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation](https://img.shields.io/badge/docs-latest-blue.svg)](https://rudag-network.github.io/rudag-sdk-python)
[![Build Status](https://github.com/Rudag-Network/rudag-sdk-python/actions/workflows/test.yml/badge.svg)](https://github.com/Rudag-Network/rudag-sdk-python/actions)

SDK oficial de Python para interactuar con la blockchain de **Rudag Network**. Esta librería proporciona una interfaz completa para desarrollar aplicaciones descentralizadas (dApps), wallets, exploradores y cualquier otro servicio sobre la red RUDAG.

## ✨ Características

- 🏦 **Gestión completa de wallets** - Crear, importar y gestionar direcciones RUDAG
- 💸 **Transacciones** - Enviar y recibir RGD de forma segura
- ⛓️ **Blockchain** - Consultar bloques, transacciones y información de la red
- ⛏️ **Minería** - Soporte para operaciones de minería
- 🌐 **Red P2P** - Gestión de nodos y sincronización
- 🔄 **Tiempo real** - WebSocket para eventos en tiempo real
- 🛡️ **Seguro** - Cifrado y mejores prácticas de seguridad
- 🚀 **Asíncrono** - Soporte completo para operaciones asíncronas
- 📚 **Bien documentado** - Documentación completa y ejemplos

## 📦 Instalación

### Instalación desde PyPI
```bash
pip install rudag-sdk
```

### Instalación desde fuente
```bash
git clone https://github.com/Rudag-Network/rudag-sdk-python.git
cd rudag-sdk-python
pip install -e .
```

### Dependencias opcionales
```bash
# Para desarrollo
pip install rudag-sdk[dev]

# Para soporte asíncrono completo
pip install rudag-sdk[async]
```

## 🚀 Uso Rápido

### Crear una Wallet
```python
from rudag_sdk import RudagSDK, RudagConfig

# Configurar SDK
config = RudagConfig(node_url="http://localhost:5000")
sdk = RudagSDK(config)

# Crear nueva wallet
wallet = sdk.create_wallet()
print(f"💰 Nueva wallet: {wallet.address}")
print(f"🔑 Clave pública: {wallet.public_key}")

# Obtener balance
balance = sdk.get_balance(wallet.address)
print(f"💳 Balance: {balance} RGD")
```

### Enviar una Transacción
```python
from rudag_sdk import RudagTransaction

# Crear transacción
transaction = RudagTransaction(
    sender="RGD:1A77LFiAzzVnDdpMRjKqwB3ZjiVnuNqQjk",
    recipient="RGD:2B88MBgVxzVnDdpMRjKqwB3ZjiVnuNqQjl",
    amount=10.5,
    fee=0.001
)

# Enviar transacción
result = sdk.send_transaction(transaction, "tu_clave_privada")
print(f"✅ Transacción enviada: {result['transaction_id']}")
```

### Consultar la Blockchain
```python
# Obtener información de la red
network_info = sdk.get_network_info()
print(f"🌐 Red: {network_info['name']}")
print(f"📦 Altura de bloque: {network_info['block_height']}")

# Obtener último bloque
last_block = sdk.get_block(block_height=network_info['block_height'] - 1)
print(f"⛓️  Hash del bloque: {last_block['hash']}")
```

## 📚 Ejemplos

Visita la [carpeta de ejemplos](examples/) para ver casos de uso completos:

- [Wallet básica](examples/basic_wallet.py)
- [Sistema de pagos](examples/payment_system.py)
- [Monitor en tiempo real](examples/real_time_monitor.py)
- [Token personalizado](examples/custom_token.py)

## 🔧 Configuración

### Configuración básica
```python
from rudag_sdk import RudagConfig

config = RudagConfig(
    node_url="http://localhost:5000",  # URL del nodo RUDAG
    network="mainnet",                 # mainnet o testnet
    timeout=30,                        # timeout en segundos
    retry_attempts=3                   # intentos de reintento
)
```

### Configuración avanzada
```python
config = RudagConfig(
    node_url="http://localhost:5000",
    network="mainnet",
    timeout=30,
    retry_attempts=3,
    api_key="tu_api_key",              # Para APIs protegidas
    websocket_url="ws://localhost:5000/ws",  # WebSocket para eventos
    auto_connect=True,                 # Conexión automática
    debug=False                        # Modo debug
)
```

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor lee nuestra [guía de contribución](CONTRIBUTING.md) para empezar.

1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🔗 Enlaces

- [Documentación completa](https://rudag-network.github.io/rudag-sdk-python)
- [Repositorio oficial](https://github.com/Rudag-Network/rudag-sdk-python)
- [Reportar un issue](https://github.com/Rudag-Network/rudag-sdk-python/issues)
- [Rudag Network](https://rudag.canariannode.uk/)

## ⚠️ Disclaimer

Este software se proporciona "tal cual", sin garantía de ningún tipo. El uso de esta SDK es bajo tu propio riesgo. Siempre verifica las transacciones y mantén tus claves privadas seguras.
