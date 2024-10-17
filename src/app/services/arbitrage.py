import time
import heapq
from collections import defaultdict

class ArbitrageDetector:
    def __init__(self, exchange_graph, socketio, config):
        self.exchange_graph = exchange_graph
        self.socketio = socketio
        self.initial_balance = config['INITIAL_BALANCE']
        self.current_balance = self.initial_balance
        self.balance_history = [(time.time(), self.initial_balance)]
        self.executed_arbitrages = {}
        self.max_arbitrage_profit = config['MAX_ARBITRAGE_PROFIT']
        self.check_interval = config['ARBITRAGE_CHECK_INTERVAL']

    def find_arbitrage_opportunities(self):
        currencies = self.exchange_graph.get_currencies()
        if not currencies:
            return []

        stablecoins = ['USDC', 'USDT']
        opportunities = []

        for start in stablecoins:
            if start not in currencies:
                continue

            n = len(currencies)
            
            distances = {currency: float('inf') for currency in currencies}
            distances[start] = 0
            
            for _ in range(n - 1):
                for source in currencies:
                    for target, rate in self.exchange_graph.graph[source].items():
                        weight = self.exchange_graph.calculate_weight(rate)
                        try:
                            if distances[source] + weight < distances[target]:
                                distances[target] = distances[source] + weight
                        except:
                            pass

            for source in currencies:
                for target, rate in self.exchange_graph.graph[source].items():
                    weight = self.exchange_graph.calculate_weight(rate)
                    cycle = self.detect_cycle(source, target, distances, start)
                    if cycle:
                        profit = self.calculate_profit(cycle)
                        opportunities.append((profit, cycle))

        return opportunities

    def detect_cycle(self, start, end, distances, stablecoin):
        cycle = [end, start]
        current = start
        visited = set()
        
        while current not in visited:
            visited.add(current)
            best_prev = None
            best_weight = float('inf')
            
            for prev, rate in self.exchange_graph.graph.items():
                if current in rate:
                    weight = self.exchange_graph.calculate_weight(rate[current])
                    if distances[prev] + weight < best_weight:
                        best_prev = prev
                        best_weight = distances[prev] + weight
            
            if best_prev is None:
                return None
            
            cycle.append(best_prev)
            current = best_prev
            
            if current == stablecoin:
                return cycle[::-1]
        
        return None

    def calculate_profit(self, cycle):
        profit = 1.0
        for i in range(len(cycle) - 1):
            profit *= self.exchange_graph.get_rate(cycle[i], cycle[i+1])
        return profit - 1

    def simulate_arbitrage(self, opportunities):
        current_time = time.time()
        
        for profit, cycle in opportunities:
            if profit > 0.01:
                continue
            cycle_key = tuple(cycle)
            if cycle_key not in self.executed_arbitrages or current_time - self.executed_arbitrages[cycle_key] > 100:
                self.current_balance *= (1 + profit)
                self.executed_arbitrages[cycle_key] = current_time
                self.balance_history.append((current_time, self.current_balance))
                break

    def print_top_opportunities(self):
        while True:
            if len(self.exchange_graph.graph) < 2:
                print("Awaiting sufficient data...")
                time.sleep(self.check_interval)
                continue

            opportunities = self.find_arbitrage_opportunities()
            opportunities = [(profit, cycle) for profit, cycle in opportunities if profit <= self.max_arbitrage_profit]
            if not opportunities:
                print("No arbitrage opportunities found.")
            else:
                top_5 = heapq.nlargest(5, opportunities, key=lambda x: x[0])
                
                print("\n--- Top 5 Arbitrage Opportunities ---")
                for i, (profit, cycle) in enumerate(top_5, 1):
                    print(f"{i}. Profit: {profit*100:.2f}% - Cycle: {' -> '.join(cycle)}")
                print("----------------------------------------\n")

                self.simulate_arbitrage(top_5)

                print(f"Current Balance: ${self.current_balance:.2f}")
                print(f"Balance History: {self.balance_history}")

                self.socketio.emit('update_data', {
                    'balance': self.current_balance,
                    'balance_history': self.balance_history,
                    'top_opportunities': [{'profit': profit, 'cycle': cycle} for profit, cycle in top_5]
                })
            
            time.sleep(self.check_interval)