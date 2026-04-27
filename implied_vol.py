"""
implied_vol.py
--------------
Implied volatility calculator using Brent's method.
"""

from scipy.optimize import brentq
from bs_pricer import bs_call


def implied_vol(S, K, T, r, market_price, low=0.001, high=10.0):
    """
    Compute implied volatility via root-finding (Brent's method).

    Parameters
    ----------
    S            : float  Current stock price
    K            : float  Strike price
    T            : float  Time to expiry in years
    r            : float  Risk-free rate
    market_price : float  Observed market price of the call
    low          : float  Lower bound for vol search (default 0.1%)
    high         : float  Upper bound for vol search (default 1000%)

    Returns
    -------
    float or None : Implied volatility, or None if no solution found
    """
    try:
        iv = brentq(
            lambda sigma: bs_call(S, K, T, r, sigma) - market_price,
            low,
            high
        )
        return iv
    except ValueError:
        return None


def vol_smile(S, T, r, strikes, market_prices):
    """
    Compute implied volatility across a range of strikes.

    Parameters
    ----------
    S             : float       Current stock price
    T             : float       Time to expiry in years
    r             : float       Risk-free rate
    strikes       : list[float] Strike prices
    market_prices : list[float] Corresponding market call prices

    Returns
    -------
    list[tuple] : (strike, implied_vol) pairs where solution exists
    """
    results = []
    for K, price in zip(strikes, market_prices):
        iv = implied_vol(S, K, T, r, price)
        if iv is not None:
            results.append((K, iv))
    return results
