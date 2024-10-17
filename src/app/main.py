from flask import Flask, render_template
from flask_socketio import SocketIO
from config import get_config
from models.exchange_graph import ExchangeGraph
from services.arbitrage import ArbitrageDetector
from services.websocket_handler import WebSocketHandler
from api.binance_api import get_all_pairs
import threading

app = Flask(__name__, template_folder='../templates')
app.config.from_object(get_config())
socketio = SocketIO(app)

exchange_graph = ExchangeGraph()
arbitrage_detector = ArbitrageDetector(exchange_graph, socketio, app.config)
websocket_handler = WebSocketHandler(exchange_graph, socketio)

@app.route('/')
def index():
    return render_template('index.html')

def start_websocket():
    pairs = get_all_pairs()
    websocket_handler.run_websocket(pairs)

def start_arbitrage_detection():
    arbitrage_detector.print_top_opportunities()

if __name__ == '__main__':
    websocket_thread = threading.Thread(target=start_websocket)
    websocket_thread.start()
    
    arbitrage_thread = threading.Thread(target=start_arbitrage_detection)
    arbitrage_thread.start()
    
    socketio.run(app, debug=app.config['DEBUG'])