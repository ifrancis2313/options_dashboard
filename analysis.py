"""
analysis.py
-----------
Visualization tools: Greeks vs stock price, vol smile, P&L heatmap.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from bs_pricer import bs_call, _d1_d2
from greeks import delta, gamma, theta, vega
from implied_vol import vol_smile as compute_vol_smile


def plot_greeks(K, T, r, sigma, S_range=None):
    """
    Plot all 4 main Greeks vs stock price.

    Parameters
    ----------
    K       : float  Strike price
    T       : float  Time to expiry in years
    r       : float  Risk-free rate
    sigma   : float  Volatility
    S_range : array  Stock price range (default 60% to 140% of K)
    """
    if S_range is None:
        S_range = np.linspace(K * 0.6, K * 1.4, 200)

    deltas = [delta(S, K, T, r, sigma) for S in S_range]
    gammas = [gamma(S, K, T, r, sigma) for S in S_range]
    thetas = [theta(S, K, T, r, sigma) for S in S_range]
    vegas  = [vega(S, K, T, r, sigma)  for S in S_range]

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle(f"Greeks vs Stock Price  (K={K}, T={T}y, σ={sigma})", fontsize=14)

    for ax, values, name, color in zip(
        axes.flat,
        [deltas, gammas, thetas, vegas],
        ["Delta", "Gamma", "Theta (per day)", "Vega (per 1% vol)"],
        ["#2196F3", "#4CAF50", "#F44336", "#FF9800"]
    ):
        ax.plot(S_range, values, color=color, linewidth=2)
        ax.axvline(K, color="grey", linestyle="--", alpha=0.5, label="Strike")
        ax.set_title(name)
        ax.set_xlabel("Stock Price")
        ax.legend()
        ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig("greeks_plot.png", dpi=150)
    plt.show()
    print("Saved: greeks_plot.png")


def plot_vol_smile(S, T, r, strikes, market_prices):
    """
    Plot the implied volatility smile across strikes.
    """
    results = compute_vol_smile(S, T, r, strikes, market_prices)
    if not results:
        print("No valid IV solutions found.")
        return

    ks, ivs = zip(*results)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(ks, [iv * 100 for iv in ivs], "o-", color="#673AB7", linewidth=2, markersize=7)
    ax.axvline(S, color="grey", linestyle="--", alpha=0.5, label=f"Spot = {S}")
    ax.set_title("Implied Volatility Smile", fontsize=13)
    ax.set_xlabel("Strike")
    ax.set_ylabel("Implied Vol (%)")
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.1f%%"))
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("vol_smile.png", dpi=150)
    plt.show()
    print("Saved: vol_smile.png")


def pnl_heatmap(K, r, sigma, stock_prices=None, days=None):
    """
    Compute and display call option P&L heatmap across
    stock prices and days to expiry.
    """
    if stock_prices is None:
        stock_prices = [80, 85, 90, 95, 100, 105, 110, 115, 120]
    if days is None:
        days = [1, 30, 60, 90, 180, 365]

    rows = []
    for S in stock_prices:
        row = {}
        for d in days:
            T = d / 365
            row[f"{d}d"] = round(bs_call(S, K, T, r, sigma), 2)
        rows.append(row)

    df = pd.DataFrame(rows, index=stock_prices)
    df.index.name = "Stock"

    print("\nCall Price Heatmap (rows=stock price, cols=days to expiry)\n")
    print(df.to_string())

    # Plot heatmap
    fig, ax = plt.subplots(figsize=(10, 6))
    im = ax.imshow(df.values, cmap="RdYlGn", aspect="auto")
    ax.set_xticks(range(len(df.columns)))
    ax.set_xticklabels(df.columns)
    ax.set_yticks(range(len(df.index)))
    ax.set_yticklabels(df.index)
    ax.set_title(f"Call Price Heatmap  (K={K}, σ={sigma})", fontsize=13)
    ax.set_xlabel("Days to Expiry")
    ax.set_ylabel("Stock Price")
    plt.colorbar(im, ax=ax, label="Call Price ($)")

    for i in range(len(df.index)):
        for j in range(len(df.columns)):
            ax.text(j, i, f"{df.values[i, j]:.1f}",
                    ha="center", va="center", fontsize=8, color="black")

    plt.tight_layout()
    plt.savefig("pnl_heatmap.png", dpi=150)
    plt.show()
    print("Saved: pnl_heatmap.png")

    return df
