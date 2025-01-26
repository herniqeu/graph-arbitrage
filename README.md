# Crypto Arbitrage Bot

## Overview

This project implements a real-time cryptocurrency arbitrage detection and execution system. It monitors multiple cryptocurrency exchanges, identifies profitable arbitrage opportunities, and simulates their execution. The system uses websocket connections to receive live market data and employs graph theory algorithms to detect arbitrage cycles.

## Features

- Real-time market data collection via WebSocket
- Arbitrage opportunity detection using the Bellman-Ford algorithm
- Simulated arbitrage execution
- Live dashboard for monitoring arbitrage opportunities and portfolio value

## Math and Algorithms

### Arbitrage Detection

We use a modified version of the Bellman-Ford algorithm to detect negative cycles in a graph representation of exchange rates. 

1. **Graph Representation**: Each cryptocurrency is a node, and exchange rates are weighted edges.

2. **Edge Weight Calculation**: 
   For an exchange rate `r` from currency A to B, the edge weight `w` is:
   w = -log(r)
   This transformation allows us to use addition instead of multiplication when calculating arbitrage profits.

3. **Bellman-Ford Algorithm**: We run V-1 iterations (where V is the number of vertices) of the following relaxation step:

```
for each edge (u, v) with weight w:
  if distance[u] + w < distance[v]:
    distance[v] = distance[v] + w
```

If after these iterations we can still relax an edge, we have found a negative cycle, which represents an arbitrage opportunity.

4. **Profit Calculation**: For a cycle `c` of currencies `[c₁, c₂, ..., cₙ, c₁]`, the profit `p` is:

p = (r₁₂ * r₂₃ * ... * rₙ₁) - 1

where `rᵢⱼ` is the exchange rate from currency `i` to `j`.

### Arbitrage Execution Simulation

The simulation assumes instant execution and no transaction fees. For each arbitrage opportunity:

1. Calculate the profit percentage `p`.
2. Update the simulated balance `B`:
B_new = B * (1 + p)

## Setup and Running

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up your `.env` file with necessary configurations
4. Run the application: `python app/main.py`

## Configuration

Key configuration options in `.env`:

- `INITIAL_BALANCE`: Starting balance for simulation
- `MAX_ARBITRAGE_PROFIT`: Maximum allowed profit for an arbitrage opportunity
- `ARBITRAGE_CHECK_INTERVAL`: Time between arbitrage checks
- `BINANCE_API_KEY` and `BINANCE_API_SECRET`: Your Binance API credentials

## Dashboard

The dashboard displays:
- Current simulated balance
- Portfolio value over time
- Top 5 current arbitrage opportunities
