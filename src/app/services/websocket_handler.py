import websocket
import json

class WebSocketHandler:
    def __init__(self, exchange_graph, socketio):
        self.exchange_graph = exchange_graph
        self.socketio = socketio

    def on_message(self, ws, message):
        data = json.loads(message)
        stream = data['stream']
        ticker_data = data['data']
        
        self.exchange_graph.update(ticker_data)
        
        self.socketio.emit('ticker_update', {'stream': stream, 'data': ticker_data})

    def on_error(self, ws, error):
        print(f"Error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        print("Connection closed")

    def on_open(self, ws):
        print("Connection opened")

    def run_websocket(self, pairs, streams_per_socket=1000):
        base_url = "wss://stream.binance.com:9443/stream?streams="
        streams = "/".join([f"{pair}@ticker" for pair in pairs[:streams_per_socket]])
        url = base_url + streams
        
        ws = websocket.WebSocketApp(url,
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)
        ws.on_open = self.on_open
        ws.run_forever()