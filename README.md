# Black-Scholes Options Analytics Dashboard

A Python toolkit for pricing European options, computing Greeks, calculating implied volatility, and analyzing options strategies.

Built as part of a quant finance learning curriculum, with direct application to options pricing research.

---

## Features

- **Black-Scholes Pricer** — European call and put pricing with put-call parity verification
- **Greeks** — Delta, Gamma, Theta, Vega, Rho
- **Implied Volatility** — Numerical solver using Brent's method
- **Strategies** — Straddle, bull call spread, bear put spread
- **Analysis** — Volatility smile, Greeks plots, P&L heatmap
- **CLI** — Run directly from terminal

---

## Installation

```bash
git clone https://github.com/yourusername/options_dashboard.git
cd options_dashboard
pip install -r requirements.txt
```

---

## Usage

### CLI
```bash
# Price a call and put
python pricer.py --S 100 --K 105 --T 30 --r 0.05 --sigma 0.2

# With Greeks
python pricer.py --S 100 --K 100 --T 365 --r 0.05 --sigma 0.2 --greeks

# With straddle analysis
python pricer.py --S 100 --K 100 --T 365 --r 0.05 --sigma 0.2 --straddle

# With P&L heatmap
python pricer.py --S 100 --K 100 --T 365 --r 0.05 --sigma 0.2 --heatmap

# Plot Greeks
python pricer.py --S 100 --K 100 --T 365 --r 0.05 --sigma 0.2 --plot
```

### Python API
```python
from bs_pricer import bs_call, bs_put
from greeks import all_greeks
from implied_vol import implied_vol
from strategies import straddle

# Price options
call = bs_call(S=100, K=100, T=1, r=0.05, sigma=0.2)
put  = bs_put(S=100,  K=100, T=1, r=0.05, sigma=0.2)

# Greeks
greeks = all_greeks(S=100, K=100, T=1, r=0.05, sigma=0.2)

# Implied volatility
iv = implied_vol(S=100, K=100, T=1, r=0.05, market_price=12.0)

# Straddle
s = straddle(S=100, K=100, T=1, r=0.05, sigma=0.2)
```

---

## Project Structure

```
options_dashboard/
├── bs_pricer.py      # Black-Scholes call/put pricing
├── greeks.py         # Delta, Gamma, Theta, Vega, Rho
├── implied_vol.py    # IV calculator and vol smile
├── strategies.py     # Straddle, spreads
├── analysis.py       # Visualizations
├── pricer.py         # CLI entry point
└── requirements.txt
```

---

## Theory

### Black-Scholes Formula
```
C = S·N(d1) - K·e^(-rT)·N(d2)
P = K·e^(-rT)·N(-d2) - S·N(-d1)

d1 = [ln(S/K) + (r + σ²/2)·T] / (σ·√T)
d2 = d1 - σ·√T
```

### The Greeks
| Greek | Measures |
|-------|----------|
| Delta | Price sensitivity to stock movement |
| Gamma | Rate of change of Delta |
| Theta | Time decay per day |
| Vega  | Sensitivity to volatility |
| Rho   | Sensitivity to interest rates |

---

## Requirements

- Python 3.8+
- numpy
- scipy
- pandas
- matplotlib
