from collections import defaultdict
import math

class ExchangeGraph:
    def __init__(self):
        self.graph = defaultdict(dict)

    def update(self, ticker_data):
        symbol = ticker_data['s']
        price = float(ticker_data['c'])
        
        crypto1, crypto2 = symbol[:-4], symbol[-4:]
        
        self.graph[crypto1][crypto2] = price
        
        if price != 0:
            self.graph[crypto2][crypto1] = 1 / price

    @staticmethod
    def calculate_weight(rate):
        return -math.log(rate)

    def get_currencies(self):
        return list(self.graph.keys())

    def get_rate(self, source, target):
        return self.graph[source].get(target)