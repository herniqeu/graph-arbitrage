import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

class Config:
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    SECRET_KEY = os.getenv('SECRET_KEY', 'chave_secreta_padrao')
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    SOCKETIO_ASYNC_MODE = os.getenv('SOCKETIO_ASYNC_MODE', 'eventlet')
    BINANCE_API_KEY = os.getenv('BINANCE_API_KEY', '')
    BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET', '')
    DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///arbitrage.db')
    INITIAL_BALANCE = float(os.getenv('INITIAL_BALANCE', '100'))
    MAX_ARBITRAGE_PROFIT = float(os.getenv('MAX_ARBITRAGE_PROFIT', '0.01'))
    ARBITRAGE_CHECK_INTERVAL = int(os.getenv('ARBITRAGE_CHECK_INTERVAL', '10'))

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    return config[os.getenv('FLASK_ENV', 'default')]