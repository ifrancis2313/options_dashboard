"""
strategies.py
-------------
Common options strategies: straddle, bull spread, bear spread.
"""

from bs_pricer import bs_call, bs_put


def straddle(S, K, T, r, sigma):
    """
    Long straddle: buy call + buy put at same strike.

    Returns
    -------
    dict : total_cost, upper_breakeven, lower_breakeven
    """
    C = bs_call(S, K, T, r, sigma)
    P = bs_put(S, K, T, r, sigma)
    total_cost = C + P
    return {
        "call_price":       round(C, 4),
        "put_price":        round(P, 4),
        "total_cost":       round(total_cost, 4),
        "upper_breakeven":  round(K + total_cost, 4),
        "lower_breakeven":  round(K - total_cost, 4),
    }


def bull_call_spread(S, K_low, K_high, T, r, sigma):
    """
    Bull call spread: buy lower strike call, sell higher strike call.

    Returns
    -------
    dict : net_cost, max_profit, max_loss, breakeven
    """
    C_low  = bs_call(S, K_low,  T, r, sigma)
    C_high = bs_call(S, K_high, T, r, sigma)
    net_cost   = C_low - C_high
    max_profit = (K_high - K_low) - net_cost
    return {
        "net_cost":   round(net_cost, 4),
        "max_profit": round(max_profit, 4),
        "max_loss":   round(net_cost, 4),
        "breakeven":  round(K_low + net_cost, 4),
    }


def bear_put_spread(S, K_high, K_low, T, r, sigma):
    """
    Bear put spread: buy higher strike put, sell lower strike put.

    Returns
    -------
    dict : net_cost, max_profit, max_loss, breakeven
    """
    P_high = bs_put(S, K_high, T, r, sigma)
    P_low  = bs_put(S, K_low,  T, r, sigma)
    net_cost   = P_high - P_low
    max_profit = (K_high - K_low) - net_cost
    return {
        "net_cost":   round(net_cost, 4),
        "max_profit": round(max_profit, 4),
        "max_loss":   round(net_cost, 4),
        "breakeven":  round(K_high - net_cost, 4),
    }
