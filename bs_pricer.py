"""
bs_pricer.py
------------
Core Black-Scholes pricing functions for European call and put options.
"""

import numpy as np
from scipy.stats import norm


def _d1_d2(S, K, T, r, sigma):
    """Compute d1 and d2 for Black-Scholes."""
    d1 = (np.log(S / K) + (r + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return d1, d2


def bs_call(S, K, T, r, sigma):
    """
    Black-Scholes European call option price.

    Parameters
    ----------
    S     : float  Current stock price
    K     : float  Strike price
    T     : float  Time to expiry in years
    r     : float  Risk-free rate
    sigma : float  Annualized volatility

    Returns
    -------
    float : Call option price
    """
    d1, d2 = _d1_d2(S, K, T, r, sigma)
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)


def bs_put(S, K, T, r, sigma):
    """
    Black-Scholes European put option price.

    Parameters
    ----------
    Same as bs_call.

    Returns
    -------
    float : Put option price
    """
    d1, d2 = _d1_d2(S, K, T, r, sigma)
    return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)


def put_call_parity_check(S, K, T, r, sigma, tol=1e-6):
    """
    Verify put-call parity: C - P = S - K * e^(-rT)

    Returns
    -------
    bool : True if parity holds within tolerance
    """
    C = bs_call(S, K, T, r, sigma)
    P = bs_put(S, K, T, r, sigma)
    lhs = C - P
    rhs = S - K * np.exp(-r * T)
    return abs(lhs - rhs) < tol
