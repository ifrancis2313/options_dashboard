"""
greeks.py
---------
Black-Scholes Greeks for European call options.
"""

import numpy as np
from scipy.stats import norm
from bs_pricer import _d1_d2


def delta(S, K, T, r, sigma):
    """Rate of change of option price w.r.t. stock price."""
    d1, _ = _d1_d2(S, K, T, r, sigma)
    return norm.cdf(d1)


def gamma(S, K, T, r, sigma):
    """Rate of change of delta w.r.t. stock price."""
    d1, _ = _d1_d2(S, K, T, r, sigma)
    return norm.pdf(d1) / (S * sigma * np.sqrt(T))


def theta(S, K, T, r, sigma):
    """Time decay — change in option price per day."""
    d1, d2 = _d1_d2(S, K, T, r, sigma)
    daily_theta = (
        -(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T))
        - r * K * np.exp(-r * T) * norm.cdf(d2)
    )
    return daily_theta / 365  # per day


def vega(S, K, T, r, sigma):
    """Change in option price per 1% move in volatility."""
    d1, _ = _d1_d2(S, K, T, r, sigma)
    return S * norm.pdf(d1) * np.sqrt(T) * 0.01  # per 1% vol move


def rho(S, K, T, r, sigma):
    """Change in option price per 1% move in risk-free rate."""
    _, d2 = _d1_d2(S, K, T, r, sigma)
    return K * T * np.exp(-r * T) * norm.cdf(d2) * 0.01  # per 1% rate move


def all_greeks(S, K, T, r, sigma):
    """Return all Greeks as a dictionary."""
    return {
        "Delta": delta(S, K, T, r, sigma),
        "Gamma": gamma(S, K, T, r, sigma),
        "Theta": theta(S, K, T, r, sigma),
        "Vega":  vega(S, K, T, r, sigma),
        "Rho":   rho(S, K, T, r, sigma),
    }
